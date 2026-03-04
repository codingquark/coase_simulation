from typing import Optional

import streamlit as st
import pandas as pd

from simulation.engine import SimulationEngine
from simulation.config import SimulationConfig
from dashboard import charts
from dashboard.help_content import (
    TAB_OVERVIEW_INTRO,
    TAB_COASE_INTRO,
    TAB_SECTOR_INTRO,
    TAB_DISTRIBUTION_INTRO,
    THEORY_COASE,
    THEORY_MODEL,
    THEORY_PHASES,
    THEORY_SECTORS,
    THEORY_EXPERIMENTS,
    THEORY_GLOSSARY,
)


def render_kpi_cards(df: pd.DataFrame):
    last = df.iloc[-1]
    cols = st.columns(4)
    cols[0].metric("Employment Rate", f"{last['employment_rate']:.1%}")
    cols[1].metric("Mean Wage", f"{last['mean_wage']:.2f}")
    cols[2].metric(
        "Displaced Workers",
        f"{last['displacement_rate']:.1%}",
    )
    cols[3].metric("Blocked Transactions", f"{int(last['blocked_transactions'])}")


def render_overview(df: pd.DataFrame, compare_df: Optional[pd.DataFrame], compare_label: str):
    st.caption(TAB_OVERVIEW_INTRO)
    render_kpi_cards(df)
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            charts.employment_chart(df, compare_df, compare_label), use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            charts.wage_chart(df, compare_df, compare_label), use_container_width=True,
        )
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(charts.ai_automation_chart(df), use_container_width=True)
    with c4:
        st.plotly_chart(charts.displacement_jobs_chart(df), use_container_width=True)


def render_coase_analysis(
    df: pd.DataFrame, compare_df: Optional[pd.DataFrame], compare_label: str,
):
    with st.expander("About this tab", expanded=False):
        st.markdown(TAB_COASE_INTRO)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            charts.surplus_allocation_chart(df, compare_df, compare_label),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            charts.blocked_transactions_chart(df, compare_df, compare_label),
            use_container_width=True,
        )
    st.plotly_chart(
        charts.total_surplus_chart(df, compare_df, compare_label), use_container_width=True,
    )

    # Summary stats
    total_surplus = df["total_surplus"].sum()
    total_worker = df["worker_compensation"].sum()
    total_firm = df["firm_gain"].sum()
    total_dw = df["deadweight_loss"].sum()
    total_blocked = df["blocked_transactions"].sum()

    st.subheader("Cumulative Surplus Allocation")
    cols = st.columns(4)
    cols[0].metric("Total Surplus", f"{total_surplus:.1f}")
    cols[1].metric("Worker Compensation", f"{total_worker:.1f}")
    cols[2].metric("Firm Gain", f"{total_firm:.1f}")
    cols[3].metric("Deadweight Loss", f"{total_dw:.1f}")

    if total_surplus > 0:
        st.caption(
            f"Worker share: {total_worker / (total_worker + total_firm) * 100:.1f}% | "
            f"Firm share: {total_firm / (total_worker + total_firm) * 100:.1f}% | "
            f"Total blocked: {int(total_blocked)}"
            if (total_worker + total_firm) > 0
            else "No completed transactions."
        )


def render_sector_dynamics(df: pd.DataFrame, sector_names: list):
    st.caption(TAB_SECTOR_INTRO)
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            charts.sector_employment_chart(df, sector_names), use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            charts.sector_automation_chart(df, sector_names), use_container_width=True,
        )
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(
            charts.sector_wage_chart(df, sector_names), use_container_width=True,
        )
    with c4:
        st.plotly_chart(charts.retraining_chart(df), use_container_width=True)


def render_distribution(engine: SimulationEngine, df: pd.DataFrame):
    st.caption(TAB_DISTRIBUTION_INTRO)
    period = st.slider(
        "Select Period", 0, len(df) - 1, len(df) - 1,
        help="View worker distributions at a specific period. "
        "Move left to see earlier snapshots and watch polarization emerge.",
    )

    # We show current snapshot (end of simulation) for the scatter
    workers = engine.workers
    sector_names = [s.name for s in engine.sectors]

    employed = [w for w in workers if w.employed]
    if employed:
        wages = [w.wage for w in employed]
        skills = [w.skill for w in employed]
        sectors = [sector_names[w.sector] for w in employed]

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(charts.wage_histogram(wages, sectors), use_container_width=True)
        with c2:
            st.plotly_chart(
                charts.skill_wage_scatter(skills, wages, sectors), use_container_width=True,
            )
    else:
        st.info("No employed workers at this point in the simulation.")


def render_theory_guide():
    """Render the Theory & Guide tab with full documentation."""
    st.markdown(THEORY_COASE)
    st.divider()
    st.markdown(THEORY_MODEL)
    st.divider()
    st.markdown(THEORY_PHASES)
    st.divider()
    st.markdown(THEORY_SECTORS)
    st.divider()
    st.markdown(THEORY_EXPERIMENTS)
    st.divider()
    st.markdown(THEORY_GLOSSARY)


def render_dashboard(
    engine: SimulationEngine,
    df: pd.DataFrame,
    compare_df: Optional[pd.DataFrame] = None,
    compare_label: str = "",
):
    sector_names = [s.name for s in engine.sectors]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview",
        "Coase Analysis",
        "Sector Dynamics",
        "Distribution",
        "Theory & Guide",
    ])

    with tab1:
        render_overview(df, compare_df, compare_label)
    with tab2:
        render_coase_analysis(df, compare_df, compare_label)
    with tab3:
        render_sector_dynamics(df, sector_names)
    with tab4:
        render_distribution(engine, df)
    with tab5:
        render_theory_guide()
