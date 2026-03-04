from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def _overlay_layout(fig: go.Figure, title: str, yaxis_title: str = "") -> go.Figure:
    fig.update_layout(
        title=title,
        xaxis_title="Period",
        yaxis_title=yaxis_title,
        template="plotly_white",
        height=350,
        margin=dict(l=40, r=20, t=40, b=30),
    )
    return fig


def employment_chart(
    df: pd.DataFrame, compare_df: Optional[pd.DataFrame] = None, compare_label: str = ""
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["employment_rate"],
        mode="lines", name="Employment Rate", line=dict(color="#2563eb"),
    ))
    if compare_df is not None:
        fig.add_trace(go.Scatter(
            x=compare_df["period"], y=compare_df["employment_rate"],
            mode="lines", name=f"Employment ({compare_label})",
            line=dict(color="#dc2626", dash="dash"),
        ))
    return _overlay_layout(fig, "Employment Rate", "Rate")


def wage_chart(
    df: pd.DataFrame, compare_df: Optional[pd.DataFrame] = None, compare_label: str = ""
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["mean_wage"],
        mode="lines", name="Mean Wage", line=dict(color="#2563eb"),
    ))
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["median_wage"],
        mode="lines", name="Median Wage", line=dict(color="#16a34a"),
    ))
    if compare_df is not None:
        fig.add_trace(go.Scatter(
            x=compare_df["period"], y=compare_df["mean_wage"],
            mode="lines", name=f"Mean Wage ({compare_label})",
            line=dict(color="#dc2626", dash="dash"),
        ))
    return _overlay_layout(fig, "Wages Over Time", "Wage")


def ai_automation_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["ai_capability"],
        mode="lines", name="AI Capability", line=dict(color="#7c3aed"),
    ))
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["total_automation"],
        mode="lines", name="Automation Level", line=dict(color="#ea580c"),
    ))
    return _overlay_layout(fig, "AI Capability vs Automation", "Level")


def displacement_jobs_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["displacement_rate"],
        mode="lines", name="Displacement Rate", line=dict(color="#dc2626"),
    ))
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["new_jobs"],
        mode="lines", name="New Jobs", yaxis="y2", line=dict(color="#16a34a"),
    ))
    fig.update_layout(
        title="Displacement vs Job Creation",
        xaxis_title="Period",
        yaxis=dict(title="Displacement Rate"),
        yaxis2=dict(title="New Jobs", overlaying="y", side="right"),
        template="plotly_white",
        height=350,
        margin=dict(l=40, r=40, t=40, b=30),
    )
    return fig


# --- Coase Analysis ---

def surplus_allocation_chart(
    df: pd.DataFrame, compare_df: Optional[pd.DataFrame] = None, compare_label: str = ""
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["worker_compensation"],
        mode="lines", stackgroup="one", name="Worker Compensation",
        line=dict(color="#2563eb"),
    ))
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["firm_gain"],
        mode="lines", stackgroup="one", name="Firm Gain",
        line=dict(color="#16a34a"),
    ))
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["deadweight_loss"],
        mode="lines", stackgroup="one", name="Deadweight Loss",
        line=dict(color="#dc2626"),
    ))
    if compare_df is not None:
        fig.add_trace(go.Scatter(
            x=compare_df["period"], y=compare_df["total_surplus"],
            mode="lines", name=f"Total Surplus ({compare_label})",
            line=dict(color="#000", dash="dash"),
        ))
    return _overlay_layout(fig, "Surplus Allocation", "Value")


def blocked_transactions_chart(
    df: pd.DataFrame, compare_df: Optional[pd.DataFrame] = None, compare_label: str = ""
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["blocked_transactions"],
        mode="lines", name="Blocked Transactions", line=dict(color="#dc2626"),
    ))
    if compare_df is not None:
        fig.add_trace(go.Scatter(
            x=compare_df["period"], y=compare_df["blocked_transactions"],
            mode="lines", name=f"Blocked ({compare_label})",
            line=dict(color="#f97316", dash="dash"),
        ))
    return _overlay_layout(fig, "Blocked Transactions (Deadweight Loss)", "Count")


def total_surplus_chart(
    df: pd.DataFrame, compare_df: Optional[pd.DataFrame] = None, compare_label: str = ""
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["total_surplus"],
        mode="lines", name="Total Surplus", line=dict(color="#7c3aed"),
    ))
    if compare_df is not None:
        fig.add_trace(go.Scatter(
            x=compare_df["period"], y=compare_df["total_surplus"],
            mode="lines", name=f"Total Surplus ({compare_label})",
            line=dict(color="#dc2626", dash="dash"),
        ))
    return _overlay_layout(fig, "Total Surplus Over Time", "Surplus")


# --- Sector Dynamics ---

def sector_employment_chart(df: pd.DataFrame, sector_names: List[str]) -> go.Figure:
    fig = go.Figure()
    colors = px.colors.qualitative.Set2
    for i, name in enumerate(sector_names):
        col = f"emp_{name}"
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df["period"], y=df[col],
                mode="lines", stackgroup="one", name=name,
                line=dict(color=colors[i % len(colors)]),
            ))
    return _overlay_layout(fig, "Sector Employment Rates", "Employment Rate")


def sector_automation_chart(df: pd.DataFrame, sector_names: List[str]) -> go.Figure:
    fig = go.Figure()
    colors = px.colors.qualitative.Set2
    for i, name in enumerate(sector_names):
        col = f"auto_{name}"
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df["period"], y=df[col],
                mode="lines", name=name,
                line=dict(color=colors[i % len(colors)]),
            ))
    return _overlay_layout(fig, "Automation Level by Sector", "Automation Level")


def sector_wage_chart(df: pd.DataFrame, sector_names: List[str]) -> go.Figure:
    fig = go.Figure()
    colors = px.colors.qualitative.Set2
    for i, name in enumerate(sector_names):
        col = f"wage_{name}"
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df["period"], y=df[col],
                mode="lines", name=name,
                line=dict(color=colors[i % len(colors)]),
            ))
    return _overlay_layout(fig, "Average Wage by Sector", "Wage")


def retraining_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["retraining_pool"],
        mode="lines", name="Retraining Pool", fill="tozeroy",
        line=dict(color="#f59e0b"),
    ))
    return _overlay_layout(fig, "Workers in Retraining", "Count")


# --- Distribution ---

def wage_histogram(wages: List[float], sectors: List[str]) -> go.Figure:
    df = pd.DataFrame({"wage": wages, "sector": sectors})
    fig = px.histogram(
        df, x="wage", color="sector", nbins=30,
        title="Wage Distribution",
        template="plotly_white",
    )
    fig.update_layout(height=400, margin=dict(l=40, r=20, t=40, b=30))
    return fig


def skill_wage_scatter(skills: List[float], wages: List[float], sectors: List[str]) -> go.Figure:
    df = pd.DataFrame({"skill": skills, "wage": wages, "sector": sectors})
    fig = px.scatter(
        df, x="skill", y="wage", color="sector",
        title="Worker Skill vs Wage",
        template="plotly_white",
        opacity=0.6,
    )
    fig.update_layout(height=400, margin=dict(l=40, r=20, t=40, b=30))
    return fig
