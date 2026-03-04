from dataclasses import dataclass, field
from typing import List

import numpy as np

from simulation.config import SimulationConfig
from simulation.sectors import Sector


@dataclass
class Worker:
    id: int
    sector: int
    skill: float  # 0-1
    employed: bool = True
    wage: float = 1.0
    reservation_wage: float = 0.5
    bargaining_power: float = 0.5
    retraining_timer: int = 0
    displaced: bool = False
    compensation_received: float = 0.0


@dataclass
class Firm:
    id: int
    sector: int
    n_workers: int = 20
    automation_level: float = 0.0
    ai_capability: float = 0.0
    worker_ids: List[int] = field(default_factory=list)


def create_workers(
    config: SimulationConfig, sectors: List[Sector], rng: np.random.Generator
) -> List[Worker]:
    workers = []
    sector_indices = list(range(len(sectors)))
    for i in range(config.n_workers):
        sec = rng.choice(sector_indices)
        skill = rng.beta(2, 2)  # centered around 0.5
        base_wage = sectors[sec].base_wage
        wage = base_wage * (0.5 + skill)
        reservation_wage = wage * 0.6
        workers.append(
            Worker(
                id=i,
                sector=sec,
                skill=skill,
                wage=wage,
                reservation_wage=reservation_wage,
                bargaining_power=config.worker_bargaining_power,
            )
        )
    return workers


def create_firms(
    config: SimulationConfig,
    sectors: List[Sector],
    workers: List[Worker],
    rng: np.random.Generator,
) -> List[Firm]:
    firms = []
    workers_per_firm = config.n_workers // config.n_firms

    # Group workers by sector
    sector_workers = {i: [] for i in range(len(sectors))}
    for w in workers:
        sector_workers[w.sector].append(w.id)

    # Distribute firms across sectors
    firm_id = 0
    for sec_idx in range(len(sectors)):
        n_firms_in_sector = max(1, config.n_firms // len(sectors))
        sec_worker_list = sector_workers[sec_idx]
        rng.shuffle(sec_worker_list)

        chunk_size = max(1, len(sec_worker_list) // n_firms_in_sector)
        for j in range(n_firms_in_sector):
            if firm_id >= config.n_firms:
                break
            start = j * chunk_size
            end = start + chunk_size if j < n_firms_in_sector - 1 else len(sec_worker_list)
            assigned = sec_worker_list[start:end]
            firms.append(
                Firm(
                    id=firm_id,
                    sector=sec_idx,
                    n_workers=len(assigned),
                    worker_ids=list(assigned),
                )
            )
            firm_id += 1

    # Assign remaining workers to existing firms if firm count was reached early
    assigned_ids = {wid for f in firms for wid in f.worker_ids}
    unassigned = [w.id for w in workers if w.id not in assigned_ids]
    for wid in unassigned:
        f = firms[rng.integers(0, len(firms))]
        f.worker_ids.append(wid)
        f.n_workers += 1

    return firms
