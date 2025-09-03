import sqlite3

# Connect to SQLite DB file
conn = sqlite3.connect("mining_db.sqlite")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# --- Create tables ---

cursor.execute("""
CREATE TABLE IF NOT EXISTS conducteur (
    id_conducteur CHAR(50) PRIMARY KEY,
    nom TEXT,
    prenom TEXT,
    CIN CHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS camion (
    id_camion INTEGER PRIMARY KEY,
    matricule TEXT,
    capacite REAL,
    modele TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS site (
    id_site CHAR(50) PRIMARY KEY,
    nom TEXT,
    localisation TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS qualite (
    id_qualite CHAR(50) PRIMARY KEY,
    taux_phosphate REAL,
    humidite REAL,
    granulometrie REAL,
    taux_silice REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS voyage (
    id_voyage CHAR(50) PRIMARY KEY,
    date TEXT,
    heure_depart TEXT,
    heure_arrive TEXT,
    distance REAL,
    id_conducteur CHAR(50),
    id_camion INTEGER,
    id_site CHAR(50),
    id_qualite CHAR(50),
    FOREIGN KEY(id_conducteur) REFERENCES conducteur(id_conducteur),
    FOREIGN KEY(id_camion) REFERENCES camion(id_camion),
    FOREIGN KEY(id_site) REFERENCES site(id_site),
    FOREIGN KEY(id_qualite) REFERENCES qualite(id_qualite)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS arret (
    id_arret CHAR(50) PRIMARY KEY,
    date_heure TEXT,
    duree INTEGER,
    type_arret TEXT,
    raison TEXT,
    id_camion INTEGER,
    id_conducteur CHAR(50),
    FOREIGN KEY(id_camion) REFERENCES camion(id_camion),
    FOREIGN KEY(id_conducteur) REFERENCES conducteur(id_conducteur)
)
""")

conn.commit()
conn.close()
print("Database and tables created successfully.")
