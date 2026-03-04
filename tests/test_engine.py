import pytest

from simulation.config import SimulationConfig
from simulation.engine import SimulationEngine


class TestSimulationEngine:
    def test_initialization(self):
        engine = SimulationEngine()
        engine.initialize()
        assert len(engine.workers) == 1000
        assert len(engine.firms) == 50
        assert len(engine.sectors) == 5

    def test_single_step(self):
        engine = SimulationEngine(SimulationConfig(n_periods=10))
        engine.initialize()
        metrics = engine.step()
        assert metrics.period == 0
        assert 0 <= metrics.employment_rate <= 1.0
        assert metrics.mean_wage >= 0

    def test_full_run(self):
        config = SimulationConfig(n_periods=20, n_workers=100, n_firms=10)
        engine = SimulationEngine(config)
        results = engine.run()
        assert len(results) == 20
        assert results[-1].period == 19

    def test_reproducibility(self):
        config = SimulationConfig(n_periods=10, n_workers=100, n_firms=10)
        engine1 = SimulationEngine(config)
        r1 = engine1.run()
        engine2 = SimulationEngine(config)
        r2 = engine2.run()
        for m1, m2 in zip(r1, r2):
            assert m1.employment_rate == m2.employment_rate
            assert m1.mean_wage == m2.mean_wage
            assert m1.total_automation == m2.total_automation

    def test_results_dataframe(self):
        config = SimulationConfig(n_periods=5, n_workers=50, n_firms=5)
        engine = SimulationEngine(config)
        engine.run()
        df = engine.results_dataframe()
        assert len(df) == 5
        assert "employment_rate" in df.columns
        assert "period" in df.columns

    def test_no_automation_with_weak_ai(self):
        config = SimulationConfig(
            n_periods=20, n_workers=100, n_firms=10,
            ai_cap_max=0.01,
        )
        engine = SimulationEngine(config)
        results = engine.run()
        # automation should stay near zero
        assert all(m.total_automation < 0.05 for m in results)
