"""
TDB Performance Camions — Rendement, Disponibilité & Utilisation de la Flotte
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from utils.ui import render_header, render_kpi, render_empty_state, style_plotly_fig, PRIMARY_COLOR, ACCENT_COLOR, WARNING_COLOR, SUCCESS_COLOR, DANGER_COLOR
from utils.queries import get_camion_performance_stats

# 1. Page Configuration
st.set_page_config(
    page_title="Performance Camions — Phosboucraa",
    page_icon="🚚",
    layout="wide"
)

# 2. Hero Header
render_header(
    title="Tableau de Bord Performance des Camions",
    subtitle="Suivi de la disponibilité opérationnelle, taux d'utilisation des bennes et temps d'arrêt",
    icon="🚚"
)

# 3. Load Data
stats_df = get_camion_performance_stats()

# 4. Sidebar Filters
with st.sidebar:
    st.markdown("### 🔍 Filtres Flotte")
    st.markdown("---")
    
    models = ["Tous les modèles"] + sorted(list(stats_df["modele"].unique()))
    selected_model = st.selectbox("🚛 Constructeur / Modèle", options=models)
    
    min_trips = st.slider("Nombre minimum de voyages", min_value=0, max_value=int(stats_df["total_voyages"].max() or 10), value=0)

# Apply filters
filtered_df = stats_df.copy()
if selected_model != "Tous les modèles":
    filtered_df = filtered_df[filtered_df["modele"] == selected_model]
if min_trips > 0:
    filtered_df = filtered_df[filtered_df["total_voyages"] >= min_trips]

if filtered_df.empty:
    render_empty_state("Aucun camion ne correspond aux critères sélectionnés.")
    st.stop()

# 5. Top KPI Row
total_fleet = len(filtered_df)
active_trucks = (filtered_df["total_voyages"] > 0).sum()
total_tonnage_fleet = filtered_df["total_tonnes"].sum()
avg_utilization = filtered_df["taux_utilisation_moyen"].mean()
total_downtime_hrs = (filtered_df["arret_total_minutes"].sum()) / 60.0

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    render_kpi("Effectif Flotte", f"{total_fleet} camions", f"{active_trucks} en activité", PRIMARY_COLOR)
with k2:
    render_kpi("Tonnage Global", f"{total_tonnage_fleet:,.0f} T", f"Moy: {total_tonnage_fleet/max(1, active_trucks):.1f} T / camion", ACCENT_COLOR)
with k3:
    render_kpi("Taux d'Utilisation", f"{avg_utilization:.1f} %", "Remplissage / capacité", SUCCESS_COLOR if avg_utilization >= 75 else WARNING_COLOR)
with k4:
    render_kpi("Cumul Arrêts", f"{total_downtime_hrs:.1f} h", f"{int(filtered_df['nb_arrets'].sum())} incidents", WARNING_COLOR if total_downtime_hrs > 0 else SUCCESS_COLOR)
with k5:
    render_kpi("Productivité Flotte", f"{(total_tonnage_fleet / max(1, active_trucks)):.0f} T/u", "Rendement unitaire", PRIMARY_COLOR)

st.markdown("---")

# 6. Performance Visualizations
c1, c2 = st.columns([7, 5])

with c1:
    st.markdown("#### 🏆 Top 10 des Camions par Tonnage Transporté")
    top_trucks = filtered_df.nlargest(10, "total_tonnes")
    fig_bar = px.bar(
        top_trucks,
        x="matricule",
        y="total_tonnes",
        color="modele",
        color_discrete_sequence=["#0F766E", "#0EA5E9", "#F59E0B"],
        labels={"matricule": "Matricule Camion", "total_tonnes": "Tonnage Total (T)", "modele": "Modèle"},
        title="Top 10 Rendement de la flotte"
    )
    st.plotly_chart(style_plotly_fig(fig_bar, height=380), use_container_width=True)

with c2:
    st.markdown("#### ⚙️ Comparatif par Modèle de Camion")
    model_agg = filtered_df.groupby("modele").agg({
        "total_tonnes": "sum",
        "total_voyages": "sum",
        "arret_total_minutes": "mean",
        "taux_utilisation_moyen": "mean"
    }).reset_index()
    
    fig_model = px.bar(
        model_agg,
        x="modele",
        y="total_tonnes",
        color="modele",
        color_discrete_sequence=["#0F766E", "#0EA5E9", "#F59E0B"],
        labels={"modele": "Modèle", "total_tonnes": "Tonnage Total (T)"},
        title="Tonnage Total par Constructeur"
    )
    st.plotly_chart(style_plotly_fig(fig_model, height=380, show_legend=False), use_container_width=True)

# 7. Scatter Correlation: Tonnage vs Downtime
st.markdown("---")
st.markdown("#### 🛑 Matrice Productivité vs Temps d'Arrêt (Détection d'Anomalies)")
fig_anomaly = px.scatter(
    filtered_df,
    x="arret_total_minutes",
    y="total_tonnes",
    size="capacite",
    color="modele",
    hover_data=["matricule", "total_voyages", "nb_arrets"],
    labels={"arret_total_minutes": "Temps d'arrêt (min)", "total_tonnes": "Tonnage Transporté (T)", "modele": "Modèle"},
    title="Analyse Quadrant : Production vs Indisponibilité"
)
st.plotly_chart(style_plotly_fig(fig_anomaly, height=400), use_container_width=True)

# 8. Detailed Fleet Table & Export
st.markdown("---")
h1, h2 = st.columns([8, 4])
with h1:
    st.markdown("#### 📋 Tableau Récapitulatif de la Flotte")
with h2:
    csv_trucks = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exporter la flotte (CSV)",
        data=csv_trucks,
        file_name=f"camions_performance_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

display_trucks = filtered_df.rename(columns={
    "id_camion": "ID Camion",
    "matricule": "Matricule",
    "modele": "Modèle",
    "capacite": "Capacité Benne (T)",
    "total_voyages": "Total Voyages",
    "total_tonnes": "Total Tonnage (T)",
    "distance_moyenne": "Distance Moy (km)",
    "taux_utilisation_moyen": "Taux Remplissage (%)",
    "arret_total_minutes": "Arrêts (min)",
    "nb_arrets": "Nb Incidents"
})

st.dataframe(display_trucks.round(2), use_container_width=True, hide_index=True)
