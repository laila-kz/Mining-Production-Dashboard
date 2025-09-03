import streamlit as st
import plotly.express as px
from database import fetch_data
import pandas as pd

def main():
    # Inject custom KPI styles and apply them to all page section titles
    st.markdown(
        """
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
    <div style='font-size:2.5rem; font-weight:700;'>TDB des Qualités</div>
    <div style='font-size:1.2rem; margin-top:0.2rem; background: rgba(20,184,166,0.10); color:#115E59; padding:0.2rem 0.5rem; border-radius:5px;'>Module Reporting & Dashboard</div>
    <div style='margin-top:0.4rem; font-size:0.85rem; opacity:0.85;'>Date et heure : {datetime.now().strftime('%A %d %B %Y, %H:%M')}</div>
</div>
""", unsafe_allow_html=True)
    # Page configuration
    st.set_page_config(page_title="Qualité Dashboard",page_icon="🟢" ,layout="wide")

    st.markdown("""
    <link href=\"https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Roboto&display=swap\" rel=\"stylesheet\">
    <style>
    body, .stApp {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        font-family: 'Roboto', sans-serif !important;
    }
    h1, h2, h3, .stSubheader, .section-title-bar {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #0F766E !important;
    }
    .stMarkdown, .stText, .stDataFrame, .stTable {
        font-family: 'Roboto', sans-serif !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        color: #1F2937 !important;
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
    </style>
    """, unsafe_allow_html=True)

   

    # Fetch data
    df = fetch_data("qualite")

    # Sidebar for filters
    with st.sidebar:
        st.markdown("### 🔍 Filtres")
        st.markdown("---")
        
        # Filter by quality ID
        quality_ids = df["id_qualite"].unique() if "id_qualite" in df.columns else []
        selected_quality = st.selectbox(
            "**Contrôle qualité**",
            options=["Tous les contrôles"] + list(quality_ids),
            help="Sélectionnez un contrôle spécifique ou tous les contrôles"
        )
        
        # Filter by phosphate rate range
        if "taux_phosphate" in df.columns:
            st.markdown("**Taux de phosphate (%)**")
            min_phosphate = float(df["taux_phosphate"].min())
            max_phosphate = float(df["taux_phosphate"].max())
            phosphate_range = st.slider(
                "Plage de taux de phosphate",
                min_value=min_phosphate,
                max_value=max_phosphate,
                value=(min_phosphate, max_phosphate),
                help="Sélectionnez une plage de taux de phosphate"
            )
        
        # Filter by humidity range
        if "humidite" in df.columns:
            st.markdown("**Humidité (%)**")
            min_humidity = float(df["humidite"].min())
            max_humidity = float(df["humidite"].max())
            humidity_range = st.slider(
                "Plage d'humidité",
                min_value=min_humidity,
                max_value=max_humidity,
                value=(min_humidity, max_humidity),
                help="Sélectionnez une plage d'humidité"
            )

    # Apply filters
    if selected_quality != "Tous les contrôles":
        df = df[df["id_qualite"] == selected_quality]
    if "taux_phosphate" in df.columns:
        df = df[(df["taux_phosphate"] >= phosphate_range[0]) & (df["taux_phosphate"] <= phosphate_range[1])]
    if "humidite" in df.columns:
        df = df[(df["humidite"] >= humidity_range[0]) & (df["humidite"] <= humidity_range[1])]
    # Example explicit KPI section title (keeps backward compatibility)
    st.markdown("<div class='kpi-section-title'>🧾Indicateurs clés</div>", unsafe_allow_html=True)
    # Main content area
    if not df.empty:
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
        total_controles = len(df)
        avg_phosphate = df["taux_phosphate"].mean() if "taux_phosphate" in df.columns else None
        avg_humidity = df["humidite"].mean() if "humidite" in df.columns else None
        conformes = len(df[df["taux_phosphate"] >= 30]) if "taux_phosphate" in df.columns else None
        st.markdown(f"""
        <div class='kpi-row'>
            <div class='kpi-tile'>
                <div class='label'>Nombre total de contrôles</div>
                <div class='value'>{total_controles:,}</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Taux phosphate moyen</div>
                <div class='value'>{round(avg_phosphate, 1) if avg_phosphate is not None else 'N/A'}%</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Humidité moyenne</div>
                <div class='value'>{round(avg_humidity, 1) if avg_humidity is not None else 'N/A'}%</div>
            </div>
            <div class='kpi-tile'>
                <div class='label'>Contrôles conformes (≥30% phosphate)</div>
                <div class='value'>{conformes if conformes is not None else 'N/A'}</div>
            </div>
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

        # Visualizations
        st.markdown("<div class='section-title-bar'>📈 Visualisations</div>", unsafe_allow_html=True)
        st.markdown("---")
        def special_title(text, icon="📌"):
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
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        import streamlit.components.v1 as components
        def render_chart(fig, title, height=420):
            special_title(title)
            html = f"<div class='chart-card'>{fig.to_html(include_plotlyjs='cdn', full_html=False)}</div>"
            components.html(html, height=height, scrolling=True)

        with col1:
            # Graph: phosphate rate distribution
            if "taux_phosphate" in df.columns:
                fig = px.histogram(
                    df, 
                    x="taux_phosphate", 
                    nbins=20, 
                    title=None,
                    color_discrete_sequence=["#315D44"]
                )
                fig.update_layout(xaxis_title="Taux de phosphate (%)", yaxis_title="Nombre de contrôles")
                render_chart(fig, "Distribution du taux de phosphate", height=420)

        with col2:
            # Graph: humidity distribution
            if "humidite" in df.columns:
                fig2 = px.histogram(
                    df, 
                    x="humidite", 
                    nbins=20, 
                    title=None,
                    color_discrete_sequence=["#315D44"]
                )
                fig2.update_layout(xaxis_title="Humidité (%)", yaxis_title="Nombre de contrôles")
                render_chart(fig2, "Distribution de l'humidité", height=420)

        # Correlation analysis
        if "taux_phosphate" in df.columns and "humidite" in df.columns:
            fig_scatter = px.scatter(
                df, 
                x="taux_phosphate", 
                y="humidite", 
                title=None,
                color="id_qualite" if "id_qualite" in df.columns else None
            )
            fig_scatter.update_layout(xaxis_title="Taux de phosphate (%)", yaxis_title="Humidité (%)")
            render_chart(fig_scatter, "Relation Phosphate vs Humidité", height=420)

        # Export Section
        st.markdown("<div class='section-title-bar'>💾 Export des Données</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        col_export1, col_export2 = st.columns([1, 3])
        with col_export1:
            filename = f'qualite_{selected_quality.replace(" ", "_")}_data.csv'
            
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
            st.info(f"📊 **Résumé**: {total_controles} contrôles analysés avec un taux moyen de phosphate de {round(avg_phosphate, 1) if avg_phosphate else 0}%")

    else:
        st.warning("⚠️ Aucune donnée disponible pour les critères sélectionnés.")
        st.info("💡 Essayez de modifier les filtres pour voir plus de données.")

if __name__ == "__main__":
    main()
