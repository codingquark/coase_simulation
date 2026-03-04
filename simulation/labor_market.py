from typing import List, Tuple

import numpy as np

from simulation.agents import Worker, Firm
from simulation.sectors import Sector
from simulation.config import SimulationConfig


def matching_function(
    unemployed: int,
    vacancies: int,
    efficiency: float,
    elasticity: float = 0.5,
) -> int:
    """Cobb-Douglas matching function.

    M = efficiency * U^mu * V^(1-mu)
    """
    if unemployed <= 0 or vacancies <= 0:
        return 0
    matches = efficiency * (unemployed ** elasticity) * (vacancies ** (1.0 - elasticity))
    return int(min(matches, unemployed, vacancies))


def determine_wage(
    worker_skill: float,
    sector_base_wage: float,
    sector_productivity: float,
    labor_share: float,
    monopsony_markdown: float,
) -> float:
    """Wage = marginal product × (1 - monopsony markdown)."""
    marginal_product = sector_productivity * (0.5 + worker_skill) * labor_share
    return marginal_product * (1.0 - monopsony_markdown) * sector_base_wage


def create_new_jobs(
    automation_level: float,
    innovation_rate: float,
    job_creation_multiplier: float,
    base_job_creation: float,
) -> int:
    """New jobs created from automation-driven innovation."""
    new_jobs = base_job_creation + job_creation_multiplier * automation_level * innovation_rate * 100
    return max(0, int(new_jobs))


def clear_labor_market(
    workers: List[Worker],
    firms: List[Firm],
    sectors: List[Sector],
    config: SimulationConfig,
    rng: np.random.Generator,
    total_automation_level: float,
) -> Tuple[int, int]:
    """Run labor market clearing: match unemployed workers to vacancies, set wages.

    Returns (matches_made, new_jobs_created).
    """
    unemployed = [w for w in workers if not w.employed and w.retraining_timer <= 0]
    employed_count = sum(1 for w in workers if w.employed)

    # Compute vacancies from job creation
    n_new_jobs = create_new_jobs(
        automation_level=total_automation_level,
        innovation_rate=config.innovation_rate,
        job_creation_multiplier=config.job_creation_multiplier,
        base_job_creation=config.base_job_creation,
    )

    # Base vacancies from turnover + new jobs
    vacancies = int(len(workers) * config.vacancy_rate) + n_new_jobs

    matches = matching_function(
        unemployed=len(unemployed),
        vacancies=vacancies,
        efficiency=config.matching_efficiency,
    )

    # Match workers (prioritize higher-skilled)
    unemployed_sorted = sorted(unemployed, key=lambda w: w.skill, reverse=True)
    matched_count = 0
    for w in unemployed_sorted[:matches]:
        sector = sectors[w.sector]
        w.employed = True
        w.displaced = False
        w.wage = determine_wage(
            worker_skill=w.skill,
            sector_base_wage=sector.base_wage,
            sector_productivity=sector.base_productivity,
            labor_share=config.labor_share,
            monopsony_markdown=config.monopsony_markdown,
        )
        # Assign to a firm in the same sector
        sector_firms = [f for f in firms if f.sector == w.sector]
        if sector_firms:
            firm = sector_firms[rng.integers(0, len(sector_firms))]
            firm.worker_ids.append(w.id)
            firm.n_workers += 1
        matched_count += 1

    # Update wages for employed workers (small adjustment toward equilibrium)
    for w in workers:
        if w.employed:
            sector = sectors[w.sector]
            eq_wage = determine_wage(
                worker_skill=w.skill,
                sector_base_wage=sector.base_wage,
                sector_productivity=sector.base_productivity,
                labor_share=config.labor_share,
                monopsony_markdown=config.monopsony_markdown,
            )
            w.wage = w.wage * 0.9 + eq_wage * 0.1  # gradual convergence

    return matched_count, n_new_jobs
