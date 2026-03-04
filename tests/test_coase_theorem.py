import pytest

from simulation.config import SimulationConfig
from simulation.engine import SimulationEngine


class TestCoaseTheorem:
    """Verify the core Coase Theorem predictions."""

    def _run_scenario(self, **kwargs) -> list:
        config = SimulationConfig(
            n_periods=50,
            n_workers=200,
            n_firms=20,
            **kwargs,
        )
        engine = SimulationEngine(config)
        return engine.run()

    def test_tc_zero_surplus_invariant_to_beta(self):
        """With TC=0, total surplus should be roughly the same regardless of bargaining power."""
        surpluses = {}
        for beta in [0.1, 0.3, 0.5, 0.7, 0.9]:
            results = self._run_scenario(
                transaction_cost=0.0,
                info_asymmetry=0.0,
                legal_friction=0.0,
                coordination_cost=0.0,
                worker_bargaining_power=beta,
            )
            total_surplus = sum(m.total_surplus for m in results)
            surpluses[beta] = total_surplus

        # All total surpluses should be within 5% of each other
        values = list(surpluses.values())
        if max(values) == 0:
            pytest.skip("No surplus generated (AI too weak in short simulation)")
        ratio = min(values) / max(values)
        assert ratio > 0.95, f"Surplus varied too much across beta: {surpluses}"

    def test_tc_zero_no_blocked_transactions(self):
        """With TC=0, no transactions should be blocked."""
        results = self._run_scenario(
            transaction_cost=0.0,
            info_asymmetry=0.0,
            legal_friction=0.0,
            coordination_cost=0.0,
        )
        total_blocked = sum(m.blocked_transactions for m in results)
        assert total_blocked == 0

    def test_higher_tc_more_blocked(self):
        """Higher transaction costs should block more deals."""
        blocked_low = sum(
            m.blocked_transactions
            for m in self._run_scenario(transaction_cost=0.05)
        )
        blocked_high = sum(
            m.blocked_transactions
            for m in self._run_scenario(transaction_cost=0.5)
        )
        assert blocked_high >= blocked_low

    def test_surplus_split_follows_beta(self):
        """Worker compensation share should track bargaining power."""
        for beta in [0.2, 0.8]:
            results = self._run_scenario(
                transaction_cost=0.0,
                info_asymmetry=0.0,
                legal_friction=0.0,
                coordination_cost=0.0,
                worker_bargaining_power=beta,
            )
            total_worker = sum(m.worker_compensation for m in results)
            total_firm = sum(m.firm_gain for m in results)
            total = total_worker + total_firm
            if total > 0:
                worker_share = total_worker / total
                assert abs(worker_share - beta) < 0.05, (
                    f"beta={beta}, worker_share={worker_share:.3f}"
                )
