"""
UI Components and Theming Helpers for Mining Production Dashboard
Provides native Streamlit components, KPI cards, and Plotly theme formatters.
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Primary Brand Color Palette
PRIMARY_COLOR = "#0F766E"       # Teal
SECONDARY_COLOR = "#0D9488"     # Medium Teal
ACCENT_COLOR = "#0EA5E9"        # Sky Blue
WARNING_COLOR = "#F59E0B"       # Amber
DANGER_COLOR = "#EF4444"        # Crimson
SUCCESS_COLOR = "#10B981"       # Emerald
DARK_TEXT = "#1F2937"

PALETTE = [
    "#0F766E", "#0EA5E9", "#F59E0B", "#10B981", "#6366F1",
    "#EC4899", "#8B5CF6", "#14B8A6", "#F97316", "#64748B"
]


def render_header(title: str, subtitle: str = "Module Reporting & Performance", icon: str = "⛏️"):
    """Renders a clean, robust native Streamlit hero header."""
    now_str = datetime.now().strftime("%A %d %B %Y, %H:%M")
    
    col_t, col_d = st.columns([8, 4])
    with col_t:
        st.title(f"{icon} {title}")
        st.caption(f"**Phosboucraa — Gestion de la Production Minière** | {subtitle}")
    with col_d:
        st.info(f"🕒 **Date & Heure :** {now_str}")


def render_kpi(label: str, value: str, subtext: str = "", color: str = PRIMARY_COLOR, delta: str = None):
    """Renders a native Streamlit metric card inside a styled border container."""
    with st.container(border=True):
        st.metric(
            label=label,
            value=value,
            delta=delta,
            help=subtext if subtext else None
        )
        if subtext:
            st.caption(subtext)


def render_empty_state(message: str = "Aucune donnée ne correspond aux filtres sélectionnés."):
    """Displays a native Streamlit empty state alert."""
    st.info(f"🔍 **Aucun résultat :** {message}")


def style_plotly_fig(
    fig: go.Figure,
    title: str = "",
    height: int = 400,
    show_legend: bool = True
) -> go.Figure:
    """Applies standardized typography, colors, and layout to any Plotly chart."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="sans-serif", size=15, color=DARK_TEXT),
            x=0.01,
            y=0.96
        ),
        template="plotly_white",
        colorway=PALETTE,
        height=height,
        margin=dict(l=30, r=30, t=50 if title else 20, b=30),
        font=dict(family="sans-serif", color=DARK_TEXT, size=12),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#F3F4F6",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F3F4F6",
            zeroline=False
        )
    )
    return fig
