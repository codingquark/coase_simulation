from dataclasses import dataclass
from typing import List

from simulation.config import SimulationConfig


@dataclass
class Sector:
    name: str
    index: int
    ai_applicability: float  # 0-1, how amenable to AI automation
    base_wage: float
    base_productivity: float


# Default AI applicability by sector
_DEFAULT_AI_APPLICABILITY = {
    "Manufacturing": 0.7,
    "Services": 0.5,
    "Tech": 0.8,
    "Healthcare": 0.4,
    "Creative": 0.3,
}

_DEFAULT_BASE_WAGE = {
    "Manufacturing": 1.0,
    "Services": 0.8,
    "Tech": 1.4,
    "Healthcare": 1.2,
    "Creative": 0.9,
}

_DEFAULT_BASE_PRODUCTIVITY = {
    "Manufacturing": 1.0,
    "Services": 0.9,
    "Tech": 1.3,
    "Healthcare": 1.1,
    "Creative": 0.85,
}


def create_sectors(config: SimulationConfig) -> List[Sector]:
    sectors = []
    for i, name in enumerate(config.sector_names[: config.n_sectors]):
        sectors.append(
            Sector(
                name=name,
                index=i,
                ai_applicability=_DEFAULT_AI_APPLICABILITY.get(name, 0.5),
                base_wage=_DEFAULT_BASE_WAGE.get(name, 1.0),
                base_productivity=_DEFAULT_BASE_PRODUCTIVITY.get(name, 1.0),
            )
        )
    return sectors
