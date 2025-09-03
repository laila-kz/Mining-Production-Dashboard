import streamlit as st
import plotly.express as px
from database import fetch_data
import pandas as pd

# --- Reusable CSS Style Block ---
def inject_global_styles():
    st.markdown("""
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
    body, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #f3f4f6 !important;
    }
    [data-testid="stBlock"] {
        background: white !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    body, .stApp {
        color: #1F2937 !important;
        font-family: 'Roboto', sans-serif !important;
    }
    h1, h2, h3, .stSubheader, .section-title-bar, .kpi-label, .kpi-value {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #0F766E !important;
    }
    .section-title-bar {
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
    """, unsafe_allow_html=True)

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



def main():
    # Inject custom KPI styles and apply them to all page section titles
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
        unsafe_allow_html=True,
    )
    
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
    <div style='font-size:2.5rem; font-weight:700;'>TDB des Voyages</div>
    <div style='font-size:1.2rem; margin-top:0.2rem; background: rgba(20,184,166,0.10); color:#115E59; padding:0.2rem 0.5rem; border-radius:5px;'>Module Reporting & Dashboard</div>
    <div style='margin-top:0.4rem; font-size:0.85rem; opacity:0.85;'>Date et heure : {datetime.now().strftime('%A %d %B %Y, %H:%M')}</div>
