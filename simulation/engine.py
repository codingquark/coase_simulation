import math
from typing import List, Optional

import numpy as np
import pandas as pd

from simulation.config import SimulationConfig
from simulation.agents import Worker, Firm, create_workers, create_firms
from simulation.sectors import Sector, create_sectors
from simulation.bargaining import evaluate_automation
from simulation.labor_market import clear_labor_market
from simulation.metrics import MetricsCollector, PeriodMetrics


class SimulationEngine:
    def __init__(self, config: Optional[SimulationConfig] = None):
        self.config = config or SimulationConfig()
        self.rng = np.random.default_rng(self.config.random_seed)
        self.sectors: List[Sector] = []
        self.workers: List[Worker] = []
        self.firms: List[Firm] = []
        self.metrics = MetricsCollector()
        self.current_period = 0
        self.ai_capability = 0.0
        self._initialized = False

    def initialize(self):
        self.rng = np.random.default_rng(self.config.random_seed)
        self.sectors = create_sectors(self.config)
        self.workers = create_workers(self.config, self.sectors, self.rng)
        self.firms = create_firms(self.config, self.sectors, self.workers, self.rng)
        self.metrics = MetricsCollector()
        self.current_period = 0
        self.ai_capability = 0.0
        self._initialized = True

    def _ai_capability_curve(self, t: int) -> float:
        """Logistic S-curve for AI capability growth."""
        c = self.config
        return c.ai_cap_max / (1.0 + math.exp(-c.ai_growth_rate * (t - c.ai_inflection_point)))

    def _phase_ai_growth(self):
        """Phase 1: Update AI capability."""
        self.ai_capability = self._ai_capability_curve(self.current_period)
        for firm in self.firms:
            firm.ai_capability = self.ai_capability

    def _phase_automation_decisions(self):
        """Phase 2: Firms evaluate Coasian bargaining for each worker."""
        self.metrics.reset_period()
        workers_by_id = {w.id: w for w in self.workers}

        for firm in self.firms:
            sector = self.sectors[firm.sector]
            to_remove = []

            for wid in list(firm.worker_ids):
                worker = workers_by_id.get(wid)
                if worker is None or not worker.employed:
                    continue

                outcome = evaluate_automation(
                    worker=worker,
                    firm=firm,
                    sector=sector,
                    ai_capability=self.ai_capability,
                    config=self.config,
                )

                blocked = outcome.surplus > 0 and not outcome.automate
                self.metrics.record_bargain(
                    surplus=max(0, outcome.surplus),
                    worker_comp=outcome.worker_compensation,
                    firm_gain=outcome.firm_gain,
                    deadweight=outcome.deadweight_loss,
                    blocked=blocked,
                    displaced=outcome.automate,
                )

                if outcome.automate:
                    worker.employed = False
                    worker.displaced = True
                    worker.compensation_received += outcome.worker_compensation
                    worker.retraining_timer = self.config.retraining_duration
                    to_remove.append(wid)
                    firm.automation_level = min(
                        1.0, firm.automation_level + 1.0 / max(1, firm.n_workers)
                    )

            for wid in to_remove:
                if wid in firm.worker_ids:
                    firm.worker_ids.remove(wid)
                    firm.n_workers = max(0, firm.n_workers - 1)

    def _phase_labor_market(self) -> tuple:
        """Phase 3: Labor market clearing."""
        total_auto = float(np.mean([f.automation_level for f in self.firms]))
        return clear_labor_market(
            workers=self.workers,
            firms=self.firms,
            sectors=self.sectors,
            config=self.config,
            rng=self.rng,
            total_automation_level=total_auto,
        )

    def _phase_state_updates(self):
        """Phase 5: Update retraining timers and adjust state."""
        for w in self.workers:
            if w.retraining_timer > 0:
                w.retraining_timer -= 1
                # Skill improvement during retraining
                if w.retraining_timer == 0:
                    w.skill = min(1.0, w.skill + 0.05)

    def step(self) -> PeriodMetrics:
        """Execute one time period (all 5 phases)."""
        if not self._initialized:
            self.initialize()

        # Phase 1: AI growth
        self._phase_ai_growth()

        # Phase 2: Automation decisions
        self._phase_automation_decisions()

        # Phase 3 & 4: Labor market clearing (includes job creation)
        matches, new_jobs = self._phase_labor_market()

        # Phase 5: State updates
        self._phase_state_updates()

        # Collect metrics
        period_metrics = self.metrics.collect(
            period=self.current_period,
            workers=self.workers,
            firms=self.firms,
            sectors=self.sectors,
            ai_capability=self.ai_capability,
            matches_made=matches,
            new_jobs=new_jobs,
        )

        self.current_period += 1
        return period_metrics

    def run(self) -> List[PeriodMetrics]:
        """Run the full simulation."""
        self.initialize()
        results = []
        for _ in range(self.config.n_periods):
            results.append(self.step())
        return results

    def results_dataframe(self) -> pd.DataFrame:
        """Convert metrics history to a DataFrame."""
        records = []
        for m in self.metrics.history:
            row = {
                "period": m.period,
                "employment_rate": m.employment_rate,
                "mean_wage": m.mean_wage,
                "median_wage": m.median_wage,
                "displacement_rate": m.displacement_rate,
                "new_jobs": m.new_jobs,
                "matches_made": m.matches_made,
                "total_automation": m.total_automation,
                "ai_capability": m.ai_capability,
                "blocked_transactions": m.blocked_transactions,
                "total_surplus": m.total_surplus,
                "worker_compensation": m.worker_compensation,
                "firm_gain": m.firm_gain,
                "deadweight_loss": m.deadweight_loss,
                "retraining_pool": m.retraining_pool,
            }
            for sec_name in m.sector_employment:
                row[f"emp_{sec_name}"] = m.sector_employment[sec_name]
                row[f"wage_{sec_name}"] = m.sector_wages.get(sec_name, 0)
                row[f"auto_{sec_name}"] = m.sector_automation.get(sec_name, 0)
            records.append(row)
        return pd.DataFrame(records)
