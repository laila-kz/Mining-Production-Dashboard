import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from database import fetch_data

def render_chart(fig, title, height=520):
    st.markdown(f"<div class='section-title-bar'>{title}</div>", unsafe_allow_html=True)
    html = f"<div class='chart-card'>{fig.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
    components.html(html, height=height, scrolling=True)

# --- Page configuration ---
st.set_page_config(page_title="TDB Performance Conducteurs",page_icon="🟢", layout="wide")
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

from datetime import datetime
# Dashboard header with professional style
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
    <div style='font-size:2.5rem; font-weight:700;'>TDB de Performance Conducteurs</div>
    <div style='font-size:1.2rem; margin-top:0.2rem; background: rgba(20,184,166,0.10); color:#115E59; padding:0.2rem 0.5rem; border-radius:5px;'>Module Reporting & Dashboard</div>
    <div style='margin-top:0.4rem; font-size:0.85rem; opacity:0.85;'>Date et heure : {datetime.now().strftime('%A %d %B %Y, %H:%M')}</div>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
try:
    trips = fetch_data("voyage")
    drivers = fetch_data("conducteur")
except Exception as e:
    st.error(f"Erreur lors du chargement des données: {e}")
    st.stop()

if trips.empty or drivers.empty:
    st.warning("Aucune donnée disponible pour les voyages ou conducteurs.")
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
selected_driver = st.sidebar.multiselect("Conducteur", drivers["id_conducteur"].unique())

filtered_df = trips[
    (pd.to_datetime(trips["date"]).dt.date >= date_range[0]) &
    (pd.to_datetime(trips["date"]).dt.date <= date_range[1])
]
if selected_driver:
    filtered_df = filtered_df[filtered_df["id_conducteur"].isin(selected_driver)]

if filtered_df.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()
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
# --- KPIs ---
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
    background: #FFFFFF;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 1rem;
    margin-bottom: 1.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

driver_summary = filtered_df.groupby("id_conducteur").agg(
    total_trips=pd.NamedAgg(column="id_voyage", aggfunc="count"),
    total_tons=pd.NamedAgg(column="quantite_transporte", aggfunc="sum"),
    avg_load=pd.NamedAgg(column="quantite_transporte", aggfunc="mean"),
    avg_duration=pd.NamedAgg(column="duration_hours", aggfunc="mean"),
    avg_tph=pd.NamedAgg(column="tons_per_hour", aggfunc="mean")
).reset_index()

total_trips = int(driver_summary["total_trips"].sum())
total_tons = round(driver_summary["total_tons"].sum(),2)
avg_duration = round(driver_summary["avg_duration"].mean(),2)

st.markdown(f"""
<div class='kpi-row'>
    <div class='kpi-tile'>
        <div class='label'>Nombre total de voyages par conducteur</div>
        <div class='value'>{total_trips}</div>
    </div>
    <div class='kpi-tile'>
        <div class='label'>Tonnage total transporté par conducteur</div>
        <div class='value'>{total_tons}</div>
    </div>
    <div class='kpi-tile'>
        <div class='label'>Durée moyenne par voyage (h)</div>
        <div class='value'>{avg_duration}</div>
    </div>
</div>
""", unsafe_allow_html=True)
# --- Donnees ---
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


