import streamlit as st

from simulation.config import SimulationConfig
from simulation.engine import SimulationEngine
from dashboard.controls import render_sidebar
from dashboard.layout import render_dashboard, render_theory_guide

st.set_page_config(
    page_title="Coase Theorem: AI Job Displacement",
    page_icon="⚖️",
    layout="wide",
)

st.title("Coase Theorem & AI Job Displacement Simulation")
st.caption(
    "Explore how transaction costs affect the efficiency of Coasian bargaining "
    "when workers hold the right to employment and firms must compensate to automate."
)

# Sidebar controls
config = render_sidebar()

# Scenario comparison
st.sidebar.divider()
st.sidebar.subheader("Scenario Comparison")
compare_mode = st.sidebar.checkbox(
    "Compare Mode",
    help="Save a simulation run, change parameters, and run again to overlay "
    "both results on the same charts. Essential for demonstrating the Coase Theorem — "
    "e.g., compare TC=0 vs TC=0.3 to see deadweight loss appear.",
)
compare_df = None
compare_label = ""

if compare_mode:
    if "saved_scenarios" not in st.session_state:
        st.session_state.saved_scenarios = {}

    save_name = st.sidebar.text_input("Save current as:", key="save_name")
    if st.sidebar.button("Save Scenario") and save_name:
        if "last_df" in st.session_state:
            st.session_state.saved_scenarios[save_name] = st.session_state.last_df.copy()
            st.sidebar.success(f"Saved '{save_name}'")

    saved = st.session_state.get("saved_scenarios", {})
    if saved:
        compare_label = st.sidebar.selectbox("Compare with:", list(saved.keys()))
        compare_df = saved.get(compare_label)

# Run simulation
st.sidebar.divider()
run = st.sidebar.button("Run Simulation", type="primary", use_container_width=True)

if run:
    engine = SimulationEngine(config)
    with st.spinner("Running simulation..."):
        engine.run()
    df = engine.results_dataframe()
    st.session_state.last_df = df
    st.session_state.last_engine = engine
    render_dashboard(engine, df, compare_df, compare_label)
elif "last_df" in st.session_state:
    render_dashboard(
        st.session_state.last_engine,
        st.session_state.last_df,
        compare_df,
        compare_label,
    )
else:
    st.info("Configure parameters in the sidebar and click **Run Simulation** to begin.")
    st.divider()
    st.subheader("Getting Started")
    st.markdown(
        "New here? Read the **Theory & Guide** below to understand the economic model, "
        "then try the **Suggested Experiments** to see the Coase Theorem in action. "
        "You can also select a **Preset Scenario** from the sidebar to get started quickly."
    )
    render_theory_guide()
