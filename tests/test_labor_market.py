import pytest
import numpy as np

from simulation.labor_market import (
    matching_function,
    determine_wage,
    create_new_jobs,
)


class TestMatchingFunction:
    def test_positive_matches(self):
        m = matching_function(unemployed=100, vacancies=50, efficiency=0.3)
        assert m > 0
        assert m <= 50  # can't exceed min(U, V)

    def test_no_unemployed(self):
        assert matching_function(unemployed=0, vacancies=50, efficiency=0.3) == 0

    def test_no_vacancies(self):
        assert matching_function(unemployed=100, vacancies=0, efficiency=0.3) == 0

    def test_higher_efficiency_more_matches(self):
        low = matching_function(unemployed=100, vacancies=50, efficiency=0.1)
        high = matching_function(unemployed=100, vacancies=50, efficiency=0.5)
        assert high >= low

    def test_more_unemployed_more_matches(self):
        low = matching_function(unemployed=10, vacancies=50, efficiency=0.3)
        high = matching_function(unemployed=200, vacancies=50, efficiency=0.3)
        assert high >= low


class TestDetermineWage:
    def test_basic_wage(self):
        wage = determine_wage(
            worker_skill=0.5,
            sector_base_wage=1.0,
            sector_productivity=1.0,
            labor_share=0.65,
            monopsony_markdown=0.1,
        )
        # marginal_product = 1.0 * (0.5+0.5) * 0.65 = 0.65
        # wage = 0.65 * 0.9 * 1.0 = 0.585
        assert pytest.approx(wage, abs=0.01) == 0.585

    def test_higher_skill_higher_wage(self):
        low = determine_wage(0.2, 1.0, 1.0, 0.65, 0.1)
        high = determine_wage(0.8, 1.0, 1.0, 0.65, 0.1)
        assert high > low

    def test_no_monopsony(self):
        with_markdown = determine_wage(0.5, 1.0, 1.0, 0.65, 0.2)
        without = determine_wage(0.5, 1.0, 1.0, 0.65, 0.0)
        assert without > with_markdown


class TestCreateNewJobs:
    def test_base_jobs(self):
        jobs = create_new_jobs(
            automation_level=0.0, innovation_rate=0.02,
            job_creation_multiplier=0.1, base_job_creation=5.0,
        )
        assert jobs == 5

    def test_more_automation_more_jobs(self):
        low = create_new_jobs(0.1, 0.02, 0.1, 5.0)
        high = create_new_jobs(0.9, 0.02, 0.1, 5.0)
        assert high >= low

    def test_zero_multiplier(self):
        jobs = create_new_jobs(0.5, 0.02, 0.0, 5.0)
        assert jobs == 5  # only base
