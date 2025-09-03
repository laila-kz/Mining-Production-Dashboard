import streamlit as st
import plotly.express as px
from database import fetch_data
import pandas as pd

#page config
st.set_page_config(page_title="TDB des arrets des camions",page_icon="🟢", layout="wide")


# --- Reusable CSS Style Block ---
def inject_global_styles():
    st.markdown('''
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Roboto&display=swap" rel="stylesheet">
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
    body, .stApp { background-color: #FFFFFF !important; color: #1F2937 !important; font-family: 'Roboto', sans-serif !important; }
    
    h1, h2, h3, .stSubheader, .section-title-bar, .kpi-label, .kpi-value {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #0F766E !important;
    }
    .section-title-bar {
        background: #F6F8FA;
        border-radius: 12px;
        padding: 0.7rem 1.2rem;
        margin-bottom: 0.5rem;
        font-size: 1.25rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif !important;
        color: #0F766E;
        box-shadow: 0 2px 8px rgba(15,118,110,0.07);
        display: inline-block;
    }
    .stMarkdown, .stText, .stDataFrame, .stTable, .stPlotlyChart, .stSidebar {
        font-family: 'Roboto', sans-serif !important;
        font-size: 14px !important;
        color: #1F2937 !important;
    }
    .kpi-card {
        background: #F6F8FA;
        border-radius: 18px;
        box-shadow: 0 4px 18px rgba(15,118,110,0.10);
        padding: 1.2rem 0.5rem 1rem 0.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
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
    .stDataFrame, .stTable {
        border-radius: 12px !important;
        background: #F6F8FA !important;
        font-family: 'Roboto', sans-serif !important;
        font-size: 14px !important;
        color: #1F2937 !important;
        box-shadow: 0 2px 8px rgba(15,118,110,0.07);
        border: none !important;
    }
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
    hr {
        border: none;
        border-top: 1px solid #F6F8FA;
        margin: 0.5rem 0 1.5rem 0;
    }
    </style>
    ''', unsafe_allow_html=True)

# --- Plotly Chart Helper ---
def plotly_style(fig):
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Roboto, sans-serif", color="#1F2937"),
        colorway=["#0F766E", "#0D9488", "#14B8A6", "#F6F8FA"],
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

# --- Header Helper ---
def render_header(title, subtitle):
    st.markdown(f"""
        <div style='display: flex; align-items: center; justify-content: center; gap: 1.5rem; margin-bottom: 1.2rem;'>
            <img src='phosboucraa_logo.jpg' width='140' style='margin-bottom:0; border-radius:10px; box-shadow:0 2px 8px #0F766E;'>
            <div style='display: flex; flex-direction: column; align-items: center; justify-content: center;'>
                <div style='font-size:2rem; font-weight:700; color:#0F766E; font-family:Poppins,sans-serif; text-align:center; margin-bottom:0.1rem;'>
                    {title}
                </div>
                <div style='font-size:1rem; color:#1F2937; font-family:Roboto,sans-serif; font-style:italic; text-align:center;'>
                    {subtitle}
                </div>
            </div>
        </div>
        <hr>
    """, unsafe_allow_html=True)

def main():
    # Page configuration (must be called before any Streamlit output)
    st.set_page_config(page_title="Arrêts Camions Dashboard", layout="wide")
    # Inject global CSS/styles early
    inject_global_styles()
    # --- Header Section ---
    from datetime import datetime
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
    <div style='font-size:2.5rem; font-weight:700;'>TDB des Arrêts Camions</div>
    <div style='font-size:1.2rem; margin-top:0.2rem; background: rgba(20,184,166,0.10); color:#115E59; padding:0.2rem 0.5rem; border-radius:5px;'>Module Reporting & Dashboard</div>
    <div style='margin-top:0.4rem; font-size:0.85rem; opacity:0.85;'>Date et heure : {datetime.now().strftime('%A %d %B %Y, %H:%M')}</div>