</div>
""", unsafe_allow_html=True)
    # Page configuration
    st.set_page_config(page_title="Voyages Dashboard",page_icon="🟢", layout="wide")

    inject_global_styles()
    
    # Fetch data
    df = fetch_data("voyage")

    # Sidebar for filters
    with st.sidebar:
        st.markdown("### 🔍 Filtres")
        st.markdown("---")
        
        # Filter by trip ID
        trip_ids = df["id_voyage"].unique() if "id_voyage" in df.columns else []
        selected_trip = st.selectbox(
            "**Voyage**",
            options=["Tous les voyages"] + list(trip_ids),
            help="Sélectionnez un voyage spécifique ou tous les voyages"
        )
        
        # Filter by truck
        if "id_camion" in df.columns:
            truck_options = df["id_camion"].unique()
            selected_truck = st.selectbox(
                "**Camion**",
                options=["Tous les camions"] + list(truck_options),
                help="Filtrer par camion"
            )
        
        # Filter by driver
        if "id_conducteur" in df.columns:
            driver_options = df["id_conducteur"].unique()
            selected_driver = st.selectbox(
                "**Conducteur**",
                options=["Tous les conducteurs"] + list(driver_options),
                help="Filtrer par conducteur"
            )
        
        # Filter by status
        if "statut" in df.columns:
            status_options = df["statut"].unique()
            selected_status = st.selectbox(
                "**Statut du voyage**",
                options=["Tous les statuts"] + list(status_options),
                help="Filtrer par statut du voyage"
            )
        
        # Initialize date variables
        start_date = None
        end_date = None
        
        # Date filter
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            date_min = df["date"].min().to_pydatetime()
            date_max = df["date"].max().to_pydatetime()
            
            st.markdown("**Période de départ**")
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Début", value=date_min.date())
            with col2:
                end_date = st.date_input("Fin", value=date_max.date())
            
            # Convert to datetime for filtering
            start_datetime = pd.Timestamp(start_date)
            end_datetime = pd.Timestamp(end_date)
            df = df[(df["date"] >= start_datetime) & (df["date"] <= end_datetime)]
        
        # Distance range filter
        if "distance" in df.columns:
            st.markdown("**Distance (km)**")
            min_distance = float(df["distance"].min())
            max_distance = float(df["distance"].max())
            distance_range = st.slider(
                "Plage de distance",
                min_value=min_distance,
                max_value=max_distance,
                value=(min_distance, max_distance),
                help="Sélectionnez une plage de distance"
            )

    # Apply filters
    if selected_trip != "Tous les voyages":
        df = df[df["id_voyage"] == selected_trip]
    if "id_camion" in df.columns and selected_truck != "Tous les camions":
        df = df[df["id_camion"] == selected_truck]
    if "id_conducteur" in df.columns and selected_driver != "Tous les conducteurs":
        df = df[df["id_conducteur"] == selected_driver]
    if "statut" in df.columns and selected_status != "Tous les statuts":
        df = df[df["statut"] == selected_status]
    if "distance" in df.columns:
        df = df[(df["distance"] >= distance_range[0]) & (df["distance"] <= distance_range[1])]


    # Main content area
    if not df.empty:
        # Convert duree to numeric (minutes) if needed
        import re
        def duree_to_minutes(duree_str):
            if pd.isnull(duree_str):
                return None
            parts = re.split(r":", str(duree_str))
            try:
                if len(parts) == 3:
                    h, m, s = map(int, parts)
                    return h*60 + m + s/60
                elif len(parts) == 2:
                    m, s = map(int, parts)
                    return m + s/60
                elif len(parts) == 1:
                    return int(parts[0])
            except Exception:
                return None
            return None
        if "duree" in df.columns:
            df["duree_min"] = df["duree"].apply(duree_to_minutes)

        # KPIs Section
        st.markdown("<div class='section-title-bar'>🧾Indicateurs clés</div>", unsafe_allow_html=True)
        st.markdown("---")
        

        today = pd.Timestamp.today().date()
        this_month = pd.Timestamp.today().month
        

        total_voyages = len(df)
        voyages_today = len(df[df["date"].dt.date == today]) if "date" in df.columns else None
        voyages_month = len(df[df["date"].dt.month == this_month]) if "date" in df.columns else None
        total_tonnage = df["quantite_transporte"].sum() if "quantite_transporte" in df.columns else None
        avg_duration = df["duree_min"].mean() if "duree_min" in df.columns else None
        avg_distance = df["distance_km"].mean() if "distance_km" in df.columns else None
        total_distance = df["distance_km"].sum() if "distance_km" in df.columns else None

        st.markdown(f"""
        <div class='kpi-row'>
            <div class='kpi-tile'>
                <div class='label'>Total voyages (aujourd'hui)</div>
                <div class='value'>{voyages_today if voyages_today is not None else 'N/A'}</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Total voyages (ce mois)</div>
                <div class='value'>{voyages_month if voyages_month is not None else 'N/A'}</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Total tonnage transporté</div>
                <div class='value'>{round(total_tonnage, 1) if total_tonnage is not None else 'N/A'} t</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Durée moyenne par voyage</div>
                <div class='value'>{round(avg_duration, 1) if avg_duration is not None else 'N/A'} min</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Distance moyenne par voyage</div>
                <div class='value'>{round(avg_distance, 1) if avg_distance is not None else 'N/A'} km</div>
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
        # Data table
        st.markdown("<div class='section-title-bar'>📋 Données</div>", unsafe_allow_html=True)
        st.markdown("---")
        styled_df = df.style.set_table_styles(
            [
                {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
                {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
                {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
            ]
        ).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
        st.dataframe(styled_df, use_container_width=True)

        import streamlit.components.v1 as components
        def render_chart(fig, title, height=420):
            special_title2(title)
            html = f"<div class='chart-card'>{fig.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
            components.html(html, height=height, scrolling=True)

        
        # Top 5 conducteurs
        if "id_conducteur" in df.columns and "quantite_transporte" in df.columns:
            conducteur_rank = df.groupby("id_conducteur").agg(
                voyages=("id_voyage", "count"),
                tonnage=("quantite_transporte", "sum")
            ).sort_values(by=["voyages", "tonnage"], ascending=False).head(5).reset_index()
            special_title("Top 5 Conducteurs")
            styled_conducteur = conducteur_rank.style.set_table_styles(
                [
                    {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
                    {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
                    {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
                ]
            ).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
            st.dataframe(styled_conducteur, use_container_width=True)
        # Top 5 camions
        if "id_camion" in df.columns and "quantite_transporte" in df.columns:
            camion_rank = df.groupby("id_camion").agg(
                voyages=("id_voyage", "count"),
                tonnage=("quantite_transporte", "sum")
            ).sort_values(by=["voyages", "tonnage"], ascending=False).head(5).reset_index()
            special_title("Top 5 Camions")
            styled_camion = camion_rank.style.set_table_styles(
                [
                    {"selector": "thead th", "props": [("background-color", "#0F766E"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody td", "props": [("text-align", "center"), ("padding", "8px")]},
                    {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F9FAFB")]},
                    {"selector": "tbody tr:hover", "props": [("background-color", "#E6FFFA")]}
                ]
            ).set_properties(**{"border": "1px solid #E5E7EB", "font-family": "Poppins"})
            st.dataframe(styled_camion, use_container_width=True)

         # Ranking tables
        st.markdown("<div class='section-title-bar'>📈 Visualisation</div>", unsafe_allow_html=True)
        st.markdown("---")


        # Evolution des voyages par jour/semaine
        if "date" in df.columns:
            df["jour"] = df["date"].dt.date
            daily_counts = df.groupby("jour").size().reset_index(name="Voyages")
            fig_evol = px.line(daily_counts, x="jour", y="Voyages", title=None)
            fig_evol = plotly_style(fig_evol)
            render_chart(fig_evol, "Evolution des voyages par jour", height=420)
            df["semaine"] = df["date"].dt.isocalendar().week
            weekly_counts = df.groupby("semaine").size().reset_index(name="Voyages")
            fig_week = px.line(weekly_counts, x="semaine", y="Voyages", title=None)
            fig_week = plotly_style(fig_week)
            render_chart(fig_week, "Evolution des voyages par semaine", height=420)

        # Répartition des voyages par camion
        if "id_camion" in df.columns:
            truck_counts = df["id_camion"].value_counts().reset_index()
            truck_counts.columns = ["Camion", "Nombre de voyages"]
            fig_truck = px.bar(truck_counts, x="Camion", y="Nombre de voyages", title=None)
            fig_truck = plotly_style(fig_truck)
            render_chart(fig_truck, "Répartition des voyages par camion", height=420)

        # Répartition des voyages par conducteur
        if "id_conducteur" in df.columns:
            driver_counts = df["id_conducteur"].value_counts().reset_index()
            driver_counts.columns = ["Conducteur", "Nombre de voyages"]
            fig_driver = px.bar(driver_counts, x="Conducteur", y="Nombre de voyages", title=None)
            fig_driver = plotly_style(fig_driver)
            render_chart(fig_driver, "Répartition des voyages par conducteur", height=420)

        # Histogramme des tonnages par voyage
        if "quantite_transporte" in df.columns:
            fig_tonnage = px.histogram(df, x="quantite_transporte", nbins=20, title=None)
            fig_tonnage = plotly_style(fig_tonnage)
            render_chart(fig_tonnage, "Histogramme des tonnages par voyage", height=420)

       
        # Export Section
        st.markdown("<div class='section-title-bar'>💾 Export des Données</div>", unsafe_allow_html=True)
        st.markdown("---")
        col_export1, col_export2 = st.columns([1, 3])
        with col_export1:
            # Create filename with date info if available
            if start_date and end_date:
                filename = f'voyages_{selected_trip.replace(" ", "_")}_{start_date}_{end_date}.csv'
            else:
                filename = f'voyages_{selected_trip.replace(" ", "_")}_all_data.csv'
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
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=filename,
                mime='text/csv',
                help="Télécharger les données filtrées au format CSV"
            )
        with col_export2:
            if start_date and end_date:
                st.info(f"📊 **Résumé**: {total_voyages} voyages analysés avec {round(total_distance, 1) if total_distance else 0} km parcourus du {start_date} au {end_date}")
            else:
                st.info(f"📊 **Résumé**: {total_voyages} voyages analysés avec {round(total_distance, 1) if total_distance else 0} km parcourus")

    else:
        st.warning("⚠️ Aucune donnée disponible pour les critères sélectionnés.")
        st.info("💡 Essayez de modifier les filtres pour voir plus de données.")

if __name__ == "__main__":
    main()
