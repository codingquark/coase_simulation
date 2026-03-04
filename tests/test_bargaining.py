import pytest

from simulation.bargaining import (
    compute_surplus,
    compute_transaction_cost,
    nash_bargain,
    evaluate_automation,
)
from simulation.agents import Worker, Firm
from simulation.sectors import Sector
from simulation.config import SimulationConfig


class TestComputeSurplus:
    def test_positive_surplus(self):
        surplus = compute_surplus(
            ai_capability=0.8,
            ai_applicability=0.7,
            worker_skill=0.5,
            worker_wage=0.8,
            horizon=10,
        )
        # (0.8*0.7 - 0.5*0.8) * 10 = (0.56 - 0.40) * 10 = 1.6
        assert pytest.approx(surplus, abs=0.01) == 1.6

    def test_negative_surplus(self):
        surplus = compute_surplus(
            ai_capability=0.1,
            ai_applicability=0.3,
            worker_skill=0.9,
            worker_wage=1.0,
            horizon=10,
        )
        assert surplus < 0

    def test_zero_ai_capability(self):
        surplus = compute_surplus(
            ai_capability=0.0,
            ai_applicability=0.5,
            worker_skill=0.5,
            worker_wage=1.0,
            horizon=10,
        )
        assert surplus < 0


class TestComputeTransactionCost:
    def test_basic(self):
        tc = compute_transaction_cost(
            base_tc=0.1, info_asymmetry=0.2, legal_friction=0.1,
            coordination_cost=0.05, n_affected=10,
        )
        # 0.1 * (1 + 0.2 + 0.1 + 0.05*10) = 0.1 * 1.8 = 0.18
        assert pytest.approx(tc, abs=0.001) == 0.18

    def test_zero_base_tc(self):
        tc = compute_transaction_cost(
            base_tc=0.0, info_asymmetry=0.5, legal_friction=0.5,
            coordination_cost=0.5, n_affected=100,
        )
        assert tc == 0.0


class TestNashBargain:
    def test_even_split(self):
        worker_comp, firm_gain, net = nash_bargain(
            surplus=10.0, transaction_cost=2.0, bargaining_power=0.5,
        )
        assert pytest.approx(net) == 8.0
        assert pytest.approx(worker_comp) == 4.0
        assert pytest.approx(firm_gain) == 4.0

    def test_all_to_worker(self):
        worker_comp, firm_gain, net = nash_bargain(
            surplus=10.0, transaction_cost=0.0, bargaining_power=1.0,
        )
        assert pytest.approx(worker_comp) == 10.0
        assert pytest.approx(firm_gain) == 0.0

    def test_all_to_firm(self):
        worker_comp, firm_gain, net = nash_bargain(
            surplus=10.0, transaction_cost=0.0, bargaining_power=0.0,
        )
        assert pytest.approx(worker_comp) == 0.0
        assert pytest.approx(firm_gain) == 10.0

    def test_blocked_deal(self):
        worker_comp, firm_gain, net = nash_bargain(
            surplus=5.0, transaction_cost=6.0, bargaining_power=0.5,
        )
        assert worker_comp == 0.0
        assert firm_gain == 0.0
        assert net < 0


class TestEvaluateAutomation:
    def _make_worker(self, **kwargs):
        defaults = dict(id=0, sector=0, skill=0.5, employed=True, wage=0.8, bargaining_power=0.5)
        defaults.update(kwargs)
        return Worker(**defaults)

    def _make_firm(self, **kwargs):
        defaults = dict(id=0, sector=0, n_workers=10, worker_ids=list(range(10)))
        defaults.update(kwargs)
        return Firm(**defaults)

    def _make_sector(self):
        return Sector(name="Test", index=0, ai_applicability=0.7, base_wage=1.0, base_productivity=1.0)

    def test_automate_when_surplus_high(self):
        config = SimulationConfig(transaction_cost=0.0)
        outcome = evaluate_automation(
            worker=self._make_worker(),
            firm=self._make_firm(),
            sector=self._make_sector(),
            ai_capability=0.9,
            config=config,
        )
        # surplus = (0.9*0.7 - 0.5*0.8)*10 = (0.63-0.4)*10 = 2.3 > 0
        assert outcome.automate is True
        assert outcome.surplus > 0
        assert outcome.deadweight_loss == 0.0

    def test_no_automate_when_ai_weak(self):
        config = SimulationConfig(transaction_cost=0.0)
        outcome = evaluate_automation(
            worker=self._make_worker(skill=0.9, wage=1.2),
            firm=self._make_firm(),
            sector=self._make_sector(),
            ai_capability=0.1,
            config=config,
        )
        assert outcome.automate is False

    def test_blocked_by_transaction_cost(self):
        config = SimulationConfig(transaction_cost=1.0, info_asymmetry=1.0, legal_friction=1.0)
        outcome = evaluate_automation(
            worker=self._make_worker(),
            firm=self._make_firm(),
            sector=self._make_sector(),
            ai_capability=0.9,
            config=config,
        )
        # surplus is positive but TC is very high
        assert outcome.automate is False
        assert outcome.deadweight_loss > 0
