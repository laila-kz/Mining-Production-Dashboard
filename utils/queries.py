"""
SQL Query & Business Analytics Module for Mining Production Dashboard
Provides parameterized, cached queries leveraging SQL joins, aggregations, and business metrics.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from database import query_df, DB_NAME


@st.cache_data(ttl=600)
def get_global_kpis() -> Dict[str, Any]:
    """Calculates top-level summary KPIs directly using SQL aggregations."""
    query = """
    SELECT
        COUNT(v.id_voyage) AS total_voyages,
        COALESCE(SUM(v.quantite_transporte), 0) AS total_tonnage,
        COALESCE(AVG(v.distance_km), 0) AS avg_distance,
        COUNT(DISTINCT v.id_conducteur) AS active_conducteurs,
        COUNT(DISTINCT v.id_camion) AS active_camions,
        (SELECT COALESCE(SUM(duree_minutes), 0) / 60.0 FROM arret) AS total_arret_hours,
        (SELECT COALESCE(AVG(taux_phosphate), 0) FROM qualite) AS avg_phosphate,
        (SELECT COALESCE(AVG(humidite), 0) FROM qualite) AS avg_humidite
    FROM voyage v;
    """
    df = query_df(query)
    if df.empty:
        return {
            "total_voyages": 0, "total_tonnage": 0.0, "avg_distance": 0.0,
            "active_conducteurs": 0, "active_camions": 0, "total_arret_hours": 0.0,
            "avg_phosphate": 0.0, "avg_humidite": 0.0
        }
    return df.iloc[0].to_dict()


@st.cache_data(ttl=600)
def get_daily_production_trend() -> pd.DataFrame:
    """Returns daily tonnage and trip volume for production trends."""
    query = """
    SELECT
        date,
        COUNT(id_voyage) AS nb_voyages,
        SUM(quantite_transporte) AS total_tonnage,
        ROUND(AVG(distance_km), 2) AS avg_distance
    FROM voyage
    GROUP BY date
    ORDER BY date ASC;
    """
    return query_df(query)


@st.cache_data(ttl=600)
def get_filter_options() -> Dict[str, List[Any]]:
    """Fetches unique values for sidebar dropdown filters."""
    camions = query_df("SELECT id_camion, matricule || ' (' || modele || ')' AS label FROM camion ORDER BY id_camion")
    conducteurs = query_df("SELECT id_conducteur, nom || ' ' || prenom AS nom_complet FROM conducteur ORDER BY nom")
    sites = query_df("SELECT id_site, nom FROM site ORDER BY nom")
    categories = query_df("SELECT DISTINCT categorie FROM qualite WHERE categorie IS NOT NULL ORDER BY categorie")
    types_arret = query_df("SELECT DISTINCT type FROM arret WHERE type IS NOT NULL ORDER BY type")
    
    date_range = query_df("SELECT MIN(date) AS min_date, MAX(date) AS max_date FROM voyage")
    min_date = date_range["min_date"].iloc[0] if not date_range.empty else "2025-01-01"
    max_date = date_range["max_date"].iloc[0] if not date_range.empty else "2025-12-31"

    return {
        "camions": camions.to_dict(orient="records"),
        "conducteurs": conducteurs.to_dict(orient="records"),
        "sites": sites.to_dict(orient="records"),
        "categories": categories["categorie"].tolist(),
        "types_arret": types_arret["type"].tolist(),
        "min_date": min_date,
        "max_date": max_date
    }


@st.cache_data(ttl=600)
def get_voyages_detailed(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    id_camion: Optional[int] = None,
    id_conducteur: Optional[str] = None,
    id_site: Optional[str] = None
) -> pd.DataFrame:
    """Fetches fully joined voyages with truck, driver, site, and quality details."""
    query = """
    SELECT
        v.id_voyage,
        v.date,
        v.heure_depart,
        v.heure_arrive,
        v.distance_km,
        v.quantite_transporte,
        v.id_camion,
        c.matricule AS camion_matricule,
        c.modele AS camion_modele,
        c.capacite AS camion_capacite,
        v.id_conducteur,
        d.nom || ' ' || d.prenom AS conducteur_nom,
        d.CIN AS conducteur_cin,
        v.id_site,
        s.nom AS site_nom,
        s.localisation AS site_localisation,
        v.id_qualite,
        q.categorie AS qualite_categorie,
        q.nom_de_produit,
        q.taux_phosphate,
        q.humidite,
        q.granulometrie
    FROM voyage v
    LEFT JOIN camion c ON v.id_camion = c.id_camion
    LEFT JOIN conducteur d ON v.id_conducteur = d.id_conducteur
    LEFT JOIN site s ON v.id_site = s.id_site
    LEFT JOIN qualite q ON v.id_qualite = q.id_qualite
    WHERE (:start_date IS NULL OR v.date >= :start_date)
      AND (:end_date IS NULL OR v.date <= :end_date)
      AND (:id_camion IS NULL OR v.id_camion = :id_camion)
      AND (:id_conducteur IS NULL OR v.id_conducteur = :id_conducteur)
      AND (:id_site IS NULL OR v.id_site = :id_site)
    ORDER BY v.date DESC, v.heure_depart DESC;
    """
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "id_camion": id_camion,
        "id_conducteur": id_conducteur,
        "id_site": id_site
    }
    df = query_df(query, params=params)
    
    if not df.empty:
        # Calculate trip duration and hourly productivity
        try:
            t_dep = pd.to_datetime(df["heure_depart"], format="%H:%M:%S", errors="coerce")
            t_arr = pd.to_datetime(df["heure_arrive"], format="%H:%M:%S", errors="coerce")
            duration_hrs = (t_arr - t_dep).dt.total_seconds() / 3600.0
            # Handle overnight trips if any
            duration_hrs = duration_hrs.apply(lambda x: x + 24.0 if x is not None and x < 0 else x)
            df["duree_heures"] = duration_hrs.round(2)
            df["tonnes_par_heure"] = (df["quantite_transporte"] / df["duree_heures"].replace(0, pd.NA)).round(2)
        except Exception:
            df["duree_heures"] = 0.0
            df["tonnes_par_heure"] = 0.0

        # Capacity utilization %
        df["taux_remplissage"] = ((df["quantite_transporte"] / df["camion_capacite"]) * 100).round(1)

    return df


@st.cache_data(ttl=600)
def get_qualite_dataset(
    categorie: Optional[str] = None,
    min_phosphate: Optional[float] = None,
    max_phosphate: Optional[float] = None
) -> pd.DataFrame:
    """Fetches quality lab records with optional geochemical thresholds."""
    query = """
    SELECT
        id_qualite,
        categorie,
        nom_de_produit,
        granulometrie,
        taux_phosphate,
        humidite
    FROM qualite
    WHERE (:categorie IS NULL OR categorie = :categorie)
      AND (:min_phosphate IS NULL OR taux_phosphate >= :min_phosphate)
      AND (:max_phosphate IS NULL OR taux_phosphate <= :max_phosphate)
    ORDER BY taux_phosphate DESC;
    """
    return query_df(query, params={
        "categorie": categorie,
        "min_phosphate": min_phosphate,
        "max_phosphate": max_phosphate
    })


@st.cache_data(ttl=600)
def get_camion_performance_stats() -> pd.DataFrame:
    """Calculates fleet performance, tonnage hauled, utilization, and downtime."""
    query = """
    SELECT
        c.id_camion,
        c.matricule,
        c.modele,
        c.capacite,
        COUNT(v.id_voyage) AS total_voyages,
        COALESCE(SUM(v.quantite_transporte), 0) AS total_tonnes,
        COALESCE(AVG(v.distance_km), 0) AS distance_moyenne,
        COALESCE(AVG((v.quantite_transporte / c.capacite) * 100), 0) AS taux_utilisation_moyen,
        COALESCE(a.total_arret_min, 0) AS arret_total_minutes,
        COALESCE(a.nb_arrets, 0) AS nb_arrets
    FROM camion c
    LEFT JOIN voyage v ON c.id_camion = v.id_camion
    LEFT JOIN (
        SELECT id_camion, SUM(duree_minutes) AS total_arret_min, COUNT(id_arret) AS nb_arrets
        FROM arret
        GROUP BY id_camion
    ) a ON c.id_camion = a.id_camion
    GROUP BY c.id_camion
    ORDER BY total_tonnes DESC;
    """
    return query_df(query)


@st.cache_data(ttl=600)
def get_conducteur_performance_stats() -> pd.DataFrame:
    """Calculates driver performance, productivity, and safety records."""
    query = """
    SELECT
        d.id_conducteur,
        d.nom,
        d.prenom,
        d.nom || ' ' || d.prenom AS nom_complet,
        d.CIN,
        COUNT(v.id_voyage) AS total_voyages,
        COALESCE(SUM(v.quantite_transporte), 0) AS total_tonnes,
        COALESCE(AVG(v.distance_km), 0) AS distance_moyenne,
        COALESCE(a.nb_arrets, 0) AS nb_arrets,
        COALESCE(a.total_arret_min, 0) AS total_arret_min
    FROM conducteur d
    LEFT JOIN voyage v ON d.id_conducteur = v.id_conducteur
    LEFT JOIN (
        SELECT id_conducteur, COUNT(id_arret) AS nb_arrets, SUM(duree_minutes) AS total_arret_min
        FROM arret
        GROUP BY id_conducteur
    ) a ON d.id_conducteur = a.id_conducteur
    GROUP BY d.id_conducteur
    ORDER BY total_tonnes DESC;
    """
    return query_df(query)


@st.cache_data(ttl=600)
def get_arrets_detailed(
    type_arret: Optional[str] = None,
    id_camion: Optional[int] = None
) -> pd.DataFrame:
    """Fetches truck stoppage incidents with duration analysis and failure causes."""
    query = """
    SELECT
        a.id_arret,
        a.date_heure,
        DATE(a.date_heure) AS date,
        a.duree,
        a.duree_minutes,
        ROUND(a.duree_minutes / 60.0, 2) AS duree_heures,
        a.type,
        a.raison,
        a.id_camion,
        c.matricule AS camion_matricule,
        c.modele AS camion_modele,
        a.id_conducteur,
        d.nom || ' ' || d.prenom AS conducteur_nom
    FROM arret a
    LEFT JOIN camion c ON a.id_camion = c.id_camion
    LEFT JOIN conducteur d ON a.id_conducteur = d.id_conducteur
    WHERE (:type_arret IS NULL OR a.type = :type_arret)
      AND (:id_camion IS NULL OR a.id_camion = :id_camion)
    ORDER BY a.date_heure DESC;
    """
    return query_df(query, params={"type_arret": type_arret, "id_camion": id_camion})
