import streamlit as st

from simulation.config import SimulationConfig
from dashboard.scenarios import get_preset_names, get_preset
from dashboard.help_content import (
    HELP_AI_CAP_MAX,
    HELP_AI_GROWTH_RATE,
    HELP_AI_INFLECTION,
    HELP_INNOVATION_RATE,
    HELP_TRANSACTION_COST,
    HELP_INFO_ASYMMETRY,
    HELP_LEGAL_FRICTION,
    HELP_COORDINATION_COST,
    HELP_BARGAINING_POWER,
    HELP_N_WORKERS,
    HELP_N_FIRMS,
    HELP_MATCHING_EFFICIENCY,
    HELP_RETRAINING_DURATION,
    HELP_LABOR_SHARE,
    HELP_MONOPSONY,
    HELP_JOB_CREATION_MULT,
    HELP_N_PERIODS,
    HELP_RANDOM_SEED,
    SCENARIO_DESCRIPTIONS,
)


def render_sidebar() -> SimulationConfig:
    """Render the sidebar controls and return a SimulationConfig."""
    st.sidebar.header("Simulation Parameters")

    # Preset selector
    preset_name = st.sidebar.selectbox(
        "Preset Scenario",
        get_preset_names(),
        help="Choose a preset to auto-fill parameters, or select Custom to set your own.",
    )
    preset = get_preset(preset_name)

    # Show scenario description
    if preset_name in SCENARIO_DESCRIPTIONS:
        st.sidebar.info(SCENARIO_DESCRIPTIONS[preset_name])

    # AI Technology
    with st.sidebar.expander("AI Technology", expanded=False):
        st.caption(
            "Controls how AI capability evolves over time. "
            "The logistic S-curve models gradual progress followed by rapid improvement."
        )
        ai_cap_max = st.slider(
            "Max AI Capability", 0.0, 2.0, preset.ai_cap_max, 0.05, help=HELP_AI_CAP_MAX,
        )
        ai_growth_rate = st.slider(
            "AI Growth Rate", 0.01, 0.5, preset.ai_growth_rate, 0.01, help=HELP_AI_GROWTH_RATE,
        )
        ai_inflection = st.slider(
            "AI Inflection Point", 10, 150, int(preset.ai_inflection_point),
            help=HELP_AI_INFLECTION,
        )
        innovation_rate = st.slider(
            "Innovation Rate", 0.0, 0.1, preset.innovation_rate, 0.005,
            help=HELP_INNOVATION_RATE,
        )

    # Coase / Bargaining
    with st.sidebar.expander("Coase / Bargaining", expanded=True):
        st.caption(
            "The core parameters of the Coase Theorem experiment. "
            "Transaction costs determine whether efficient bargaining occurs."
        )
        transaction_cost = st.slider(
            "Transaction Cost", 0.0, 1.0, preset.transaction_cost, 0.01,
            help=HELP_TRANSACTION_COST,
        )
        info_asymmetry = st.slider(
            "Info Asymmetry", 0.0, 1.0, preset.info_asymmetry, 0.05,
            help=HELP_INFO_ASYMMETRY,
        )
        legal_friction = st.slider(
            "Legal Friction", 0.0, 1.0, preset.legal_friction, 0.05,
            help=HELP_LEGAL_FRICTION,
        )
        coordination_cost = st.slider(
            "Coordination Cost", 0.0, 0.5, preset.coordination_cost, 0.01,
            help=HELP_COORDINATION_COST,
        )
        bargaining_power = st.slider(
            "Worker Bargaining Power (\u03b2)", 0.0, 1.0, preset.worker_bargaining_power, 0.05,
            help=HELP_BARGAINING_POWER,
        )

    # Labor Market
    with st.sidebar.expander("Labor Market", expanded=False):
        st.caption(
            "Structure of the labor market: how many agents, how fast matching occurs, "
            "and how long retraining takes."
        )
        n_workers = st.slider(
            "Workers", 50, 5000, preset.n_workers, 50, help=HELP_N_WORKERS,
        )
        n_firms = st.slider(
            "Firms", 5, 200, preset.n_firms, 5, help=HELP_N_FIRMS,
        )
        matching_eff = st.slider(
            "Matching Efficiency", 0.05, 1.0, preset.matching_efficiency, 0.05,
            help=HELP_MATCHING_EFFICIENCY,
        )
        retrain_dur = st.slider(
            "Retraining Duration", 1, 20, preset.retraining_duration,
            help=HELP_RETRAINING_DURATION,
        )

    # Production
    with st.sidebar.expander("Production", expanded=False):
        st.caption(
            "How output and wages are determined. These parameters shape "
            "the baseline economy before automation begins."
        )
        labor_share = st.slider(
            "Labor Share (\u03b1)", 0.1, 0.9, preset.labor_share, 0.05, help=HELP_LABOR_SHARE,
        )
        monopsony = st.slider(
            "Monopsony Markdown", 0.0, 0.5, preset.monopsony_markdown, 0.05,
            help=HELP_MONOPSONY,
        )
        job_mult = st.slider(
            "Job Creation Multiplier", 0.0, 0.5, preset.job_creation_multiplier, 0.01,
            help=HELP_JOB_CREATION_MULT,
        )

    # Simulation
    with st.sidebar.expander("Simulation", expanded=False):
        st.caption("General simulation settings.")
        n_periods = st.slider(
            "Periods", 20, 500, preset.n_periods, 10, help=HELP_N_PERIODS,
        )
        seed = st.number_input(
            "Random Seed", value=preset.random_seed, min_value=0, step=1,
            help=HELP_RANDOM_SEED,
        )

    return SimulationConfig(
        ai_cap_max=ai_cap_max,
        ai_growth_rate=ai_growth_rate,
        ai_inflection_point=float(ai_inflection),
        innovation_rate=innovation_rate,
        transaction_cost=transaction_cost,
        info_asymmetry=info_asymmetry,
        legal_friction=legal_friction,
        coordination_cost=coordination_cost,
        worker_bargaining_power=bargaining_power,
        n_workers=n_workers,
        n_firms=n_firms,
        matching_efficiency=matching_eff,
        retraining_duration=retrain_dur,
        labor_share=labor_share,
        monopsony_markdown=monopsony,
        job_creation_multiplier=job_mult,
        n_periods=n_periods,
        random_seed=int(seed),
    )