# Conducteurs en dessous de la moyenne
special_title("Conducteurs en dessous de la moyenne")
voyage_mean = driver_summary["total_trips"].mean()
tonnage_mean = driver_summary["total_tons"].mean()
below_avg = driver_summary[(driver_summary["total_trips"] < voyage_mean) | (driver_summary["total_tons"] < tonnage_mean)]
styled_below_avg = below_avg.style.set_table_styles(
    [
        {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
        {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
        {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
        {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
    ]
).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
st.dataframe(styled_below_avg, use_container_width=True)


# Top 5 conducteurs (tonnage ou voyages)
special_title("Top 5 conducteurs (tonnage ou voyages)")
top5_voyages = driver_summary.sort_values("total_trips", ascending=False).head(5)
top5_tonnage = driver_summary.sort_values("total_tons", ascending=False).head(5)
st.markdown("**Top 5 par voyages**")
styled_top5_voyages = top5_voyages.style.set_table_styles(
    [
        {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
        {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
        {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
        {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
    ]
).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
st.dataframe(styled_top5_voyages, use_container_width=True)
st.markdown("**Top 5 par tonnage**")
styled_top5_tonnage = top5_tonnage.style.set_table_styles(
    [
        {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
        {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
        {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
        {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
    ]
).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
st.dataframe(styled_top5_tonnage, use_container_width=True)



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

# Classement conducteurs par voyages
fig_voyages = px.bar(
    driver_summary.sort_values("total_trips", ascending=False),
    x="id_conducteur",
    y="total_trips",
    title=""
)
special_title2("Classement conducteurs par voyages")
render_chart(fig_voyages,"")
# Classement conducteurs par voyages
fig_voyages = px.bar(
    driver_summary.sort_values("total_trips", ascending=False),
    x="id_conducteur",
    y="total_trips",
    title="Classement par nombre de voyages"
)
special_title2("Classement conducteurs par voyages")
render_chart(fig_voyages,"")

# Classement conducteurs par tonnage
fig_tonnage = px.bar(
    driver_summary.sort_values("total_tons", ascending=False),
    x="id_conducteur",
    y="total_tons",
    title="Classement par tonnage transporté"
)
special_title2("Classement conducteurs par tonnage")
render_chart(fig_tonnage, "")

# Évolution des performances d’un conducteur choisi
special_title2("Évolution des performances d’un conducteur choisi")
# Styled label
st.markdown("""
<div style="
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    color: black;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    display: inline-block;
    margin-bottom: 0.25rem;
">
📍 Choisir un conducteur pour l'évolution
</div>
""", unsafe_allow_html=True)

# Custom CSS for selectbox
st.markdown("""
<style>
div.stSelectbox > div[data-baseweb] {
    background-color: #0F766E;
    color: white;
    border-radius: 8px;
    padding: 0.25rem 0.5rem;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
}

div.stSelectbox div[role="listbox"] {
    background-color: #0F766E;
    color: white;
    font-weight: 500;
}

div.stSelectbox div[role="option"]:hover {
    background-color: #115E59;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Selectbox without label text
selected_perf_driver = st.selectbox(
    "",  # label is empty because we use the styled markdown above
    driver_summary["id_conducteur"].unique()
)

perf_driver_df = filtered_df[filtered_df["id_conducteur"] == selected_perf_driver]
if not perf_driver_df.empty:
    perf_by_date = perf_driver_df.groupby(pd.to_datetime(perf_driver_df["date"]).dt.date)["quantite_transporte"].sum().reset_index()
    perf_by_date.columns = ["date", "tonnage"]
    fig_perf = px.line(perf_by_date, x="date", y="tonnage", title=f"Évolution du tonnage pour le conducteur {selected_perf_driver}")
    special_title2(f"Évolution du tonnage pour le conducteur {selected_perf_driver}")
    render_chart(fig_perf,"")
    
else:
    st.info("Aucune donnée pour le conducteur sélectionné.")




# 1. Total trips per driver
fig1 = px.bar(driver_summary, x="id_conducteur", y="total_trips", title="Nombre de voyages par conducteur")
special_title2("Nombre de voyages par conducteur")
render_chart(fig1,"")



# 2. Total tons transported per driver
fig2 = px.bar(driver_summary, x="id_conducteur", y="total_tons", title="Tons transportés par conducteur")
special_title2("Tons transportés par conducteur")
render_chart(fig2,"")

# 3. Average load per trip
fig3 = px.box(filtered_df, x="id_conducteur", y="quantite_transporte", title="Charge moyenne par voyage par conducteur")
special_title2("Charge moyenne par voyage par conducteur")
render_chart(fig3,"")

# 4. Tons per hour per driver
fig4 = px.scatter(driver_summary, x="id_conducteur", y="avg_tph", size="total_trips", color="total_tons",
                  hover_data=["avg_load", "avg_duration"], title="Tons par heure par conducteur")
special_title2("Tons par heure par conducteur")
render_chart(fig4,"")

# 5. Trend of trips per driver over time
trips_per_day_driver = filtered_df.groupby([pd.to_datetime(filtered_df["date"]).dt.date, "id_conducteur"]).size().reset_index(name="trips")
if not trips_per_day_driver.empty:
    trips_per_day_driver.rename(columns={0: "date"}, inplace=True)
    fig5 = px.line(trips_per_day_driver, x="date", y="trips", color="id_conducteur", title="Tendance des voyages par conducteur")
    st.plotly_chart(fig5, use_container_width=True)

# --- Export Section ---
st.markdown("<div class='section-title-bar'>💾 Export des Données</div>", unsafe_allow_html=True)
st.markdown("---")
col_export1, col_export2 = st.columns([1, 3])
with col_export1:
    filename = f'conducteurs_{selected_perf_driver}_data.csv'
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
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name=filename,
        mime='text/csv',
        help="Télécharger les données filtrées au format CSV"
    )
with col_export2:
    total_conducteurs = len(filtered_df)
    avg_tph = round(filtered_df['tons_per_hour'].mean(), 1) if 'tons_per_hour' in filtered_df.columns and not filtered_df['tons_per_hour'].isnull().all() else 0
    st.info(f"📊 **Résumé**: {total_conducteurs} voyages analysés avec une moyenne de {avg_tph} tons/heure")
