

import streamlit as st
import pandas as pd
import plotly.express as px
from database import fetch_data

# Helper to apply a consistent Plotly style to figures when a plotly_style function isn't provided elsewhere.
def plotly_style(fig):
    try:
        fig.update_layout(
            template="plotly_white",
            title={"x": 0.5},
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=20, t=60, b=40)
        )
    except Exception:
        # If updating layout fails for any reason, return the original figure unchanged.
        pass
    return fig

# --- Page configuration ---
st.set_page_config(page_title="TDB Performance Camions",page_icon="🟢", layout="wide")

# Theme color palette and custom CSS
primaryColor = "#0F766E"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F6F8FA"
textColor = "#1F2937"
font = "sans-serif"
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&family=Roboto&display=swap" rel="stylesheet">
    <style>
        /* Base font */
        html, body, .stApp {
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            color: #1F2937;
        }
        /* Sidebar nav links (generic selector for reliability) */
        section[data-testid="stSidebar"] a {
            background: #ffffff !important;
            color: #0F766E !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            margin-bottom: 8px !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 500 !important;
            text-decoration: none !important;
            transition: all 0.25s ease-in-out;
            border: 1px solid #e5e7eb !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.04) !important;
        }
        /* Hover effect */
        section[data-testid="stSidebar"] a:hover {
            background: linear-gradient(135deg, #0EA5E9, #38BDF8) !important;
            color: white !important;
            transform: translateX(3px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important;
        }
        /* Active (selected) link (aria-current="page") */
        section[data-testid="stSidebar"] a[aria-current="page"] {
            background: linear-gradient(135deg, #0F766E, #115E59) !important;
            color: white !important;
            font-weight: 600 !important;
        }
        body, .stApp, [data-testid="stAppViewContainer"] {
            background-color: #f3f4f6 !important;
        }
        [data-testid="stBlock"] {
            background: white !important;
            padding: 2rem !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        }
        /* Titles (Dashboard name, KPI headers) */
        h1, h2, h3, .stSubheader {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700 !important;
            color: #0F766E;
        }
        /* Section subtitles */
        .section-title-bar, .stMarkdown h4 {
            font-size: 18px !important;
            font-weight: 500 !important;
            font-family: 'Poppins', sans-serif !important;
            color: #0F766E !important;
        }
        /* Normal text (tables, paragraphs) */
        .stMarkdown, .stText, .stDataFrame, .stTable {
            font-family: 'Roboto', sans-serif !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            color: #1F2937 !important;
        }
        /* Buttons */
        .stButton>button {
            background-color: #0F766E !important;
            color: #fff !important;
            border-radius: 8px !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 0.6em 1.2em !important;
        }
        .stButton>button:hover {
            background-color: #115e59 !important;
        }
        /* KPI cards */
        .kpi-card {
            background: #F6F8FA;
            border-radius: 18px;
            box-shadow: 0 4px 18px rgba(15,118,110,0.10);
            padding: 1.2rem 0.5rem 1rem 0.5rem;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .kpi-label {
            font-size: 1.05rem;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            color: #0F766E;
            margin-bottom: 0.3rem;
        }
        .kpi-value {
            font-size: 2.1rem;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700;
            color: #0F766E;
            margin-bottom: 0.1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header section with logo and title
from datetime import datetime
# Header section with lighter, modern style
st.markdown(f"""
<div style="
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(90deg, #F6F8FA 60%, #E0F2F1 100%);
    color: #0F766E;
    padding: 1.5rem 1rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 3px 10px rgba(15,118,110,0.08);
    margin-bottom: 2rem;
">
    <img src='phosboucraa_logo.jpg' width='80' style='border-radius:8px; margin-bottom:0.8rem; box-shadow:0 2px 6px rgba(15,118,110,0.10);'>
    <div style='font-size:2.5rem; font-weight:700;'>TDB de Performance Camions</div>
    <div style='font-size:1.2rem; margin-top:0.2rem; background: rgba(20,184,166,0.10); color:#115E59; padding:0.2rem 0.5rem; border-radius:5px;'>Module Reporting & Dashboard</div>
    <div style='margin-top:0.4rem; font-size:0.85rem; opacity:0.85;'>Date et heure : {datetime.now().strftime('%A %d %B %Y, %H:%M')}</div>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
try:
    trips = fetch_data("voyage")
    trucks = fetch_data("camion")
except Exception as e:
    st.error(f"Erreur lors du chargement des données: {e}")
    st.stop()

if trips.empty or trucks.empty:
    st.warning("Aucune donnée disponible pour les voyages ou camions.")
    st.stop()

# --- Calculate metrics ---
try:
    trips["heure_depart"] = pd.to_datetime(trips["heure_depart"])
    trips["heure_arrive"] = pd.to_datetime(trips["heure_arrive"])
    trips["duration_hours"] = (trips["heure_arrive"] - trips["heure_depart"]).dt.total_seconds() / 3600
    trips["tons_per_hour"] = trips["quantite_transporte"] / trips["duration_hours"]
except Exception as e:
    st.error(f"Erreur lors du calcul des métriques: {e}")
    st.stop()

# --- Sidebar filters ---
st.sidebar.header("Filtrer les données")
date_range = st.sidebar.date_input(
    "Date range",
    [trips["date"].min(), trips["date"].max()]
)
selected_truck = st.sidebar.multiselect("Camion", trucks["id_camion"].unique())

filtered_df = trips[
    (pd.to_datetime(trips["date"]).dt.date >= date_range[0]) &
    (pd.to_datetime(trips["date"]).dt.date <= date_range[1])
]
if selected_truck:
    filtered_df = filtered_df[filtered_df["id_camion"].isin(selected_truck)]

if filtered_df.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()

# --- KPIs ---
# Inject custom KPI styles and apply them to all page section titles
st.markdown(
    """
    <style>
    /* KPI Section title (kept as class for explicit use) */
    .kpi-section-title {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        color: #0F766E !important;
        margin: 1rem 0 1.2rem 0 !important;
        padding: 0.6rem 1rem !important;
        background: linear-gradient(90deg, rgba(15,118,110,0.08), rgba(15,118,110,0.02)) !important;
        border-left: 6px solid #0F766E !important;
        border-radius: 8px !important;
        display: inline-block !important;
        box-shadow: 0 2px 6px rgba(15,118,110,0.08) !important;
    }

    /* Apply same visual style to standard headings and Streamlit subheaders */
    h1, h2, h3, h4, .stSubheader, .section-title-bar, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        color: #0F766E !important;
        margin: 1rem 0 1.2rem 0 !important;
        padding: 0.6rem 1rem !important;
        background: linear-gradient(90deg, rgba(15,118,110,0.08), rgba(15,118,110,0.02)) !important;
        border-left: 6px solid #0F766E !important;
        border-radius: 8px !important;
        display: inline-block !important;
        box-shadow: 0 2px 6px rgba(15,118,110,0.08) !important;
    }

    /* KPI cards container */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 2rem;
    }

    /* Individual KPI card */
    .kpi-card {
        flex: 1;
        background: #FFFFFF;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        padding: 1rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(15,118,110,0.15);
    }
    .kpi-label {
        font-size: 0.95rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        color: #115E59;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        color: #0F766E;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Example explicit KPI section title (keeps backward compatibility)
st.markdown("<div class='kpi-section-title'>🧾Indicateurs clés</div>", unsafe_allow_html=True)

# Aggregate per-truck metrics
truck_summary = filtered_df.groupby("id_camion").agg(
    total_trips=pd.NamedAgg(column="id_voyage", aggfunc="count"),
    total_tons=pd.NamedAgg(column="quantite_transporte", aggfunc="sum"),
    avg_load=pd.NamedAgg(column="quantite_transporte", aggfunc="mean"),
    avg_duration=pd.NamedAgg(column="duration_hours", aggfunc="mean"),
    avg_tph=pd.NamedAgg(column="tons_per_hour", aggfunc="mean")
).reset_index()


# Load arret.csv for downtime
import re
arret = pd.read_csv("data/arret.csv")
def duree_to_seconds(duree_str):
    if pd.isnull(duree_str):
        return 0
    parts = re.split(r":", str(duree_str))
    try:
        if len(parts) == 3:
            h, m, s = map(int, parts)
            return h*3600 + m*60 + s
        elif len(parts) == 2:
            m, s = map(int, parts)
            return m*60 + s
        elif len(parts) == 1:
            return int(parts[0])
    except Exception:
        return 0
    return 0
arret["duree_seconds"] = arret["duree"].apply(duree_to_seconds)

# Inject custom KPI tile styles
st.markdown(
    """
    <style>
    .kpi-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-tile {
        flex: 1;
        background: #E5E7EB;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-tile:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(15,118,110,0.15);
    }
    .kpi-tile .label {
        font-size: 0.9rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.4rem;
    }
    .kpi-tile .value {
        font-size: 1.8rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        color: #0F766E;
    }
    .chart-card {
    background: #F6F8FA;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(15,118,110,0.07);
    }
    .chart-card-alt {
    background: #3a6438; /* lighter background */
    border-left: 6px solid #0F766E; /* accent bar */
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }


    </style>
    """,
    unsafe_allow_html=True
)

# KPIs
total_voyages = int(truck_summary["total_trips"].sum())
total_tonnage = round(truck_summary["total_tons"].sum(),2)
avg_dispo = 0
avg_arrets = 0
if "id_camion" in truck_summary.columns:
    active_hours = truck_summary.set_index("id_camion")["avg_duration"] * truck_summary.set_index("id_camion")["total_trips"]
    downtime = arret.groupby("id_camion")["duree_seconds"].sum() / 3600
    total_hours = active_hours.add(downtime, fill_value=0)
    availability = (active_hours / total_hours * 100).fillna(0)
    truck_summary["availability"] = availability.reindex(truck_summary["id_camion"]).values
    avg_dispo = round(truck_summary["availability"].mean(),2)
    avg_arrets = round(arret["id_camion"].value_counts().mean(),2)
st.markdown(f"""
<div class='kpi-row'>
    <div class='kpi-tile'>
        <div class='label'>Nombre total de voyages par camion</div>
        <div class='value'>{total_voyages}</div>
    </div>
    <div class='kpi-tile'>
        <div class='label'>Tonnage total transporté par camion</div>
        <div class='value'>{total_tonnage}</div>
    </div>
    <div class='kpi-tile'>
        <div class='label'>Disponibilité moyenne (%)</div>
        <div class='value'>{avg_dispo}</div>
    </div>
    <div class='kpi-tile'>
        <div class='label'>Moyenne des arrêts par camion</div>
        <div class='value'>{avg_arrets}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Visualisations ---
st.subheader("📋 Données") 
def special_title(text, icon="✨"):
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #0D9488, #0F766E);
        color: white;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1rem;
        text-align: left;
    ">
    {icon} {text}
    </div>
    """, unsafe_allow_html=True)


# Camions avec plus d’arrêts que la moyenne
special_title("Camions avec plus d’arrêts que la moyenne")
truck_stops = arret["id_camion"].value_counts()
mean_stops = truck_stops.mean()
above_avg_stops = truck_stops[truck_stops > mean_stops].reset_index()
above_avg_stops.columns = ["id_camion", "Nombre d'arrêts"]
styled_above_avg_stops = above_avg_stops.style.set_table_styles(
    [
        {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
        {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
        {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
        {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
    ]
).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
st.dataframe(styled_above_avg_stops, use_container_width=True)

# Top 5 camions les plus performants
special_title("Top 5 camions les plus performants")
top5_perf = truck_summary.sort_values(["total_trips", "total_tons", "availability"], ascending=False).head(5)
styled_top5_perf = top5_perf.style.set_table_styles(
    [
        {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
        {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
        {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
        {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
    ]
).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
st.dataframe(styled_top5_perf, use_container_width=True)

# 5 camions les moins performants
special_title("5 camions les moins performants")
bottom5_perf = truck_summary.sort_values(["total_trips", "total_tons", "availability"], ascending=True).head(5)
styled_bottom5_perf = bottom5_perf.style.set_table_styles(
    [
        {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
        {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
        {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
        {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
    ]
).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
st.dataframe(styled_bottom5_perf, use_container_width=True)

# --- Visualisations ---
st.subheader("📈 Visualisations") 
def special_title2(text, icon="📌"):
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #0D9488, #0F766E);
        color: white;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1rem;
        text-align: left;
    ">
    {icon} {text}
    </div>
    """, unsafe_allow_html=True)


# Classement camions par voyages
special_title2("Classement camions par voyages")
fig_voyages = px.bar(truck_summary.sort_values("total_trips", ascending=False), x="id_camion", y="total_trips", title="Classement par nombre de voyages")
import streamlit.components.v1 as components

# Render the Plotly figure inside a div with the "chart-card" class so the CSS applies
html = f"<div class='chart-card'>{fig_voyages.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
components.html(html, height=520, scrolling=True)

import streamlit.components.v1 as components

# Classement camions par tonnage
special_title2("Classement camions par tonnage transporté")

fig_tonnage = px.bar(
    truck_summary.sort_values("total_tons", ascending=False),
    x="id_camion", y="total_tons",
    title="Classement par tonnage transporté"
)
# Apply basic styling directly since plotly_style is not defined
fig_tonnage.update_layout(
    template="plotly_white",
    title={"x": 0.5},
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=20, t=60, b=40)
)
html_tonnage = f"<div class='chart-card'>{fig_tonnage.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
components.html(html_tonnage, height=520, scrolling=True)

# Évolution des performances d’un camion
special_title2("Évolution des performances d’un camion choisi")
selected_perf_truck = st.selectbox("Choisir un camion pour l'évolution", truck_summary["id_camion"].unique())
perf_truck_df = filtered_df[filtered_df["id_camion"] == selected_perf_truck]
if not perf_truck_df.empty:
    perf_by_date = perf_truck_df.groupby(pd.to_datetime(perf_truck_df["date"]).dt.date)["quantite_transporte"].sum().reset_index()
    perf_by_date.columns = ["date", "tonnage"]
    fig_perf = px.line(perf_by_date, x="date", y="tonnage", title=f"Évolution du tonnage pour le camion {selected_perf_truck}")
    st.plotly_chart(fig_perf, use_container_width=True)



import streamlit.components.v1 as components

# 1. Total trips per truck
special_title2("Nombre de voyages par camion")

fig1 = px.bar(
    truck_summary,
    x="id_camion", y="total_trips",
    title="Nombre de voyages par camion"
)
fig1 = plotly_style(fig1)
html_fig1 = f"<div class='chart-card'>{fig1.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
components.html(html_fig1, height=520, scrolling=True)

# 2. Total tons transported per truck
special_title2("Tons transportés par camion")
fig2 = px.bar(
    truck_summary,
    x="id_camion", y="total_tons",
    title="Tons transportés par camion"
)
fig2 = plotly_style(fig2)
html_fig2 = f"<div class='chart-card'>{fig2.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
components.html(html_fig2, height=520, scrolling=True)

import streamlit.components.v1 as components

# 3. Average load per trip
special_title2("Charge moyenne par voyage par camion")
fig3 = px.box(
    filtered_df,
    x="id_camion", y="quantite_transporte",
    title="Charge moyenne par voyage par camion"
)

def plotly_style2(fig):
    """
    Apply a dark/green card-friendly style to a Plotly figure.
    The figure background is made transparent so the surrounding .chart-card-alt div (#3a6438) shows through,
    and text/lines are adjusted to be readable on that background.
    """
    dark_green = "#0F766E"        # darkish green to replace black elements
    light_text = "#060606"        # light text for contrast on dark background
    hover_bg = "#145A46"          # slightly darker hover label background

    try:
        fig.update_layout(
            template="plotly_white",
            title={"x": 0.5, "font": {"color": light_text}},
            paper_bgcolor="rgba(0,0,0,0)",  # keep figure transparent so container background shows
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=light_text, family="Poppins, Roboto, sans-serif"),
            legend=dict(bgcolor=f"rgba(15,118,110,0.08)", font=dict(color=light_text)),
            margin=dict(l=40, r=20, t=60, b=40),
            hoverlabel=dict(bgcolor=hover_bg, font=dict(color=light_text))
        )
        # Axes and grid styling for good contrast on dark green
        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(15,118,110,0.06)",  # subtle green grid instead of white/black
            zeroline=False,
            tickcolor=light_text,
            title_font=dict(color=light_text),
            tickfont=dict(color=light_text),
            linecolor=dark_green
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(15,118,110,0.06)",
            zeroline=False,
            tickcolor=light_text,
            title_font=dict(color=light_text),
            tickfont=dict(color=light_text),
            linecolor=dark_green
        )
        # Gentle marker/line defaults: remove heavy black outlines and use dark green accents where applicable
        fig.update_traces(marker=dict(line=dict(width=0, color=dark_green)))
    except Exception:
        pass
    return fig

fig3 = plotly_style2(fig3)  # apply custom style
html_fig3 = f"<div class='chart-card-alt'>{fig3.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
components.html(html_fig3, height=520, scrolling=True)

# 4. Tons per hour per truck
special_title2("Tons par heure par camion")
fig4 = px.scatter(
    truck_summary,
    x="id_camion", y="avg_tph",
    size="total_trips", color="total_tons",
    hover_data=["avg_load", "avg_duration"],
    title="Tons par heure par camion"
)
fig4 = plotly_style2(fig4)
html_fig4 = f"<div class='chart-card-alt'>{fig4.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
components.html(html_fig4, height=520, scrolling=True)

# 5. Trend of trips per truck over time
trips_per_day_truck = filtered_df.groupby([pd.to_datetime(filtered_df["date"]).dt.date, "id_camion"]).size().reset_index(name="trips")
if not trips_per_day_truck.empty:
    trips_per_day_truck.rename(columns={0: "date"}, inplace=True)
    fig5 = px.line(trips_per_day_truck, x="date", y="trips", color="id_camion", title="Tendance des voyages par camion")
    st.plotly_chart(fig5, use_container_width=True)
    # Export section
    st.markdown("<div class='section-title-bar'>💾 Export des Données</div>", unsafe_allow_html=True)
    st.markdown("---")
    col_export1, col_export2 = st.columns([1, 3])

    with col_export1:
        # Determine start/end dates from the sidebar date_range
        if isinstance(date_range, (list, tuple)) and len(date_range) >= 2:
            start_date = pd.to_datetime(date_range[0]).strftime("%Y-%m-%d")
            end_date = pd.to_datetime(date_range[1]).strftime("%Y-%m-%d")
        else:
            start_date = pd.to_datetime(date_range).strftime("%Y-%m-%d")
            end_date = start_date

        # Build a readable truck label for the filename
        if selected_truck:
            truck_label = "_".join([str(x).replace(" ", "_") for x in selected_truck])
        else:
            truck_label = "all_trucks"

        # Let user choose which dataset to export
        dataset_choice = st.selectbox("Donnée à exporter", ["Voyages filtrés", "Résumé camions", "Arrêts"])

        if dataset_choice == "Voyages filtrés":
            df_to_export = filtered_df.copy()
            filename = f"voyages_{truck_label}_{start_date}_{end_date}.csv"
        elif dataset_choice == "Résumé camions":
            df_to_export = truck_summary.copy()
            filename = f"resume_camions_{truck_label}_{start_date}_{end_date}.csv"
        else:
            df_to_export = arret.copy()
            filename = f"arrets_{truck_label}_{start_date}_{end_date}.csv"


        st.markdown("""
    <style>
    /* Sidebar nav links (generic selector for reliability) */
    section[data-testid="stSidebar"] a {
        background: #ffffff !important;
        color: #0F766E !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        transition: all 0.25s ease-in-out;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04) !important;
    }
    /* Hover effect */
    section[data-testid="stSidebar"] a:hover {
        background: linear-gradient(135deg, #0EA5E9, #38BDF8) !important;
        color: white !important;
        transform: translateX(3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important;
    }
    /* Active (selected) link (aria-current="page") */
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: linear-gradient(135deg, #0F766E, #115E59) !important;
        color: white !important;
        font-weight: 600 !important;
    }
        
        .stDownloadButton button {
            background-color: #0F766E !important;
            color: #fff !important;
            border-radius: 8px !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 0.6em 1.2em !important;
            box-shadow: 0 4px 16px rgba(15,118,110,0.18), 0 1.5px 6px rgba(0,0,0,0.10);
            transition: background 0.2s, box-shadow 0.2s;
        }
        .stDownloadButton button:hover {
            background-color: #115e59 !important;
            color: #fff !important;
            box-shadow: 0 8px 24px rgba(15,118,110,0.28), 0 2px 8px rgba(0,0,0,0.13);
            transform: translateY(-2px) scale(1.03);
        }
        </style>
        """, unsafe_allow_html=True)
        st.download_button(
            label="📥 Télécharger CSV",
            data=df_to_export.to_csv(index=False).encode("utf-8"),
            file_name=filename,
            mime="text/csv",
            help="Télécharger les données sélectionnées au format CSV"
        )

    with col_export2:
        st.markdown(
            "Sélectionnez le jeu de données à exporter (Voyages filtrés = données appliquées aux filtres), "
            "puis cliquez sur Télécharger pour obtenir le fichier CSV."
        )