from dataclasses import dataclass
from typing import Tuple

from simulation.agents import Worker, Firm
from simulation.sectors import Sector
from simulation.config import SimulationConfig


@dataclass
class BargainOutcome:
    automate: bool
    surplus: float
    transaction_cost: float
    net_surplus: float
    worker_compensation: float
    firm_gain: float
    deadweight_loss: float  # surplus lost to TC when deal is blocked


def compute_surplus(
    ai_capability: float,
    ai_applicability: float,
    worker_skill: float,
    worker_wage: float,
    horizon: int,
) -> float:
    """Compute the gross surplus from automating a worker's position."""
    return (ai_capability * ai_applicability - worker_skill * worker_wage) * horizon


def compute_transaction_cost(
    base_tc: float,
    info_asymmetry: float,
    legal_friction: float,
    coordination_cost: float,
    n_affected: int,
) -> float:
    """Compute the transaction cost for a bargaining round."""
    return base_tc * (1.0 + info_asymmetry + legal_friction + coordination_cost * n_affected)


def nash_bargain(
    surplus: float,
    transaction_cost: float,
    bargaining_power: float,
) -> Tuple[float, float, float]:
    """Nash bargaining solution.

    Returns (worker_compensation, firm_gain, net_surplus).
    If surplus <= transaction_cost, the deal is blocked.
    """
    net_surplus = surplus - transaction_cost
    if net_surplus <= 0:
        return 0.0, 0.0, net_surplus
    worker_comp = bargaining_power * net_surplus
    firm_gain = (1.0 - bargaining_power) * net_surplus
    return worker_comp, firm_gain, net_surplus


def evaluate_automation(
    worker: Worker,
    firm: Firm,
    sector: Sector,
    ai_capability: float,
    config: SimulationConfig,
) -> BargainOutcome:
    """Evaluate whether to automate a single worker's position via Coasian bargaining."""
    surplus = compute_surplus(
        ai_capability=ai_capability,
        ai_applicability=sector.ai_applicability,
        worker_skill=worker.skill,
        worker_wage=worker.wage,
        horizon=config.horizon,
    )

    if surplus <= 0:
        return BargainOutcome(
            automate=False,
            surplus=surplus,
            transaction_cost=0.0,
            net_surplus=surplus,
            worker_compensation=0.0,
            firm_gain=0.0,
            deadweight_loss=0.0,
        )

    tc = compute_transaction_cost(
        base_tc=config.transaction_cost,
        info_asymmetry=config.info_asymmetry,
        legal_friction=config.legal_friction,
        coordination_cost=config.coordination_cost,
        n_affected=firm.n_workers,
    )

    worker_comp, firm_gain, net_surplus = nash_bargain(
        surplus=surplus,
        transaction_cost=tc,
        bargaining_power=worker.bargaining_power,
    )

    if net_surplus <= 0:
        # Deal blocked by transaction costs — deadweight loss
        return BargainOutcome(
            automate=False,
            surplus=surplus,
            transaction_cost=tc,
            net_surplus=0.0,
            worker_compensation=0.0,
            firm_gain=0.0,
            deadweight_loss=surplus,  # entire surplus lost
        )

    return BargainOutcome(
        automate=True,
        surplus=surplus,
        transaction_cost=tc,
        net_surplus=net_surplus,
        worker_compensation=worker_comp,
        firm_gain=firm_gain,
        deadweight_loss=0.0,
    )
