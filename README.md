# Système de Gestion de la Production Minière (Phosboucraa) — Dashboard & Reporting

Module de visualisation et de reporting développé avec **Streamlit** pour analyser la production minière à partir d’une base **SQLite**.

> **Aperçu** : Vue globale sur les voyages, contrôle qualité, performance des conducteurs/camions et monitoring des arrêts.

---

## Fonctionnalités

- **Tableau de bord global** (accueil) avec KPIs et activité récente
- **TDB Voyages** : filtres par voyage, camion, conducteur, statut et plage de distance
- **TDB Qualité** : filtres par contrôle, plage de taux de phosphate et humidité
- **TDB Performance Camions** : performance par camion + analyse des arrêts (disponibilité)
- **TDB Performance Conducteurs** : performance par conducteur
- **TDB Arrêts Camions** : suivi des arrêts avec statistiques et visualisations (causes, type, tendances)
- **Export CSV** des données filtrées (selon le tableau de bord)

---

## Structure du projet

```text
production_miniere_dashboard-main/
├─ Accueil.py
├─ database.py
├─ init_db.py
├─ import_csv.py
├─ mining_db.sqlite
├─ assets/
│  └─ phosboucraa_logo.jpg
├─ data/
│  ├─ voyage.csv
│  ├─ qualite.csv
│  ├─ arret.csv
│  ├─ conducteur.csv
│  ├─ camion.csv
│  └─ site.csv
└─ pages/
   ├─ Tableau_de_Bord_Voyages.py
   ├─ Tableau_de_Bord_Qualité.py
   ├─ Tableau_de_Bord_Camions.py
   ├─ Tableau_de_Bord_Conducteurs.py
   └─ Tableau_de_Bord_Arrêts_Camions.py
```

---

## Pré-requis

- Python 3.9+ (recommandé)
- Un environnement virtuel (optionnel mais recommandé)
- Dépendances principales :
  - `streamlit`
  - `pandas`
  - `plotly`

---

## Installation

1) (Optionnel) Créez un environnement virtuel :

```bash
python -m venv .venv
.
# Sur Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

2) Installez les dépendances :

```bash
pip install streamlit pandas plotly
```

---

## Initialisation de la base de données

### 1) Création des tables

Le script **`init_db.py`** crée les tables SQLite avec contraintes (foreign keys activées).

```bash
python init_db.py
```

### 2) Import des CSV vers SQLite

Le script **`import_csv.py`** parcourt le dossier `data/` et charge les fichiers CSV dans SQLite (nom du fichier = nom de la table).

```bash
python import_csv.py
```

> Le fichier de base est **`mining_db.sqlite`**.

---

## Lancer l’application Streamlit

Selon la configuration souhaitée, vous pouvez démarrer en indiquant la page d’accueil.

```bash
streamlit run Accueil.py
```

Ensuite :
- Utilisez la **barre latérale** ou les **boutons de navigation** pour accéder aux différents tableaux de bord.

---

## Données attendues (schéma logique)

Tables présentes dans SQLite :

- `conducteur` : `id_conducteur`, `nom`, `prenom`, `CIN`
- `camion` : `id_camion`, `matricule`, `capacite`, `modele`
- `site` : `id_site`, `nom`, `localisation`
- `qualite` : `id_qualite`, `taux_phosphate`, `humidite`, `granulometrie`, `taux_silice`
- `voyage` : `id_voyage`, `date`, `heure_depart`, `heure_arrive`, `distance`, `id_conducteur`, `id_camion`, `id_site`, `id_qualite`
- `arret` : `id_arret`, `date_heure`, `duree`, `type_arret`, `raison`, `id_camion`, `id_conducteur`

---

## Visualisations & KPIs (principes)

Les dashboards combinent :
- **KPIs** calculés directement depuis la base (comptages, sommes, moyennes)
- **Graphiques Plotly** (histogrammes, barres, scatter, camemberts, séries temporelles)
- **Filtres** côté interface (Streamlit)
- **Exports CSV** des datasets filtrés

---

## Notes d’utilisation

- Les pages utilisent des styles HTML/CSS embarqués pour une UI homogène.
- Les graphiques interactifs Plotly permettent : zoom, survol, exploration.
- Les exports respectent les filtres appliqués dans chaque tableau de bord (quand disponibles).

---


