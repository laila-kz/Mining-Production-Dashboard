"""
TDB Suivi des Voyages — Module de Contrôle des Transports et Débits Miniers
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, date

from utils.ui import render_header, render_kpi, render_empty_state, style_plotly_fig, PRIMARY_COLOR, ACCENT_COLOR, WARNING_COLOR, SUCCESS_COLOR
from utils.queries import get_voyages_detailed, get_filter_options

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Suivi des Voyages — Phosboucraa",
    page_icon="🚛",
    layout="wide"
)

# 2. Header
render_header(
    title="Tableau de Bord des Voyages",
    subtitle="Supervision des flux de transport de phosphate, tonnages et cadences",
    icon="🚛"
)

# 3. Sidebar Filters
filter_opts = get_filter_options()

with st.sidebar:
    st.markdown("### 🔍 Filtres Opérationnels")
    st.markdown("---")

    # Safe Date Range Selector
    min_d = datetime.strptime(filter_opts["min_date"], "%Y-%m-%d").date() if filter_opts["min_date"] else date(2025, 1, 1)
    max_d = datetime.strptime(filter_opts["max_date"], "%Y-%m-%d").date() if filter_opts["max_date"] else date(2025, 12, 31)
    
    selected_dates = st.date_input(
        "📅 Période d'analyse",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d
    )
    
    # Safe date extraction
    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) > 0:
        start_date = selected_dates[0].strftime("%Y-%m-%d")
        end_date = selected_dates[1].strftime("%Y-%m-%d") if len(selected_dates) > 1 else start_date
    else:
        start_date, end_date = None, None

    # Truck Filter
    truck_choices = [{"id": None, "label": "Tous les camions"}] + [
        {"id": c["id_camion"], "label": f"Camion #{c['id_camion']} - {c['label']}"} for c in filter_opts["camions"]
    ]
    selected_truck_obj = st.selectbox(
        "🚚 Camion",
        options=truck_choices,
        format_func=lambda x: x["label"]
    )
    selected_camion_id = selected_truck_obj["id"]

    # Driver Filter
    driver_choices = [{"id": None, "label": "Tous les conducteurs"}] + [
        {"id": d["id_conducteur"], "label": d["nom_complet"]} for d in filter_opts["conducteurs"]
    ]
    selected_driver_obj = st.selectbox(
        "👨‍💼 Conducteur",
        options=driver_choices,
        format_func=lambda x: x["label"]
    )
    selected_driver_id = selected_driver_obj["id"]

    # Site Filter
    site_choices = [{"id": None, "label": "Tous les sites"}] + [
        {"id": s["id_site"], "label": s["nom"]} for s in filter_opts["sites"]
    ]
    selected_site_obj = st.selectbox(
        "🏭 Site / Destination",
        options=site_choices,
        format_func=lambda x: x["label"]
    )
    selected_site_id = selected_site_obj["id"]

# 4. Fetch Filtered Data
df = get_voyages_detailed(
    start_date=start_date,
    end_date=end_date,
    id_camion=selected_camion_id,
    id_conducteur=selected_driver_id,
    id_site=selected_site_id
)

if df.empty:
    render_empty_state("Aucun voyage ne correspond aux filtres sélectionnés. Essayez d'élargir la période.")
    st.stop()

# 5. Top KPI Row
k1, k2, k3, k4, k5 = st.columns(5)
total_tonnage = df["quantite_transporte"].sum()
total_trips = len(df)
avg_distance = df["distance_km"].mean()
avg_duration = df["duree_heures"].mean() if "duree_heures" in df.columns else 0.0
avg_rate = df["tonnes_par_heure"].mean() if "tonnes_par_heure" in df.columns else 0.0

with k1:
    render_kpi("Voyages Réalisés", f"{total_trips}", "Trajets enregistrés", PRIMARY_COLOR)
with k2:
    render_kpi("Volume Transporté", f"{total_tonnage:,.0f} T", f"Moy: {total_tonnage/total_trips:.1f} T / voyage", ACCENT_COLOR)
with k3:
    render_kpi("Distance Moyenne", f"{avg_distance:.1f} km", f"Total: {df['distance_km'].sum():,.0f} km", PRIMARY_COLOR)
with k4:
    render_kpi("Durée Moyenne", f"{avg_duration:.1f} h", "Temps de cycle moyen", WARNING_COLOR)
with k5:
    render_kpi("Cadence Moyenne", f"{avg_rate:.1f} T/h", "Débit de transport horaire", SUCCESS_COLOR)

st.markdown("---")

# 6. Charts Section
c1, c2 = st.columns([7, 5])

with c1:
    st.markdown("#### 📊 Évolution des Volumes Journaliers & Cadences")
    daily_v = df.groupby("date").agg({
        "quantite_transporte": "sum",
        "distance_km": "mean",
        "id_voyage": "count"
    }).reset_index().rename(columns={"id_voyage": "nb_voyages"})
    
    fig_v_trend = px.bar(
        daily_v,
        x="date",
        y="quantite_transporte",
        color_discrete_sequence=["#0F766E"],
        labels={"quantite_transporte": "Tonnage (T)", "date": "Date"},
        title="Tonnage Journalier Transporté"
    )
    fig_v_trend.add_scatter(
        x=daily_v["date"],
        y=daily_v["nb_voyages"],
        mode="lines+markers",
        name="Nb Voyages",
        yaxis="y2",
        line=dict(color="#F59E0B", width=2.5)
    )
    fig_v_trend.update_layout(
        yaxis2=dict(title="Nombre de Voyages", overlaying="y", side="right", showgrid=False)
    )
    st.plotly_chart(style_plotly_fig(fig_v_trend, height=380), use_container_width=True)

with c2:
    st.markdown("#### 🚚 Corrélation Charge vs Distance")
    fig_scatter = px.scatter(
        df,
        x="distance_km",
        y="quantite_transporte",
        color="camion_modele" if "camion_modele" in df.columns else None,
        size="camion_capacite" if "camion_capacite" in df.columns else None,
        hover_data=["camion_matricule", "conducteur_nom", "site_nom"],
        labels={"distance_km": "Distance (km)", "quantite_transporte": "Quantité (T)", "camion_modele": "Modèle"},
        title="Distribution Distance vs Tonnage par Modèle"
    )
    st.plotly_chart(style_plotly_fig(fig_scatter, height=380), use_container_width=True)

# 7. Detailed Table & Export
st.markdown("---")
h_left, h_right = st.columns([8, 4])
with h_left:
    st.markdown("#### 📋 Registre Détaillé des Voyages")
with h_right:
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exporter en CSV",
        data=csv_data,
        file_name=f"voyages_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

display_cols = [
    "id_voyage", "date", "heure_depart", "heure_arrive", "camion_matricule",
    "conducteur_nom", "site_nom", "quantite_transporte", "distance_km",
    "duree_heures", "tonnes_par_heure", "taux_remplissage"
]
table_df = df[[c for c in display_cols if c in df.columns]].rename(columns={
    "id_voyage": "ID Voyage",
    "date": "Date",
    "heure_depart": "Départ",
    "heure_arrive": "Arrivée",
    "camion_matricule": "Matricule",
    "conducteur_nom": "Conducteur",
    "site_nom": "Site",
    "quantite_transporte": "Tonnage (T)",
    "distance_km": "Distance (km)",
    "duree_heures": "Durée (h)",
    "tonnes_par_heure": "Débit (T/h)",
    "taux_remplissage": "Remplissage (%)"
})

st.dataframe(table_df, use_container_width=True, hide_index=True)
