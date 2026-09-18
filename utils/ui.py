"""
UI Components and Theming Helpers for Mining Production Dashboard
Provides consistent header banners, KPI widgets, styling, and Plotly theme formatters.
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import os

# Primary Brand Color Palette
PRIMARY_COLOR = "#0F766E"       # Teal
SECONDARY_COLOR = "#0D9488"     # Medium Teal
ACCENT_COLOR = "#0EA5E9"        # Sky Blue
WARNING_COLOR = "#F59E0B"       # Amber
DANGER_COLOR = "#EF4444"        # Crimson
SUCCESS_COLOR = "#10B981"       # Emerald
DARK_TEXT = "#1F2937"
MUTED_TEXT = "#6B7280"
CARD_BG = "#FFFFFF"

PALETTE = [
    "#0F766E", "#0EA5E9", "#F59E0B", "#10B981", "#6366F1",
    "#EC4899", "#8B5CF6", "#14B8A6", "#F97316", "#64748B"
]


def inject_custom_css():
    """Injects lightweight shared styling to polish typography and containers."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, .kpi-title {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600;
        color: #0F766E;
    }
    
    /* Sleek card container */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.2rem 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15, 118, 110, 0.10);
    }
    .metric-card .label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #4B5563;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    .metric-card .value {
        font-size: 1.9rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        color: #0F766E;
    }
    .metric-card .sub {
        font-size: 0.8rem;
        color: #6B7280;
        margin-top: 0.25rem;
    }
    
    /* Empty state alert */
    .empty-state {
        background: #F0FDF4;
        border: 1px dashed #0F766E;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        color: #115E59;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = "Module Reporting & Performance", icon: str = "⛏️"):
    """Renders a consistent, polished top hero header."""
    inject_custom_css()
    now_str = datetime.now().strftime("%A %d %B %Y, %H:%M")
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
        color: white;
        padding: 1.75rem 1.5rem;
        border-radius: 14px;
        margin-bottom: 1.75rem;
        box-shadow: 0 4px 15px rgba(15, 118, 110, 0.2);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.85; font-weight: 500;">
                    Phosboucraa — Production Minière
                </div>
                <div style="font-size: 2rem; font-weight: 700; font-family: 'Poppins', sans-serif; margin-top: 0.2rem;">
                    {icon} {title}
                </div>
                <div style="font-size: 1rem; opacity: 0.9; margin-top: 0.2rem;">
                    {subtitle}
                </div>
            </div>
            <div style="text-align: right; background: rgba(255,255,255,0.12); padding: 0.6rem 1rem; border-radius: 8px; backdrop-filter: blur(4px);">
                <div style="font-size: 0.75rem; opacity: 0.8;">Date et heure</div>
                <div style="font-size: 0.95rem; font-weight: 600;">{now_str}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi(label: str, value: str, subtext: str = "", color: str = PRIMARY_COLOR):
    """Renders a styled HTML KPI card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value" style="color: {color};">{value}</div>
        {f'<div class="sub">{subtext}</div>' if subtext else ''}
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(message: str = "Aucune donnée ne correspond aux filtres sélectionnés."):
    """Displays a clean empty state card."""
    st.markdown(f"""
    <div class="empty-state">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
        <div style="font-size: 1.1rem; font-weight: 600;">Aucun résultat</div>
        <div style="font-size: 0.9rem; opacity: 0.85; margin-top: 0.25rem;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


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
            font=dict(family="Poppins, sans-serif", size=15, color=DARK_TEXT),
            x=0.01,
            y=0.96
        ),
        template="plotly_white",
        colorway=PALETTE,
        height=height,
        margin=dict(l=30, r=30, t=50 if title else 20, b=30),
        font=dict(family="Inter, sans-serif", color=DARK_TEXT, size=12),
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
