"""
Unit Tests for Database Queries & Analytics Calculations
"""

import pytest
import os
from database import fetch_data, query_df
from utils.queries import (
    get_global_kpis,
    get_voyages_detailed,
    get_camion_performance_stats,
    get_conducteur_performance_stats,
    get_arrets_detailed,
    get_qualite_dataset
)


def test_database_table_whitelist():
    """Verifies that fetch_data rejects unwhitelisted table queries."""
    with pytest.raises(ValueError):
        fetch_data("malicious_table_drop_all")


def test_global_kpis_calculation():
    """Verifies that top-level KPIs are properly aggregated."""
    kpis = get_global_kpis()
    assert kpis["total_voyages"] > 0
    assert kpis["total_tonnage"] > 0
    assert kpis["avg_distance"] > 0
    assert kpis["avg_phosphate"] > 0


def test_voyages_enrichment():
    """Verifies that voyages query properly computes durations and capacity fills."""
    df = get_voyages_detailed()
    assert not df.empty
    assert "duree_heures" in df.columns
    assert "tonnes_par_heure" in df.columns
    assert "taux_remplissage" in df.columns
    assert "conducteur_nom" in df.columns
    assert "camion_matricule" in df.columns


def test_fleet_performance_aggregation():
    """Verifies fleet statistics computation."""
    camions = get_camion_performance_stats()
    assert not camions.empty
    assert "total_tonnes" in camions.columns
    assert "taux_utilisation_moyen" in camions.columns
    assert "arret_total_minutes" in camions.columns


def test_quality_dataset_filtering():
    """Verifies phosphate threshold filtering in quality dataset."""
    df_all = get_qualite_dataset()
    df_filtered = get_qualite_dataset(min_phosphate=65.0)
    assert len(df_filtered) <= len(df_all)
    if not df_filtered.empty:
        assert (df_filtered["taux_phosphate"] >= 65.0).all()
