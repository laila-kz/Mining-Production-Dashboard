"""
TDB Performance Conducteurs — Évaluation de la Productivité, Assiduité & Sécurité
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from utils.ui import render_header, render_kpi, render_empty_state, style_plotly_fig, PRIMARY_COLOR, ACCENT_COLOR, WARNING_COLOR, SUCCESS_COLOR
from utils.queries import get_conducteur_performance_stats

# 1. Page Configuration
st.set_page_config(
    page_title="Performance Conducteurs — Phosboucraa",
    page_icon="👨‍💼",
    layout="wide"
)

# 2. Hero Header
render_header(
    title="Tableau de Bord Performance des Conducteurs",
    subtitle="Évaluation des volumes transportés, assiduité, distances parcourues et incidents",
    icon="👨‍💼"
)

# 3. Load Data
drivers_df = get_conducteur_performance_stats()

# 4. Sidebar Filters
with st.sidebar:
    st.markdown("### 🔍 Filtres Conducteurs")
    st.markdown("---")
    
    search_name = st.text_input("Recherche par nom ou prénom", placeholder="Ex: Haddad, Sbai...")
    min_trips = st.slider("Nombre minimum de trajets", min_value=0, max_value=int(drivers_df["total_voyages"].max() or 10), value=0)

# Filter logic
filtered_df = drivers_df.copy()
if search_name:
    filtered_df = filtered_df[filtered_df["nom_complet"].str.contains(search_name, case=False, na=False)]
if min_trips > 0:
    filtered_df = filtered_df[filtered_df["total_voyages"] >= min_trips]

if filtered_df.empty:
    render_empty_state("Aucun conducteur ne correspond à la recherche.")
    st.stop()

# 5. Top KPI Row
total_drivers = len(filtered_df)
active_drivers = (filtered_df["total_voyages"] > 0).sum()
total_tonnage = filtered_df["total_tonnes"].sum()
avg_tonnage_driver = (total_tonnage / max(1, active_drivers))
top_driver_row = filtered_df.nlargest(1, "total_tonnes").iloc[0] if not filtered_df.empty else None

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    render_kpi("Effectif Chauffeurs", f"{total_drivers}", f"{active_drivers} en mission", PRIMARY_COLOR)
with k2:
    render_kpi("Tonnage Acheminé", f"{total_tonnage:,.0f} T", f"Moyenne: {avg_tonnage_driver:.1f} T / chauffeur", ACCENT_COLOR)
with k3:
    render_kpi("Total Voyages", f"{int(filtered_df['total_voyages'].sum())}", "Missions complétées", PRIMARY_COLOR)
with k4:
    render_kpi("Total Arrêts Déclarés", f"{int(filtered_df['nb_arrets'].sum())}", "Incidents / Pauses", WARNING_COLOR)
with k5:
    top_name = top_driver_row["nom_complet"] if top_driver_row is not None else "N/A"
    top_val = f"{top_driver_row['total_tonnes']:.0f} T" if top_driver_row is not None else "0 T"
    render_kpi("Leader Production", top_name, top_val, SUCCESS_COLOR)

st.markdown("---")

# 6. Visualizations
c1, c2 = st.columns([7, 5])

with c1:
    st.markdown("#### 🏆 Top 10 Conducteurs les Plus Productifs")
    top_10 = filtered_df.nlargest(10, "total_tonnes")
    fig_top = px.bar(
        top_10,
        x="nom_complet",
        y="total_tonnes",
        color="total_voyages",
        color_continuous_scale="Teal",
        labels={"nom_complet": "Conducteur", "total_tonnes": "Tonnage Total (T)", "total_voyages": "Nb Voyages"},
        title="Top 10 : Tonnage Transporté par Conducteur"
    )
    st.plotly_chart(style_plotly_fig(fig_top, height=380), use_container_width=True)

with c2:
    st.markdown("#### 🔄 Relation Voyages vs Tonnage")
    fig_rel = px.scatter(
        filtered_df,
        x="total_voyages",
        y="total_tonnes",
        size="distance_moyenne",
        hover_data=["nom_complet", "CIN", "nb_arrets"],
        labels={"total_voyages": "Nombre de Voyages", "total_tonnes": "Tonnage Total (T)", "distance_moyenne": "Distance Moy (km)"},
        title="Volume vs Nombre de Rotations"
    )
    st.plotly_chart(style_plotly_fig(fig_rel, height=380), use_container_width=True)

# 7. Detailed Table & Export
st.markdown("---")
h1, h2 = st.columns([8, 4])
with h1:
    st.markdown("#### 📋 Registre Individuel des Performances")
with h2:
    csv_drivers = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exporter les données conducteurs (CSV)",
        data=csv_drivers,
        file_name=f"conducteurs_performance_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

display_drivers = filtered_df.rename(columns={
    "id_conducteur": "ID",
    "nom_complet": "Nom & Prénom",
    "CIN": "Numéro CIN",
    "total_voyages": "Total Voyages",
    "total_tonnes": "Tonnage (T)",
    "distance_moyenne": "Distance Moy (km)",
    "nb_arrets": "Nb Arrêts",
    "total_arret_min": "Arrêt Cumulé (min)"
})

st.dataframe(display_drivers.round(2), use_container_width=True, hide_index=True)
