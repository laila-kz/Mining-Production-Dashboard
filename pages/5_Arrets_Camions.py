"""
TDB Suivi des Arrêts Camions — Analyse des Causes, Pannes & Temps d'Indisponibilité
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from utils.ui import render_header, render_kpi, render_empty_state, style_plotly_fig, PRIMARY_COLOR, ACCENT_COLOR, WARNING_COLOR, DANGER_COLOR, SUCCESS_COLOR
from utils.queries import get_arrets_detailed, get_filter_options

# 1. Page Configuration
st.set_page_config(
    page_title="Arrêts Camions — Phosboucraa",
    page_icon="🛑",
    layout="wide"
)

# 2. Hero Header
render_header(
    title="Tableau de Bord des Arrêts de la Flotte",
    subtitle="Monitoring des pannes, maintenances préventives, causes racines et indicateurs MTTR",
    icon="🛑"
)

# 3. Sidebar Filters
filter_opts = get_filter_options()

with st.sidebar:
    st.markdown("### 🔍 Filtres Arrêts")
    st.markdown("---")
    
    types = ["Tous les types"] + filter_opts["types_arret"]
    selected_type = st.selectbox("🛑 Type d'arrêt", options=types)
    type_filter = None if selected_type == "Tous les types" else selected_type

    truck_choices = [{"id": None, "label": "Tous les camions"}] + [
        {"id": c["id_camion"], "label": f"Camion #{c['id_camion']} ({c['label']})"} for c in filter_opts["camions"]
    ]
    selected_truck_obj = st.selectbox("🚚 Camion concerné", options=truck_choices, format_func=lambda x: x["label"])
    truck_filter = selected_truck_obj["id"]

# 4. Fetch Data
df = get_arrets_detailed(type_arret=type_filter, id_camion=truck_filter)

if df.empty:
    render_empty_state("Aucun incident d'arrêt ne correspond aux critères sélectionnés.")
    st.stop()

# 5. Top KPI Row
total_incidents = len(df)
total_lost_minutes = df["duree_minutes"].sum()
total_lost_hours = total_lost_minutes / 60.0
avg_duration_min = df["duree_minutes"].mean()

# MTTR: Mean Time To Repair on mechanical/failure types ("Panne" or "Maintenance")
pannes_df = df[df["type"].isin(["Panne", "Maintenance"])]
mttr_min = pannes_df["duree_minutes"].mean() if not pannes_df.empty else 0.0

# Most frequent reason
top_reason = df["raison"].value_counts().index[0] if not df["raison"].empty else "N/A"

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    render_kpi("Incidents Enregistrés", f"{total_incidents}", "Événements d'arrêt", PRIMARY_COLOR)
with k2:
    render_kpi("Temps Perdu Cumulé", f"{total_lost_hours:.1f} h", f"{total_lost_minutes:,.0f} minutes au total", DANGER_COLOR if total_lost_hours > 50 else WARNING_COLOR)
with k3:
    render_kpi("Durée Moyenne / Arrêt", f"{avg_duration_min:.0f} min", "Impact moyen par incident", WARNING_COLOR)
with k4:
    render_kpi("MTTR (Réparation Moy)", f"{mttr_min:.0f} min", "Mean Time To Repair", ACCENT_COLOR)
with k5:
    render_kpi("Cause Principale", top_reason, f"{df['raison'].value_counts().iloc[0]} occurrences", PRIMARY_COLOR)

st.markdown("---")

# 6. Charts Section
c1, c2 = st.columns([5, 7])

with c1:
    st.markdown("#### 🛑 Répartition du Temps Perdu par Type")
    type_agg = df.groupby("type")["duree_minutes"].sum().reset_index()
    fig_donut = px.pie(
        type_agg,
        values="duree_minutes",
        names="type",
        hole=0.45,
        color="type",
        color_discrete_map={"Panne": "#EF4444", "Maintenance": "#F59E0B", "Pause": "#0F766E"}
    )
    fig_donut.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(style_plotly_fig(fig_donut, height=380, show_legend=False), use_container_width=True)

with c2:
    st.markdown("#### 🔧 Analyse des Causes Racines (Raisons)")
    cause_agg = df.groupby(["raison", "type"])["duree_minutes"].agg(["sum", "count"]).reset_index().rename(
        columns={"sum": "minutes_totales", "count": "nb_incidents"}
    ).sort_values(by="minutes_totales", ascending=True)
    
    fig_cause = px.bar(
        cause_agg,
        y="raison",
        x="minutes_totales",
        color="type",
        orientation="h",
        color_discrete_map={"Panne": "#EF4444", "Maintenance": "#F59E0B", "Pause": "#0F766E"},
        labels={"minutes_totales": "Minutes Totales", "raison": "Cause / Motif", "type": "Type"},
        title="Impact Cumulé par Motif d'Arrêt"
    )
    st.plotly_chart(style_plotly_fig(fig_cause, height=380), use_container_width=True)

# 7. Timeline Analysis
st.markdown("---")
st.markdown("#### 📅 Historique Chronologique des Événements d'Arrêt")
daily_arret = df.groupby("date").agg({
    "duree_minutes": "sum",
    "id_arret": "count"
}).reset_index().rename(columns={"id_arret": "nb_arrets"})

fig_timeline = px.bar(
    daily_arret,
    x="date",
    y="duree_minutes",
    labels={"date": "Date", "duree_minutes": "Minutes d'Arrêt (min)"},
    color_discrete_sequence=["#F59E0B"],
    title="Minutes d'Arrêt par Jour"
)
st.plotly_chart(style_plotly_fig(fig_timeline, height=320), use_container_width=True)

# 8. Detailed Incident Log & Export
st.markdown("---")
h1, h2 = st.columns([8, 4])
with h1:
    st.markdown("#### 📋 Journal des Incidents & Maintenances")
with h2:
    csv_arrets = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exporter le journal des arrêts (CSV)",
        data=csv_arrets,
        file_name=f"arrets_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

display_arrets = df[[
    "date_heure", "type", "raison", "duree", "duree_minutes",
    "camion_matricule", "camion_modele", "conducteur_nom"
]].rename(columns={
    "date_heure": "Date & Heure",
    "type": "Type",
    "raison": "Cause / Raison",
    "duree": "Durée (Format)",
    "duree_minutes": "Durée (min)",
    "camion_matricule": "Camion",
    "camion_modele": "Modèle",
    "conducteur_nom": "Conducteur"
})

st.dataframe(display_arrets, use_container_width=True, hide_index=True)
