import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import get_connection



st.set_page_config(
    page_title="Système de Gestion Minière - Phosboucraa",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&family=Roboto&display=swap" rel="stylesheet">
<style>
  html, body, [class*="css"] { font-family: 'Roboto', sans-serif !important; font-size: 14px !important; }
  h1, h2, h3, .dashboard-title { font-family: 'Poppins', sans-serif !important; font-weight: 700 !important; }
  .stButton>button { background-color: #0F766E !important; color: #fff !important; border-radius: 8px !important; font-weight: 600 !important; border: none; padding: 0.6em 1.2em; }
  .stButton>button:hover { background-color: #115e59 !important; }
  .dashboard-card { background-color: #F6F8FA; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);}
  .dashboard-card h4 { color: #0F766E; font-weight: 600; }
  .dashboard-card p, .dashboard-card li { font-size: 0.95rem; margin: 0.2rem 0; }
  body, .stApp {
    background-color: #f9fafb !important;
    background-image: radial-gradient(#d1d5db 1px, transparent 1px) !important;
    background-size: 20px 20px !important;
  }
  /* Sidebar container */
  section[data-testid="stSidebar"] {
    background: #f9fafb !important;
  }
  /* Sidebar title */
  section[data-testid="stSidebar"] h1,
  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    color: #0F766E !important;
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
</style>
""", unsafe_allow_html=True)



# Professional font setup via Google Fonts
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&family=Roboto&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif !important;
            font-size: 14px !important;
            font-weight: 400 !important;
        }
        h1, h2, h3, .dashboard-title, .kpi-header {
            font-family: 'Poppins', sans-serif !important;
            font-size: 22px !important;
            font-weight: 700 !important;
        }
        .section-title-bar, .stSubheader, .chart-title {
            font-family: 'Poppins', sans-serif !important;
            font-size: 18px !important;
            font-weight: 500 !important;
        }
        .stButton>button {
            background-color: #0F766E !important;
            color: #fff !important;
            border-radius: 8px !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            border: none;
            padding: 0.6em 1.2em;
        }
        .stButton>button:hover {
            background-color: #115e59 !important;
        }
        .stMarkdown, .stText, .stHeader, .stSubheader {
            color: #1F2937 !important;
        }
        .stDataFrame, .stTable {
            background-color: #F6F8FA !important;
            color: #1F2937 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Header with centered title and background
st.image("assets/phosboucraa_logo.jpg", width=120)
st.markdown(f"""
<div style="
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(90deg, #0F766E, #115E59);
    color: white;
    padding: 2rem 1rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    margin-bottom: 2rem;
">
    <img src='assets/phosboucraa_logo.jpg' width='120' style='border-radius:10px; margin-bottom:1rem; box-shadow:0 2px 8px rgba(0,0,0,0.2);'>
    <div style='font-size:3.5rem; font-weight:700;'>Système de Gestion de la Production Minière</div>
    <div style='font-size:1.5rem; font-style:italic; margin-top:0.3rem;'>Module Reporting & Dashboard</div>
    <div style='margin-top:0.5rem; font-size:0.9rem; opacity:0.85;'>Date et heure actuelles : {datetime.now().strftime('%A %d %B %Y, %H:%M')}</div>
</div>
""", unsafe_allow_html=True)

# Current date & time
now = datetime.now().strftime('%A %d %B %Y, %H:%M')
st.write(f"**Date et heure actuelles :** {now}")


# User (optional)
user = st.session_state.get('user', None)
if user:
    st.write(f"**Utilisateur :** {user}")

# Quick Navigation Tiles / Cards
st.markdown("---")
st.subheader("Accès rapide aux Tableaux de Bord")
nav_cols = st.columns(5)
dashboards = [
    {"label": "🚛 TDB Voyages", "path": "pages/TDB_des_voyages.py"},
    {"label": "🧪 TDB Qualités", "path": "pages/TDB_des_qualite.py"},
    {"label": "🛑 TDB Arrêts Camions", "path": "pages/TDB_des_arret_camions.py"},
    {"label": "👨‍💼 TDB Performance Conducteurs", "path": "pages/TDB_de_performance_des_conducteurs.py"},
    {"label": "🚚 TDB Performance Camions", "path": "pages/TDB_de_performance_des_camions.py"},
]
# CSS for uniform tiles
st.markdown("""
<style>
/* Ensure columns have equal horizontal padding (equal spacing between tiles) */
[data-testid="column"] {
    padding-left: 0.6rem;
    padding-right: 0.6rem;
}

/* Make Streamlit buttons fill their column and have a fixed, identical height */
.stButton>button {
    width: 100% !important;
    height: 88px !important;                /* uniform height for all tiles */
    min-height: 88px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px !important;
    padding: 0.25rem 0.75rem !important;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1rem !important;
    transition: transform 0.15s ease-in-out, background-color 0.15s ease-in-out;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

/* Hover effect */
.stButton>button:hover {
    transform: translateY(-3px);
}

/* Optionally style the first row of buttons (dashboard nav) differently */
.stButton>button:active {
    transform: translateY(0);
}

/* If you also want a colored tile look for these buttons, set background here */
.stButton>button {
    background-color: #0F766E !important;
    color: #ffffff !important;
}

/* Ensure the text inside doesn't wrap and stays centered */
.stButton>button > div, .stButton>button > span {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}

/* Smaller vertical gap between rows of columns (if tiles wrap to next row) */
.row-widget.stButton {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)
for i, dash in enumerate(dashboards):
    with nav_cols[i]:
        if st.button(dash["label"]):
            st.switch_page(dash["path"])



@st.cache_data
def load_summary_data():
    """Load summary data for the home dashboard"""
    conn = get_connection()
    
    # Get basic counts
    summary = {}
    
    # Voyages
    voyages_df = pd.read_sql_query("SELECT COUNT(*) as count FROM voyage", conn)
    summary['total_voyages'] = voyages_df['count'].iloc[0] if not voyages_df.empty else 0
    
    # Conducteurs
    conducteurs_df = pd.read_sql_query("SELECT COUNT(*) as count FROM conducteur", conn)
    summary['total_conducteurs'] = conducteurs_df['count'].iloc[0] if not conducteurs_df.empty else 0
    
    # Camions
    camions_df = pd.read_sql_query("SELECT COUNT(*) as count FROM camion", conn)
    summary['total_camions'] = camions_df['count'].iloc[0] if not camions_df.empty else 0
    
    # Arrêts
    arrets_df = pd.read_sql_query("SELECT COUNT(*) as count FROM arret", conn)
    summary['total_arrets'] = arrets_df['count'].iloc[0] if not arrets_df.empty else 0
    
    # Recent activity
    recent_voyages = pd.read_sql_query("""
        SELECT DATE(date) as date, COUNT(*) as count 
        FROM voyage 
        WHERE date >= date('now', '-30 days')
        GROUP BY DATE(date)
        ORDER BY date
    """, conn)
    
    conn.close()
    
    return summary, recent_voyages

# Load data
summary, recent_activity = load_summary_data()


# Global KPIs (Summary cards)
import os
import numpy as np

# Load additional data for KPIs
voyage_path = os.path.join('data', 'voyage.csv')
qualite_path = os.path.join('data', 'qualite.csv')
arret_path = os.path.join('data', 'arret.csv')
conducteur_path = os.path.join('data', 'conducteur.csv')
camion_path = os.path.join('data', 'camion.csv')

voyage_df = pd.read_csv(voyage_path) if os.path.exists(voyage_path) else pd.DataFrame()
qualite_df = pd.read_csv(qualite_path) if os.path.exists(qualite_path) else pd.DataFrame()
arret_df = pd.read_csv(arret_path) if os.path.exists(arret_path) else pd.DataFrame()
conducteur_df = pd.read_csv(conducteur_path) if os.path.exists(conducteur_path) else pd.DataFrame()
camion_df = pd.read_csv(camion_path) if os.path.exists(camion_path) else pd.DataFrame()

# KPIs calculations
total_voyages = len(voyage_df)
total_tonnage = voyage_df['quantite_transporte'].sum() if 'quantite_transporte' in voyage_df.columns else 0
mean_phosphate = qualite_df['taux_phosphate'].mean() if 'taux_phosphate' in qualite_df.columns else np.nan
mean_humidite = qualite_df['humidite'].mean() if 'humidite' in qualite_df.columns else np.nan
total_arret_heures = 0
if 'duree' in arret_df.columns:
    # Assume 'duree' is in format HH:MM:SS or minutes
    def to_hours(val):
        if isinstance(val, str):
            parts = val.split(':')
            if len(parts) == 3:
                return int(parts[0]) + int(parts[1])/60 + int(parts[2])/3600
            elif len(parts) == 2:
                return int(parts[0]) + int(parts[1])/60
            else:
                try:
                    return float(val)/60
                except:
                    return 0
        try:
            return float(val)/60
        except:
            return 0
    total_arret_heures = arret_df['duree'].apply(to_hours).sum()
active_conducteurs = len(conducteur_df[conducteur_df['actif'] == 1]) if 'actif' in conducteur_df.columns else len(conducteur_df)
active_camions = len(camion_df[camion_df['actif'] == 1]) if 'actif' in camion_df.columns else len(camion_df)

st.header("🌍 Vue Globale de l'Opération Minière")

# Professional KPI card styles
st.markdown(
    """
    <style>
    .kpi-grid { display:flex; gap:16px; align-items:stretch; margin-bottom:12px; }
    .kpi-card {
        flex:1;
        background: linear-gradient(180deg, #FFFFFF 0%, #F7FAFC 100%);
        border-radius:12px;
        padding:14px 16px;
        box-shadow: 0 6px 18px rgba(15, 118, 110, 0.08);
        border: 1px solid rgba(15,118,110,0.06);
        min-height:110px;
        display:flex;
        flex-direction:column;
        justify-content:space-between;
    }
    .kpi-top { display:flex; align-items:center; gap:12px; }
    .kpi-icon {
        width:48px; height:48px; border-radius:10px;
        display:flex; align-items:center; justify-content:center;
        font-size:20px; color:#fff;
    }
    .icon-green { background: linear-gradient(90deg,#0F766E,#115E59); box-shadow: 0 4px 10px rgba(17,94,89,0.08); }
    .icon-blue  { background: linear-gradient(90deg,#0EA5E9,#0369A1); box-shadow: 0 4px 10px rgba(3,105,161,0.08); }
    .icon-amber { background: linear-gradient(90deg,#F59E0B,#D97706); box-shadow: 0 4px 10px rgba(217,119,6,0.08); }
    .kpi-label { font-size:13px; color:#0f172a; font-weight:700; }
    .kpi-value { font-size:26px; font-weight:800; color:#0f172a; margin-top:6px; }
    .kpi-meta { font-size:12px; color:#6b7280; margin-top:6px; }
    .kpi-small { font-size:13px; color:#374151; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Format values
_fmt_int = lambda v: f"{int(v):,}" if pd.notna(v) else "0"
_fmt_ton = lambda v: f"{v:,.0f} t" if pd.notna(v) else "0 t"
_fmt_pct = lambda v: (f"{v:.2f}%" if (v is not None and not np.isnan(v)) else "N/A")
_fmt_hours = lambda v: (f"{v:.1f} h" if pd.notna(v) else "0.0 h")

# KPI grid (3 columns, each with two neat cards)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
      <div>
        <div class="kpi-top">
          <div class="kpi-icon icon-green">🚛</div>
          <div>
            <div class="kpi-label">Total Voyages</div>
            <div class="kpi-value">{_fmt_int(total_voyages)}</div>
          </div>
        </div>
        <div class="kpi-meta">Nombre total d'opérations de transport enregistrées</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-card" style="margin-top:10px;">
      <div>
        <div class="kpi-top">
          <div class="kpi-icon icon-blue">⛏️</div>
          <div>
            <div class="kpi-label">Total tonnage transporté</div>
            <div class="kpi-value">{_fmt_ton(total_tonnage)}</div>
          </div>
        </div>
        <div class="kpi-meta">Tonnage cumulé enregistré dans les voyages</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
      <div>
        <div class="kpi-top">
          <div class="kpi-icon icon-amber">🧪</div>
          <div>
            <div class="kpi-label">Moy. taux de phosphate</div>
            <div class="kpi-value">{_fmt_pct(mean_phosphate)}</div>
          </div>
        </div>
        <div class="kpi-meta">Qualité moyenne mesurée sur les échantillons</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-card" style="margin-top:10px;">
      <div>
        <div class="kpi-top">
          <div class="kpi-icon icon-blue">💧</div>
          <div>
            <div class="kpi-label">Moy. humidité</div>
            <div class="kpi-value">{_fmt_pct(mean_humidite)}</div>
          </div>
        </div>
        <div class="kpi-meta">Humidité moyenne des prélèvements</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
      <div>
        <div class="kpi-top">
          <div class="kpi-icon icon-amber">⏱️</div>
          <div>
            <div class="kpi-label">Total heures d’arrêts</div>
            <div class="kpi-value">{_fmt_hours(total_arret_heures)}</div>
          </div>
        </div>
        <div class="kpi-meta">Somme des durées d'immobilisation des camions</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-card" style="margin-top:10px;">
      <div>
        <div class="kpi-top">
          <div class="kpi-icon icon-green">🚜</div>
          <div>
            <div class="kpi-label">Camions actifs</div>
            <div class="kpi-value">{_fmt_int(active_camions)}</div>
          </div>
        </div>
        <div class="kpi-meta">Véhicules marqués comme actifs dans la flotte</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Recent Activity Chart
if not recent_activity.empty:
    st.subheader("📈 Activité des 30 Derniers Jours")
    
    fig_activity = px.line(
        recent_activity,
        x='date',
        y='count',
        title="Nombre de voyages par jour",
        markers=True
    )
    fig_activity.update_layout(
        xaxis_title="Date",
        yaxis_title="Nombre de voyages",
        height=400
    )
    st.plotly_chart(fig_activity, use_container_width=True)

# Dashboard Navigation
st.header("🎯 Tableaux de Bord Disponibles")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <style>
        .dash-grid { display:flex; flex-direction:column; gap:14px; }
        .dash-card {
            background: linear-gradient(180deg, #ffffff 0%, #fbfcfd 100%);
            border: 1px solid rgba(15,118,110,0.06);
            border-radius: 12px;
            padding: 14px;
            box-shadow: 0 8px 24px rgba(15,118,110,0.04);
            transition: transform 0.14s ease, box-shadow 0.14s ease;
        }
        .dash-card:hover { transform: translateY(-6px); box-shadow: 0 14px 40px rgba(15,118,110,0.08); }
        .dash-header { display:flex; gap:12px; align-items:center; }
        .dash-icon {
            width:48px; height:48px; border-radius:10px;
            display:flex; align-items:center; justify-content:center;
            font-size:22px; color:#fff;
        }
        .accent-green { background: linear-gradient(90deg,#0F766E,#115E59); }
        .accent-blue  { background: linear-gradient(90deg,#0EA5E9,#0369A1); }
        .dash-title { font-weight:700; font-size:16px; color:#0f172a; }
        .dash-desc { color:#475569; margin-top:8px; font-size:13px; line-height:1.35; }
        .dash-list { margin:8px 0 0 1rem; color:#374151; font-size:13px; }
        .dash-meta { margin-top:10px; font-size:12px; color:#6b7280; display:flex; justify-content:space-between; align-items:center; }
        .dash-open { background:transparent; color:#0F766E; font-weight:700; border:none; cursor:pointer; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="dash-grid">
          <div class="dash-card">
            <div class="dash-header">
              <div class="dash-icon accent-green">🚛</div>
              <div>
                <div class="dash-title">TDB des Voyages</div>
                <div class="dash-desc">Suivi des trajets, distances parcourues et performance des livraisons — utile pour optimiser les rotations et réduire les coûts.</div>
              </div>
            </div>
            <ul class="dash-list">
              <li>Analyse des trajets quotidiens</li>
              <li>Métriques distance / durée</li>
              <li>Performance par site</li>
            </ul>
            <div class="dash-meta">
              <span>Dernière mise à jour : {last}</span>
            </div>
          </div>
          
          <div class="dash-card">
            <div class="dash-header">
              <div class="dash-icon accent-blue">🧪</div>
              <div>
                <div class="dash-title">TDB des Qualités</div>
                <div class="dash-desc">Contrôle qualité des matériaux extraits et transportés, avec tendances du taux de phosphate et humidité.</div>
              </div>
            </div>
            <ul class="dash-list">
              <li>Taux de phosphate</li>
              <li>Contrôle humidité</li>
              <li>Analyse granulométrique</li>
            </ul>
            <div class="dash-meta">
              <span>Sources : échantillons & labo</span>
            </div>
          </div>

          <div class="dash-card">
            <div class="dash-header">
              <div class="dash-icon accent-green">🛑</div>
              <div>
                <div class="dash-title">TDB des Arrêts Camions</div>
                <div class="dash-desc">Monitoring des interruptions, typologie des arrêts et durée — indispensable pour la maintenance prédictive.</div>
              </div>
            </div>
            <ul class="dash-list">
              <li>Types d'arrêts</li>
              <li>Durées d'immobilisation</li>
              <li>Planification maintenance</li>
            </ul>
            <div class="dash-meta">
              <span>Action requise : vérifier incidents récents</span>
            </div>
          </div>
        </div>
        """.format(last=datetime.now().strftime("%d/%m/%Y %H:%M")),
        unsafe_allow_html=True,
    )

   


with col2:
    st.markdown(
        """
        <style>
        /* keep styles scoped to the right column cards (re-using same classes for consistency) */
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="dash-grid">
          <div class="dash-card">
            <div class="dash-header">
              <div class="dash-icon accent-green">👨‍💼</div>
              <div>
                <div class="dash-title">TDB Performance Conducteurs</div>
                <div class="dash-desc">Évaluation et suivi des performances individuelles pour formation ciblée et amélioration continue.</div>
              </div>
            </div>
            <ul class="dash-list">
              <li>Scores de performance</li>
              <li>Efficacité de conduite</li>
              <li>Recommandations formation</li>
            </ul>
            <div class="dash-meta">
              <span>Confidentialité : niveaux d'accès appliqués</span>
            </div>
          </div>

          <div class="dash-card">
            <div class="dash-header">
              <div class="dash-icon accent-blue">🚚</div>
              <div>
                <div class="dash-title">TDB Performance Camions</div>
                <div class="dash-desc">Vue centrale sur l'utilisation, l'efficacité énergétique et les coûts opérationnels de la flotte.</div>
              </div>
            </div>
            <ul class="dash-list">
              <li>Utilisation des véhicules</li>
              <li>Efficacité énergétique</li>
              <li>Coûts opérationnels</li>
            </ul>
            <div class="dash-meta">
              <span>Inclut historiques & tendances</span>
            </div>
          </div>

          <div class="dash-card">
            <div class="dash-header">
              <div class="dash-icon accent-green">📋</div>
              <div>
                <div class="dash-title">Informations Système</div>
                <div class="dash-desc">Résumé rapide de la version, état de la base et outils utilisés pour ce dashboard.</div>
              </div>
            </div>
            <div style="margin-top:10px; color:#374151; font-size:13px;">
              <p style="margin:2px 0;"><strong>Version:</strong> 1.0.0</p>
              <p style="margin:2px 0;"><strong>Dernière MAJ:</strong> {last}</p>
              <p style="margin:2px 0;"><strong>Base de données:</strong> SQLite</p>
              <p style="margin:2px 0;"><strong>Framework:</strong> Streamlit</p>
            </div>
            <div class="dash-meta">
              <span style="color:#0F766E; font-weight:600;">État : opérationnel</span>
            </div>
          </div>
        </div>
        """.format(last=datetime.now().strftime("%d/%m/%Y %H:%M")),
        unsafe_allow_html=True,
    )

    

# Navigation Instructions
st.markdown("---")
st.info("""
💡 **Comment naviguer:**
- Utilisez la barre latérale pour accéder aux différents tableaux de bord
- Chaque dashboard offre des filtres personnalisables
- Les données peuvent être exportées en format CSV
- Les graphiques sont interactifs (zoom, sélection, etc.)
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>🏭 <strong>Phosboucraa</strong> - Système de Gestion Minière</p>
    <p>Développé pour l'optimisation des opérations de production</p>
</div>
""", unsafe_allow_html=True)
