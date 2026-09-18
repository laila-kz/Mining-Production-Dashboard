"""
TDB Contrôle Qualité — Analyse des Teneurs en Phosphate (P2O5) et Humidité
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from utils.ui import render_header, render_kpi, render_empty_state, style_plotly_fig, PRIMARY_COLOR, ACCENT_COLOR, WARNING_COLOR, SUCCESS_COLOR, DANGER_COLOR
from utils.queries import get_qualite_dataset, get_filter_options

# 1. Page Configuration
st.set_page_config(
    page_title="Contrôle Qualité — Phosboucraa",
    page_icon="🧪",
    layout="wide"
)

# 2. Hero Header
render_header(
    title="Tableau de Bord Contrôle Qualité",
    subtitle="Surveillance des teneurs en phosphate (P₂O₅), taux d'humidité et granulométrie",
    icon="🧪"
)

# 3. Sidebar Filters
filter_opts = get_filter_options()

with st.sidebar:
    st.markdown("### 🔍 Filtres Qualité")
    st.markdown("---")
    
    categories = ["Toutes les catégories"] + filter_opts["categories"]
    selected_category = st.selectbox("🏷️ Catégorie de Produit", options=categories)
    cat_filter = None if selected_category == "Toutes les catégories" else selected_category

    # Phosphate content slider
    phosphate_range = st.slider(
        "🧪 Taux de Phosphate P₂O₅ (%)",
        min_value=40.0,
        max_value=90.0,
        value=(40.0, 90.0),
        step=0.5
    )

# 4. Fetch Data
df = get_qualite_dataset(
    categorie=cat_filter,
    min_phosphate=phosphate_range[0],
    max_phosphate=phosphate_range[1]
)

if df.empty:
    render_empty_state("Aucun échantillon ne correspond aux critères de qualité sélectionnés.")
    st.stop()

# 5. Top KPI Row
COMMERCIAL_PHOSPHATE_TARGET = 65.0  # Commercial minimum %
MAX_HUMIDITY_THRESHOLD = 8.0        # Max allowable humidity %

total_samples = len(df)
mean_phosphate = df["taux_phosphate"].mean()
mean_humidity = df["humidite"].mean()
mean_granulo = df["granulometrie"].mean()

conforming_phosphate = (df["taux_phosphate"] >= COMMERCIAL_PHOSPHATE_TARGET).sum()
pct_conforming_p2o5 = (conforming_phosphate / total_samples) * 100

conforming_humidity = (df["humidite"] <= MAX_HUMIDITY_THRESHOLD).sum()
pct_conforming_hum = (conforming_humidity / total_samples) * 100

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    render_kpi("Échantillons Analysés", f"{total_samples}", "Lots contrôlés", PRIMARY_COLOR)
with k2:
    render_kpi("Teneur Moyenne P₂O₅", f"{mean_phosphate:.2f} %", f"Seuil cible: ≥ {COMMERCIAL_PHOSPHATE_TARGET}%", SUCCESS_COLOR if mean_phosphate >= COMMERCIAL_PHOSPHATE_TARGET else WARNING_COLOR)
with k3:
    render_kpi("Humidité Moyenne", f"{mean_humidity:.2f} %", f"Seuil max: ≤ {MAX_HUMIDITY_THRESHOLD}%", SUCCESS_COLOR if mean_humidity <= MAX_HUMIDITY_THRESHOLD else DANGER_COLOR)
with k4:
    render_kpi("Conformité P₂O₅", f"{pct_conforming_p2o5:.1f} %", f"{conforming_phosphate}/{total_samples} lots conformes", SUCCESS_COLOR)
with k5:
    render_kpi("Granulométrie Moyenne", f"{mean_granulo:.2f} mm", "Calibre moyen des grains", ACCENT_COLOR)

st.markdown("---")

# 6. Quality Analytics Charts
c1, c2 = st.columns([6, 6])

with c1:
    st.markdown("#### 📊 Distribution des Teneurs en Phosphate (P₂O₅)")
    fig_hist = px.histogram(
        df,
        x="taux_phosphate",
        nbins=20,
        color="categorie",
        color_discrete_sequence=["#0F766E", "#0EA5E9", "#F59E0B"],
        labels={"taux_phosphate": "Taux de Phosphate (%)", "count": "Fréquence"},
        title="Distribution de la teneur en P₂O₅ par catégorie"
    )
    # Add target line
    fig_hist.add_vline(
        x=COMMERCIAL_PHOSPHATE_TARGET,
        line_dash="dash",
        line_color="#EF4444",
        annotation_text=f"Seuil Commercial ({COMMERCIAL_PHOSPHATE_TARGET}%)",
        annotation_position="top left"
    )
    st.plotly_chart(style_plotly_fig(fig_hist, height=380), use_container_width=True)

with c2:
    st.markdown("#### 🧪 Corrélation Humidité vs Teneur en Phosphate")
    fig_scatter = px.scatter(
        df,
        x="humidite",
        y="taux_phosphate",
        color="categorie",
        size="granulometrie",
        hover_data=["nom_de_produit"],
        color_discrete_sequence=["#0F766E", "#0EA5E9", "#F59E0B"],
        labels={"humidite": "Humidité (%)", "taux_phosphate": "Teneur P₂O₅ (%)", "categorie": "Catégorie"},
        title="Positionnement Qualité : Teneur vs Humidité"
    )
    fig_scatter.add_hline(y=COMMERCIAL_PHOSPHATE_TARGET, line_dash="dot", line_color="#10B981")
    fig_scatter.add_vline(x=MAX_HUMIDITY_THRESHOLD, line_dash="dot", line_color="#EF4444")
    st.plotly_chart(style_plotly_fig(fig_scatter, height=380), use_container_width=True)

# 7. Quality Correlation Heatmap
st.markdown("---")
c_heat, c_cat = st.columns([5, 7])

with c_heat:
    st.markdown("#### 📐 Matrice de Corrélation Physico-Chimique")
    corr_cols = ["taux_phosphate", "humidite", "granulometrie"]
    corr_df = df[corr_cols].corr()
    fig_corr = px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="Viridis",
        labels=dict(color="Corrélation")
    )
    st.plotly_chart(style_plotly_fig(fig_corr, height=350, show_legend=False), use_container_width=True)

with c_cat:
    st.markdown("#### 📦 Répartition par Catégorie et Produit")
    cat_summary = df.groupby(["categorie", "nom_de_produit"]).agg({
        "taux_phosphate": "mean",
        "humidite": "mean",
        "granulometrie": "mean",
        "id_qualite": "count"
    }).reset_index().rename(columns={
        "categorie": "Catégorie",
        "nom_de_produit": "Produit",
        "taux_phosphate": "P₂O₅ Moy (%)",
        "humidite": "Humidité Moy (%)",
        "granulometrie": "Granulo (mm)",
        "id_qualite": "Échantillons"
    })
    st.dataframe(cat_summary.round(2), use_container_width=True, hide_index=True)

# 8. Export Data
st.markdown("---")
h1, h2 = st.columns([8, 4])
with h1:
    st.markdown("#### 📋 Registre des Analyses de Laboratoire")
with h2:
    csv_qual = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exporter les données qualité (CSV)",
        data=csv_qual,
        file_name=f"qualite_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

st.dataframe(
    df.rename(columns={
        "id_qualite": "ID Qualité",
        "categorie": "Catégorie",
        "nom_de_produit": "Nom Produit",
        "granulometrie": "Granulométrie (mm)",
        "taux_phosphate": "Teneur P₂O₅ (%)",
        "humidite": "Humidité (%)"
    }),
    use_container_width=True,
    hide_index=True
)
