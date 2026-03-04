from dataclasses import dataclass, field
from typing import List


@dataclass
class SimulationConfig:
    # AI Technology
    ai_cap_max: float = 1.0
    ai_growth_rate: float = 0.1
    ai_inflection_point: float = 50.0
    innovation_rate: float = 0.02

    # Coase / Bargaining
    transaction_cost: float = 0.1
    info_asymmetry: float = 0.2
    legal_friction: float = 0.1
    coordination_cost: float = 0.05
    worker_bargaining_power: float = 0.5

    # Labor Market
    n_workers: int = 1000
    n_firms: int = 50
    n_sectors: int = 5
    matching_efficiency: float = 0.3
    retraining_duration: int = 4
    vacancy_rate: float = 0.05

    # Production
    labor_share: float = 0.65
    monopsony_markdown: float = 0.1
    job_creation_multiplier: float = 0.1
    base_job_creation: float = 5.0
    horizon: int = 10

    # Simulation
    n_periods: int = 200
    random_seed: int = 42

    # Sector names
    sector_names: List[str] = field(
        default_factory=lambda: [
            "Manufacturing",
            "Services",
            "Tech",
            "Healthcare",
            "Creative",
        ]
    )