</div>
""", unsafe_allow_html=True)

    # --- Fonts & Styling ---

    # Fetch data
    df = fetch_data("arret")

    # Debug: Show initial data info
    st.sidebar.markdown("### 🔍 Debug Info")
    st.sidebar.info(f"**Raw data loaded**: {len(df)} rows")

    # Create a working copy for filtering
    df_filtered = df.copy()

    # Sidebar for filters
    with st.sidebar:
        st.markdown("### 🔍 Filtres")
        st.markdown("---")
        
        # Filter by truck
        truck_ids = df_filtered["id_camion"].unique() if "id_camion" in df_filtered.columns else []
        selected_truck = st.selectbox(
            "**Camion**",
            options=["Tous les camions"] + list(truck_ids),
            help="Sélectionnez un camion spécifique ou tous les camions"
        )
        
        # Initialize date variables
        start_date = None
        end_date = None
        
        # Date filter (optional - disabled by default to show all data)
        show_date_filter = st.checkbox("📅 Activer le filtre par date", value=False)
        
        if show_date_filter and "date_heure" in df_filtered.columns and not df_filtered.empty:
            try:
                df_filtered["date_heure"] = pd.to_datetime(df_filtered["date_heure"])
                date_min = df_filtered["date_heure"].min().to_pydatetime()
                date_max = df_filtered["date_heure"].max().to_pydatetime()
                
                st.markdown("**Période**")
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Début", value=date_min.date())
                with col2:
                    end_date = st.date_input("Fin", value=date_max.date())
                
                # Convert to datetime for filtering
                start_datetime = pd.Timestamp(start_date)
                end_datetime = pd.Timestamp(end_date)
                
                # Apply date filter and show debug info
                before_filter = len(df_filtered)
                df_filtered = df_filtered[(df_filtered["date_heure"] >= start_datetime) & (df_filtered["date_heure"] <= end_datetime)]
                after_filter = len(df_filtered)
                
                st.sidebar.info(f"**Date filter**: {before_filter} → {after_filter} rows")
                
            except Exception as e:
                st.error(f"Erreur lors du filtrage par date: {e}")
                st.sidebar.error("Date filtering failed - showing all data")
        else:
            st.sidebar.info("📅 Date filter disabled - showing all data")

    # Apply truck filter
    if selected_truck != "Tous les camions" and not df_filtered.empty:
        before_truck_filter = len(df_filtered)
        df_filtered = df_filtered[df_filtered["id_camion"] == selected_truck]
        after_truck_filter = len(df_filtered)
        st.sidebar.info(f"**Truck filter**: {before_truck_filter} → {after_truck_filter} rows")

    # Show data info in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📊 Informations")
        st.info(f"**Données totales**: {len(df)} enregistrements")
        st.info(f"**Données filtrées**: {len(df_filtered)} enregistrements")
        
        if len(df_filtered) == 0 and len(df) > 0:
            st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés")
            col1, col2 = st.columns(2)
            with col1:
                st.button("🔄 Réinitialiser les filtres", on_click=lambda: st.rerun())
            with col2:
                if st.button("📊 Afficher toutes les données"):
                    df_filtered = df.copy()
                    st.rerun()

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
    .chart-card {
    background: #FFFFFF;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 1rem;
    margin-bottom: 1.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)   
    # Example explicit KPI section title (keeps backward compatibility)
    st.markdown("<div class='kpi-section-title'>🧾Indicateurs clés</div>", unsafe_allow_html=True)

    # Main content area
    if not df_filtered.empty:
    # KPIs Section
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
            </style>
            """,
            unsafe_allow_html=True
        )
        total_arrets = len(df_filtered)
        import re
        def duree_to_seconds(duree_str):
            # Accepts 'H:M:S' or 'M:S' or 'S' format
            if pd.isnull(duree_str):
                return None
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
                return None
            return None

        avg_duree = None
        total_duree = None
        if "duree" in df_filtered.columns:
            df_filtered["duree_seconds"] = df_filtered["duree"].apply(duree_to_seconds)
            avg_duree = df_filtered["duree_seconds"].mean()
            total_duree = df_filtered["duree_seconds"].sum()
        st.markdown(f"""
        <div class='kpi-row'>
            <div class='kpi-tile'>
                <div class='label'>Nombre d'arrêts</div>
                <div class='value'>{total_arrets:,}</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Durée moyenne par arrêt</div>
                <div class='value'>{round(avg_duree/60, 2) if avg_duree is not None else 'N/A'} h</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Total heures perdues</div>
                <div class='value'>{round(total_duree/3600, 2) if total_duree is not None else 'N/A'} h</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
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
        # Data table
        st.markdown("<div style='margin-top: 3rem;'><div class='section-title-bar'>📋 Données</div></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Display the full table
        styled_df = df_filtered.style.set_table_styles(
            [
                {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
                {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
                {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
            ]
        ).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
        st.dataframe(styled_df, use_container_width=True)
        
        # Show table info
        st.info(f"📊 Affichage de {len(df_filtered)} lignes sur {len(df)} total")

        
        st.markdown("---")

        # Ensure truck_counts and cause_counts exist before using them
        if "id_camion" in df_filtered.columns and not df_filtered.empty:
            truck_counts = df_filtered["id_camion"].value_counts().reset_index()
            truck_counts.columns = ["Camion", "Nombre d'arrêts"]
        else:
            truck_counts = pd.DataFrame(columns=["Camion", "Nombre d'arrêts"])

        if "cause" in df_filtered.columns and not df_filtered.empty:
            cause_counts = df_filtered["cause"].value_counts().reset_index()
            cause_counts.columns = ["Cause", "Nombre d'arrêts"]
        else:
            cause_counts = pd.DataFrame(columns=["Cause", "Nombre d'arrêts"])

        # Top 5 camions avec le plus d’arrêts
        if not truck_counts.empty:
            top_trucks = truck_counts.head(5)
            special_title("Top 5 Camions avec le plus d’arrêts")
            styled_trucks = top_trucks.style.set_table_styles(
                [
                    {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
                    {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
                    {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
                ]
            ).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
            st.dataframe(styled_trucks, use_container_width=True)
        else:
            st.info("Aucun camion disponible pour ce filtre.")

        # Top 5 causes d’arrêt
        if not cause_counts.empty:
            top_causes = cause_counts.head(5)
            st.subheader("Top 5 Causes d’arrêt")
            styled_causes = top_causes.style.set_table_styles(
                [
                    {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
                    {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
                    {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
                ]
            ).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
            st.dataframe(styled_causes, use_container_width=True)
        else:
            st.info("Aucune cause d'arrêt disponible pour ce filtre.")
        
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
        

        # Charts Section
        st.markdown("<div class='section-title-bar'>📈 Visualisations</div>", unsafe_allow_html=True)
        st.markdown("---")
        import streamlit.components.v1 as components
        def render_chart(fig, title, height=520):
            special_title2(title)
            
            html = f"<div class='chart-card'>{fig.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
            components.html(html, height=height, scrolling=True)

        # Evolution du temps d’arrêt par semaine/mois
        if "date_heure" in df_filtered.columns and "duree_seconds" in df_filtered.columns:
            df_filtered["date_heure"] = pd.to_datetime(df_filtered["date_heure"])
            df_filtered["semaine"] = df_filtered["date_heure"].dt.isocalendar().week
            weekly_downtime = df_filtered.groupby("semaine")["duree_seconds"].sum().reset_index()
            weekly_downtime["heures"] = weekly_downtime["duree_seconds"] / 3600
            fig_week = px.line(weekly_downtime, x="semaine", y="heures", title=None)
            fig_week = plotly_style(fig_week)
            render_chart(fig_week, "Evolution du temps d'arrêt par semaine", height=420)
            df_filtered["mois"] = df_filtered["date_heure"].dt.month
            monthly_downtime = df_filtered.groupby("mois")["duree_seconds"].sum().reset_index()
            monthly_downtime["heures"] = monthly_downtime["duree_seconds"] / 3600
            fig_month = px.line(monthly_downtime, x="mois", y="heures", title=None)
            fig_month = plotly_style(fig_month)
            render_chart(fig_month, "Evolution du temps d'arrêt par mois", height=420)

        # Répartition des causes d’arrêt (pie chart)
        if "cause" in df_filtered.columns:
            cause_counts = df_filtered["cause"].value_counts().reset_index()
            cause_counts.columns = ["Cause", "Nombre d'arrêts"]
            fig_cause = px.pie(cause_counts, names="Cause", values="Nombre d'arrêts", title=None, color_discrete_sequence=["#0F766E", "#0D9488", "#14B8A6"])
            fig_cause = plotly_style(fig_cause)
            render_chart(fig_cause, "Répartition des causes d'arrêt", height=420)
            special_title2("Répartition des causes d'arrêt")

        # Nombre d’arrêts par camion (bar chart)
        if "id_camion" in df_filtered.columns:
            truck_counts = df_filtered["id_camion"].value_counts().reset_index()
            truck_counts.columns = ["Camion", "Nombre d'arrêts"]
            fig_truck = px.bar(truck_counts, x="Camion", y="Nombre d'arrêts", title=None)
            fig_truck = plotly_style(fig_truck)
            render_chart(fig_truck, "Nombre d'arrêts par camion", height=420)
            

        
        
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        with col1:
            import streamlit.components.v1 as components

            def render_chart(fig, title, height=520):
                special_title2(title)
                
                html = f"<div class='chart-card'>{fig.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
                components.html(html, height=height, scrolling=True)

            # Graph: stops per truck
            if "id_camion" in df_filtered.columns:
                truck_counts = df_filtered["id_camion"].value_counts().reset_index()
                truck_counts.columns = ["Camion", "Nombre d'arrêts"]
                fig = px.bar(
                    truck_counts,
                    x="Camion",
                    y="Nombre d'arrêts",
                    color="Nombre d'arrêts",
                    color_continuous_scale=["#0F766E", "#0D9488", "#14B8A6"]
                )
                fig.update_layout(showlegend=False, title=None)
                fig = plotly_style(fig)
                render_chart(fig, "Répartition des arrêts par camion", height=420)
        with col2:
            # Graph: stops by type
            if "type" in df_filtered.columns:
                type_counts = df_filtered["type"].value_counts().reset_index()
                type_counts.columns = ["Type", "Nombre d'arrêts"]
                fig2 = px.pie(
                    type_counts,
                    names="Type",
                    values="Nombre d'arrêts",
                    color_discrete_sequence=["#0F766E", "#0D9488", "#14B8A6"]
                )
                fig2.update_layout(title=None)
                fig2 = plotly_style(fig2)
                render_chart(fig2,"Répartition des arrêts par type", height=420)
                

        # Export Section
        st.markdown("<div class='section-title-bar'>💾 Export des Données</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        col_export1, col_export2 = st.columns([1, 3])
        with col_export1:
            # Create filename with date info if available
            if start_date and end_date:
                filename = f'arrets_{selected_truck.replace(" ", "_")}_{start_date}_{end_date}.csv'
            else:
                filename = f'arrets_{selected_truck.replace(" ", "_")}_all_data.csv'
            
            st.markdown("""
            <style>
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
                data=df_filtered.to_csv(index=False).encode('utf-8'),
                file_name=filename,
                mime='text/csv',
                help="Télécharger les données filtrées au format CSV"
            )
        with col_export2:
            if start_date and end_date:
                st.info(f"📊 **Résumé**: {total_arrets} arrêts analysés pour la période du {start_date} au {end_date}")
            else:
                st.info(f"📊 **Résumé**: {total_arrets} arrêts analysés")

    else:
        st.warning("⚠️ Aucune donnée disponible pour les critères sélectionnés.")
        st.info("💡 Essayez de modifier les filtres pour voir plus de données.")

if __name__ == "__main__":
    main()
