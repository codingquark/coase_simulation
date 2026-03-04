from dataclasses import dataclass, field
from typing import List, Dict

import numpy as np

from simulation.agents import Worker, Firm
from simulation.sectors import Sector


@dataclass
class PeriodMetrics:
    period: int
    employment_rate: float
    mean_wage: float
    median_wage: float
    displacement_rate: float
    new_jobs: int
    matches_made: int
    total_automation: float
    ai_capability: float
    blocked_transactions: int
    total_surplus: float
    worker_compensation: float
    firm_gain: float
    deadweight_loss: float
    retraining_pool: int
    sector_employment: Dict[str, float] = field(default_factory=dict)
    sector_wages: Dict[str, float] = field(default_factory=dict)
    sector_automation: Dict[str, float] = field(default_factory=dict)


class MetricsCollector:
    def __init__(self):
        self.history: List[PeriodMetrics] = []
        self._period_surplus = 0.0
        self._period_worker_comp = 0.0
        self._period_firm_gain = 0.0
        self._period_deadweight = 0.0
        self._period_blocked = 0
        self._period_displaced = 0

    def reset_period(self):
        self._period_surplus = 0.0
        self._period_worker_comp = 0.0
        self._period_firm_gain = 0.0
        self._period_deadweight = 0.0
        self._period_blocked = 0
        self._period_displaced = 0

    def record_bargain(
        self,
        surplus: float,
        worker_comp: float,
        firm_gain: float,
        deadweight: float,
        blocked: bool,
        displaced: bool,
    ):
        self._period_surplus += surplus
        self._period_worker_comp += worker_comp
        self._period_firm_gain += firm_gain
        self._period_deadweight += deadweight
        if blocked:
            self._period_blocked += 1
        if displaced:
            self._period_displaced += 1

    def collect(
        self,
        period: int,
        workers: List[Worker],
        firms: List[Firm],
        sectors: List[Sector],
        ai_capability: float,
        matches_made: int,
        new_jobs: int,
    ) -> PeriodMetrics:
        n = len(workers)
        employed = [w for w in workers if w.employed]
        employed_wages = [w.wage for w in employed]
        retraining = sum(1 for w in workers if w.retraining_timer > 0)

        emp_rate = len(employed) / n if n > 0 else 0.0
        mean_wage = float(np.mean(employed_wages)) if employed_wages else 0.0
        median_wage = float(np.median(employed_wages)) if employed_wages else 0.0
        disp_rate = self._period_displaced / n if n > 0 else 0.0

        total_automation = float(np.mean([f.automation_level for f in firms])) if firms else 0.0

        # Sector-level metrics
        sector_emp = {}
        sector_wages = {}
        sector_auto = {}
        for sec in sectors:
            sec_workers = [w for w in workers if w.sector == sec.index]
            sec_employed = [w for w in sec_workers if w.employed]
            sec_firms = [f for f in firms if f.sector == sec.index]

            sector_emp[sec.name] = len(sec_employed) / len(sec_workers) if sec_workers else 0.0
            sector_wages[sec.name] = (
                float(np.mean([w.wage for w in sec_employed])) if sec_employed else 0.0
            )
            sector_auto[sec.name] = (
                float(np.mean([f.automation_level for f in sec_firms])) if sec_firms else 0.0
            )

        metrics = PeriodMetrics(
            period=period,
            employment_rate=emp_rate,
            mean_wage=mean_wage,
            median_wage=median_wage,
            displacement_rate=disp_rate,
            new_jobs=new_jobs,
            matches_made=matches_made,
            total_automation=total_automation,
            ai_capability=ai_capability,
            blocked_transactions=self._period_blocked,
            total_surplus=self._period_surplus,
            worker_compensation=self._period_worker_comp,
            firm_gain=self._period_firm_gain,
            deadweight_loss=self._period_deadweight,
            retraining_pool=retraining,
            sector_employment=sector_emp,
            sector_wages=sector_wages,
            sector_automation=sector_auto,
        )
        self.history.append(metrics)
        return metrics
