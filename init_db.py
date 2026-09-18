"""
Database Schema Initialization for Mining Production Dashboard
Defines SQLite tables, constraints, foreign keys, and indexes.
"""

import sqlite3
import os

DB_NAME = os.getenv("MINING_DB_PATH", "mining_db.sqlite")


def create_schema(db_path: str = DB_NAME, drop_existing: bool = True):
    """Initializes the database schema with relational integrity and indexes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    if drop_existing:
        # Drop child tables first, then parent tables
        cursor.execute("DROP TABLE IF EXISTS arret;")
        cursor.execute("DROP TABLE IF EXISTS voyage;")
        cursor.execute("DROP TABLE IF EXISTS qualite;")
        cursor.execute("DROP TABLE IF EXISTS conducteur;")
        cursor.execute("DROP TABLE IF EXISTS camion;")
        cursor.execute("DROP TABLE IF EXISTS site;")

    # Table: site
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site (
        id_site TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        localisation TEXT
    );
    """)

    # Table: camion
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS camion (
        id_camion INTEGER PRIMARY KEY,
        matricule TEXT NOT NULL,
        capacite REAL NOT NULL,
        modele TEXT NOT NULL
    );
    """)

    # Table: conducteur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conducteur (
        id_conducteur TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        CIN TEXT NOT NULL
    );
    """)

    # Table: qualite
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qualite (
        id_qualite TEXT PRIMARY KEY,
        categorie TEXT,
        nom_de_produit TEXT,
        granulometrie REAL,
        taux_phosphate REAL,
        humidite REAL
    );
    """)

    # Table: voyage
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voyage (
        id_voyage TEXT PRIMARY KEY,
        date TEXT NOT NULL,
        heure_depart TEXT,
        heure_arrive TEXT,
        distance_km REAL,
        quantite_transporte REAL DEFAULT 0,
        id_conducteur TEXT,
        id_camion INTEGER,
        id_site TEXT,
        id_qualite TEXT,
        FOREIGN KEY (id_conducteur) REFERENCES conducteur(id_conducteur) ON DELETE SET NULL,
        FOREIGN KEY (id_camion) REFERENCES camion(id_camion) ON DELETE SET NULL,
        FOREIGN KEY (id_site) REFERENCES site(id_site) ON DELETE SET NULL,
        FOREIGN KEY (id_qualite) REFERENCES qualite(id_qualite) ON DELETE SET NULL
    );
    """)

    # Table: arret
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS arret (
        id_arret TEXT PRIMARY KEY,
        date_heure TEXT NOT NULL,
        duree TEXT,
        duree_minutes REAL DEFAULT 0,
        type TEXT,
        raison TEXT,
        id_camion INTEGER,
        id_conducteur TEXT,
        FOREIGN KEY (id_camion) REFERENCES camion(id_camion) ON DELETE SET NULL,
        FOREIGN KEY (id_conducteur) REFERENCES conducteur(id_conducteur) ON DELETE SET NULL
    );
    """)

    # Performance Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_voyage_date ON voyage(date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_voyage_camion ON voyage(id_camion);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_voyage_conducteur ON voyage(id_conducteur);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_voyage_site ON voyage(id_site);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_voyage_qualite ON voyage(id_qualite);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_arret_camion ON arret(id_camion);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_arret_conducteur ON arret(id_conducteur);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_arret_date ON arret(date_heure);")

    conn.commit()
    conn.close()
    print(f"[OK] Schema and indexes successfully initialized in '{db_path}'.")


if __name__ == "__main__":
    create_schema()
