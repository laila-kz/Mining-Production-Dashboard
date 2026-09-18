"""
Accueil / Executive Dashboard — Système de Gestion de la Production Minière (Phosboucraa)
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.ui import render_header, render_kpi, style_plotly_fig, PRIMARY_COLOR, ACCENT_COLOR, WARNING_COLOR, SUCCESS_COLOR
from utils.queries import get_global_kpis, get_daily_production_trend, get_voyages_detailed, get_qualite_dataset

# 1. Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="Phosboucraa — Gestion Minière",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Hero Header
render_header(
    title="Tableau de Bord Exécutif",
    subtitle="Supervision Globale de la Production Minière & Performance Opérationnelle",
    icon="⛏️"
)

# 3. Quick Navigation Hub
st.markdown("### 🧭 Accès Rapide aux Modules")
nav_cols = st.columns(5)
dashboards = [
    {"label": "🚛 Suivi des Voyages", "path": "pages/1_Voyages.py", "desc": "Trajets & cadences"},
    {"label": "🧪 Contrôle Qualité", "path": "pages/2_Qualite.py", "desc": "Teneur & humidité"},
    {"label": "🚚 Flotte Camions", "path": "pages/3_Performance_Camions.py", "desc": "Rendement & TRS"},
    {"label": "👨‍💼 Conducteurs", "path": "pages/4_Performance_Conducteurs.py", "desc": "Productivité & sécurité"},
    {"label": "🛑 Suivi des Arrêts", "path": "pages/5_Arrets_Camions.py", "desc": "Pannes & MTTR"},
]

for idx, dash in enumerate(dashboards):
    with nav_cols[idx]:
        if st.button(dash["label"], key=f"nav_btn_{idx}", use_container_width=True):
            st.switch_page(dash["path"])
        st.caption(dash["desc"])

st.markdown("---")

# 4. Global KPIs Section
kpis = get_global_kpis()

st.markdown("### 📊 Indicateurs Clés de Performance (KPIs)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi("Production Totale", f"{kpis['total_tonnage']:,.0f} T", "Tonnage extrait & transporté", PRIMARY_COLOR)
with col2:
    render_kpi("Voyages Réalisés", f"{int(kpis['total_voyages']):,}", f"Moyenne: {kpis['avg_distance']:.1f} km / voyage", ACCENT_COLOR)
with col3:
    render_kpi("Temps d'Arrêt Total", f"{kpis['total_arret_hours']:.1f} h", "Cumul arrêts & maintenance", WARNING_COLOR)
with col4:
    render_kpi("Teneur Moyenne P₂O₅", f"{kpis['avg_phosphate']:.2f} %", f"Humidité moy: {kpis['avg_humidite']:.2f} %", SUCCESS_COLOR)

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)
with col5:
    render_kpi("Flotte Camions Active", f"{int(kpis['active_camions'])} unités", "Camions en service", PRIMARY_COLOR)
with col6:
    render_kpi("Effectif Conducteurs", f"{int(kpis['active_conducteurs'])} chauffeurs", "Conducteurs mobilisés", ACCENT_COLOR)
with col7:
    avg_load = (kpis['total_tonnage'] / kpis['total_voyages']) if kpis['total_voyages'] > 0 else 0
    render_kpi("Charge Moyenne / Trajet", f"{avg_load:.1f} T", "Taux de remplissage optimal", SUCCESS_COLOR)
with col8:
    render_kpi("Statut Opérationnel", "Actif", "Périmètre Minier Phosboucraa", PRIMARY_COLOR)

st.markdown("---")

# 5. Production Visualizations & Analytics
c_left, c_right = st.columns([7, 5])

with c_left:
    st.markdown("#### 📈 Évolution Journalière de la Production (Tonnage & Voyages)")
    trend_df = get_daily_production_trend()
    if not trend_df.empty:
        fig_trend = go.Figure()
        # Bar chart for tonnage
        fig_trend.add_trace(go.Bar(
            x=trend_df["date"],
            y=trend_df["total_tonnage"],
            name="Tonnage (T)",
            marker_color="#0F766E",
            opacity=0.85
        ))
        # Line chart for number of trips
        fig_trend.add_trace(go.Scatter(
            x=trend_df["date"],
            y=trend_df["nb_voyages"],
            name="Nombre de Voyages",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="#F59E0B", width=3),
            marker=dict(size=6)
        ))
        fig_trend.update_layout(
            yaxis=dict(title="Tonnage (T)"),
            yaxis2=dict(
                title="Nombre de Voyages",
                overlaying="y",
                side="right",
                showgrid=False
            )
        )
        st.plotly_chart(style_plotly_fig(fig_trend, height=380), use_container_width=True)
    else:
        st.info("Données d'activité récentes indisponibles.")

with c_right:
    st.markdown("#### 🏭 Répartition de la Production par Site Minier")
    voyages_all = get_voyages_detailed()
    if not voyages_all.empty and "site_nom" in voyages_all.columns:
        site_agg = voyages_all.groupby("site_nom")["quantite_transporte"].sum().reset_index()
        fig_site = px.pie(
            site_agg,
            values="quantite_transporte",
            names="site_nom",
            hole=0.45,
            color_discrete_sequence=["#0F766E", "#0EA5E9", "#10B981", "#F59E0B", "#6366F1"]
        )
        fig_site.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(style_plotly_fig(fig_site, height=380, show_legend=False), use_container_width=True)
    else:
        st.info("Données des sites indisponibles.")

# 6. Recent Trips Feed
st.markdown("---")
st.markdown("#### 📋 Dernières Expéditions Enregistrées")
if not voyages_all.empty:
    recent_table = voyages_all[[
        "date", "heure_depart", "heure_arrive", "camion_matricule", "conducteur_nom",
        "site_nom", "quantite_transporte", "distance_km", "taux_remplissage"
    ]].head(8).rename(columns={
        "date": "Date",
        "heure_depart": "Départ",
        "heure_arrive": "Arrivée",
        "camion_matricule": "Matricule Camion",
        "conducteur_nom": "Conducteur",
        "site_nom": "Site / Usine",
        "quantite_transporte": "Tonnage (T)",
        "distance_km": "Distance (km)",
        "taux_remplissage": "Remplissage (%)"
    })
    st.dataframe(recent_table, use_container_width=True, hide_index=True)
