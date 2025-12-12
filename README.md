# API Gestion des Compétences - IT Room

Application Flask pour gérer les compétences techniques des développeurs et faciliter l'allocation des ressources sur les projets.

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

Ou manuellement :
```bash
pip install flask flask-cors pdfplumber python-docx python-dateutil
```

2. Lancer l'application :
```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## Quick Start avec données de démo

Pour tester rapidement l'application avec des données exemples :

```bash
# 1. Lancer l'application
python app.py

# 2. Dans un autre terminal, importer les compétences
curl -X POST http://localhost:5000/import/competences/csv \
  -F "file=@examples/competences.csv"

# 3. Importer les projets
curl -X POST http://localhost:5000/import/projects/json \
  -F "file=@examples/projets.json"

# 4. Vérifier les données
curl http://localhost:5000/collaborators
curl http://localhost:5000/competences
```

Voir le dossier `examples/` pour plus de détails et des exemples d'intégration React.

## Structure de la base de données

### Tables principales
- `collaborator` - Collaborateurs
- `type` - Types de technologies
- `project` - Projets (avec date_fin et duree_mois)
- `techno` - Technologies
- `competence` - Compétences des collaborateurs (niveau déclaré et calculé)
- `project_techno_history` - Historique des technologies utilisées par projet

### Tables de liaison
- `techno_type` - Relation entre technos et types
- `techno_project` - Relation entre technos et projets
- `collaborator_project` - Relation entre collaborateurs et projets

---

## Documentation des Routes API

### 1. Collaborators (Collaborateurs)

#### GET `/collaborators`
Récupère tous les collaborateurs.

**Réponse :**
```json
[
  {
    "id": 1,
    "firstname": "Jean",
    "lastname": "Dupont",
    "date_add": "2024-12-12 10:00:00",
    "date_upd": "2024-12-12 10:00:00"
  }
]
```

#### GET `/collaborators/<id>`
Récupère un collaborateur par ID.

**Exemple :** `GET /collaborators/1`

#### POST `/collaborators`
Crée un nouveau collaborateur.

**Body :**
```json
{
  "firstname": "Sophie",
  "lastname": "Martin"
}
```

#### PATCH `/collaborators/<id>`
Met à jour un collaborateur.

**Body :**
```json
{
  "firstname": "Sophie",
  "lastname": "Durand"
}
```

#### DELETE `/collaborators/<id>`
Supprime un collaborateur.

**Exemple :** `DELETE /collaborators/1`

---

### 2. Types

#### GET `/types`
Récupère tous les types.

#### GET `/types/<id>`
Récupère un type par ID.

#### POST `/types`
Crée un nouveau type.

**Body :**
```json
{
  "name": "Frontend"
}
```

#### PATCH `/types/<id>`
Met à jour un type.

**Body :**
```json
{
  "name": "Backend"
}
```

#### DELETE `/types/<id>`
Supprime un type.

---

### 3. Projects (Projets)

#### GET `/projects`
Récupère tous les projets.

**Réponse :**
```json
[
  {
    "id": 1,
    "name": "Site E-commerce",
    "date_fin": "2024-08",
    "duree_mois": 6,
    "date_add": "2024-12-12 10:00:00",
    "date_upd": "2024-12-12 10:00:00"
  }
]
```

#### GET `/projects/<id>`
Récupère un projet par ID.

#### POST `/projects`
Crée un nouveau projet.

**Body :**
```json
{
  "name": "Site E-commerce",
  "date_fin": "2024-08",
  "duree_mois": 6
}
```

**Note :** `date_fin` et `duree_mois` sont optionnels.

#### PATCH `/projects/<id>`
Met à jour un projet.

**Body :**
```json
{
  "name": "Application Mobile",
  "date_fin": "2025-06",
  "duree_mois": 12
}
```

#### DELETE `/projects/<id>`
Supprime un projet.

---

### 4. Technos (Technologies)

#### GET `/technos`
Récupère toutes les technologies.

#### GET `/technos/<id>`
Récupère une technologie par ID.

#### POST `/technos`
Crée une nouvelle technologie.

**Body :**
```json
{
  "name": "React"
}
```

#### PATCH `/technos/<id>`
Met à jour une technologie.

**Body :**
```json
{
  "name": "React Native"
}
```

#### DELETE `/technos/<id>`
Supprime une technologie.

---

### 5. Competences (Compétences)

#### GET `/competences`
Récupère toutes les compétences.

**Réponse :**
```json
[
  {
    "id": 1,
    "id_collaborator": 1,
    "id_techno": 3,
    "niveau_declare": 4,
    "niveau_calcule": 4.2,
    "date_add": "2024-12-12 10:00:00",
    "date_upd": "2024-12-12 10:00:00"
  }
]
```

#### GET `/competences/<id>`
Récupère une compétence par ID.

#### GET `/competences/collaborator/<id_collaborator>`
Récupère toutes les compétences d'un collaborateur.

**Exemple :** `GET /competences/collaborator/1`

#### GET `/competences/techno/<id_techno>`
Récupère toutes les compétences pour une technologie.

**Exemple :** `GET /competences/techno/3`

#### GET `/competences/collaborator/<id_collaborator>/techno/<id_techno>`
Récupère la compétence d'un collaborateur pour une techno spécifique.

**Exemple :** `GET /competences/collaborator/1/techno/3`

#### POST `/competences`
Crée une nouvelle compétence.

**Body :**
```json
{
  "id_collaborator": 1,
  "id_techno": 3,
  "niveau_declare": 4,
  "niveau_calcule": 4.2
}
```

**Note :**
- `niveau_declare` est requis (1-5)
- `niveau_calcule` est optionnel (par défaut = niveau_declare)
- Les niveaux doivent être entre 1 et 5

#### PATCH `/competences/<id>`
Met à jour une compétence.

**Body :**
```json
{
  "niveau_declare": 5,
  "niveau_calcule": 4.8
}
```

#### DELETE `/competences/<id>`
Supprime une compétence.

---

### 6. Project History (Historique des projets)

#### GET `/project_history`
Récupère tout l'historique.

**Réponse :**
```json
[
  {
    "id": 1,
    "id_project": 1,
    "id_techno": 3,
    "id_collaborator": 1,
    "date_debut": "2024-01",
    "date_fin": "2024-08",
    "duree_mois": 6
  }
]
```

#### GET `/project_history/<id>`
Récupère un élément d'historique par ID.

#### GET `/project_history/project/<id_project>`
Récupère l'historique d'un projet.

**Exemple :** `GET /project_history/project/1`

#### GET `/project_history/collaborator/<id_collaborator>`
Récupère l'historique d'un collaborateur.

**Exemple :** `GET /project_history/collaborator/1`

#### GET `/project_history/techno/<id_techno>`
Récupère l'historique d'une technologie.

**Exemple :** `GET /project_history/techno/3`

#### POST `/project_history`
Crée un nouvel enregistrement d'historique.

**Body :**
```json
{
  "id_project": 1,
  "id_techno": 3,
  "id_collaborator": 1,
  "date_debut": "2024-01",
  "date_fin": "2024-08",
  "duree_mois": 6
}
```

**Note :** `date_debut`, `date_fin` et `duree_mois` sont optionnels.

#### PATCH `/project_history/<id>`
Met à jour un élément d'historique.

**Body :**
```json
{
  "date_fin": "2024-09",
  "duree_mois": 7
}
```

#### DELETE `/project_history/<id>`
Supprime un élément d'historique.

---

### 7. Relations

#### Techno ↔ Type

**GET** `/techno_type` - Liste toutes les relations
**POST** `/techno_type` - Crée une relation
**DELETE** `/techno_type/<id_techno>/<id_type>` - Supprime une relation

**Exemple POST :**
```json
{
  "id_techno": 1,
  "id_type": 2
}
```

#### Techno ↔ Project

**GET** `/techno_project` - Liste toutes les relations
**POST** `/techno_project` - Crée une relation
**DELETE** `/techno_project/<id_techno>/<id_project>` - Supprime une relation

**Exemple POST :**
```json
{
  "id_techno": 1,
  "id_project": 3
}
```

#### Collaborator ↔ Project

**GET** `/collaborator_project` - Liste toutes les relations
**POST** `/collaborator_project` - Crée une relation
**DELETE** `/collaborator_project/<id_collaborator>/<id_project>` - Supprime une relation

**Exemple POST :**
```json
{
  "id_collaborator": 1,
  "id_project": 3
}
```

---

### 8. Imports (CSV/JSON)

#### POST `/import/competences/csv`
Importe des compétences depuis un fichier CSV.

**Format CSV attendu :**
```csv
nom,prenom,technologie,niveau_declare
Dupont,Jean,PHP,4
Dupont,Jean,React,3
Martin,Sophie,Python,5
```

**Fonctionnement :**
- Crée automatiquement les collaborateurs et technologies s'ils n'existent pas
- Si la compétence existe déjà, elle est mise à jour
- Le niveau_calcule est initialisé au niveau_declare

**Exemple avec curl :**
```bash
curl -X POST http://localhost:5000/import/competences/csv \
  -F "file=@competences.csv"
```

**Réponse :**
```json
{
  "message": "Import terminé",
  "created": 15,
  "updated": 3,
  "errors": []
}
```

#### POST `/import/competences/json`
Importe des compétences depuis un fichier JSON.

**Format JSON attendu :**
```json
[
  {
    "nom": "Dupont",
    "prenom": "Jean",
    "technologie": "PHP",
    "niveau_declare": 4
  },
  {
    "nom": "Martin",
    "prenom": "Sophie",
    "technologie": "Python",
    "niveau_declare": 5
  }
]
```

**Exemple avec curl :**
```bash
curl -X POST http://localhost:5000/import/competences/json \
  -F "file=@competences.json"
```

#### POST `/import/projects/json`
Importe des projets avec leur équipe et technologies depuis un fichier JSON.

**Format JSON attendu :**
```json
{
  "projets": [
    {
      "nom": "Site E-commerce",
      "technologies": ["PHP", "Symfony", "MySQL", "React"],
      "equipe": ["Jean Dupont", "Sophie Martin"],
      "duree_mois": 6,
      "date_fin": "2024-08"
    },
    {
      "nom": "Application Mobile",
      "technologies": ["React Native", "Node.js"],
      "equipe": ["Jean Dupont"],
      "duree_mois": 12,
      "date_fin": "2025-06"
    }
  ]
}
```

**Fonctionnement :**
- Crée automatiquement les projets, collaborateurs et technologies s'ils n'existent pas
- Crée les relations techno-project et collaborator-project
- Crée un enregistrement dans l'historique pour chaque combinaison (projet, techno, collaborateur)

**Exemple avec curl :**
```bash
curl -X POST http://localhost:5000/import/projects/json \
  -F "file=@projets.json"
```

**Réponse :**
```json
{
  "message": "Import terminé",
  "created_projects": 2,
  "created_history": 12,
  "errors": []
}
```

**Notes importantes :**
- Taille maximale des fichiers : 16 MB
- Format nom d'équipe : "Prénom Nom" (séparés par un espace)
- Les erreurs ne bloquent pas l'import, elles sont listées dans la réponse
- Les doublons sont ignorés (relations déjà existantes)

---

## Exemples d'utilisation avec curl

### Créer un collaborateur
```bash
curl -X POST http://localhost:5000/collaborators \
  -H "Content-Type: application/json" \
  -d '{"firstname": "Jean", "lastname": "Dupont"}'
```

### Créer une technologie
```bash
curl -X POST http://localhost:5000/technos \
  -H "Content-Type: application/json" \
  -d '{"name": "React"}'
```

### Créer une compétence
```bash
curl -X POST http://localhost:5000/competences \
  -H "Content-Type: application/json" \
  -d '{"id_collaborator": 1, "id_techno": 1, "niveau_declare": 4}'
```

### Créer un projet
```bash
curl -X POST http://localhost:5000/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Site E-commerce", "date_fin": "2024-08", "duree_mois": 6}'
```

### Créer un historique
```bash
curl -X POST http://localhost:5000/project_history \
  -H "Content-Type: application/json" \
  -d '{"id_project": 1, "id_techno": 1, "id_collaborator": 1, "duree_mois": 6}'
```

### Récupérer les compétences d'un collaborateur
```bash
curl http://localhost:5000/competences/collaborator/1
```

### Mettre à jour une compétence
```bash
curl -X PATCH http://localhost:5000/competences/1 \
  -H "Content-Type: application/json" \
  -d '{"niveau_calcule": 4.5}'
```

---

## Format des réponses

### Succès
```json
{
  "message": "Operation successful",
  "id": 1
}
```

### Erreur
```json
{
  "error": "Description de l'erreur"
}
```

---

## Codes de statut HTTP

- `200 OK` - Succès (GET, PATCH, DELETE)
- `201 Created` - Ressource créée (POST)
- `400 Bad Request` - Données invalides
- `404 Not Found` - Ressource non trouvée

---

## Structure des fichiers

```
hackcathon/
├── app.py                      # Point d'entrée principal
├── requirements.txt            # Dépendances Python
├── data/
│   └── database.db            # Base de données SQLite
├── examples/                   # Fichiers exemples pour import
│   ├── competences.csv
│   ├── competences.json
│   ├── projets.json
│   └── README.md
├── uploads/                    # Fichiers uploadés (temporaire)
└── src/
    ├── config.py              # Configuration de la BD
    ├── models.py              # Modèles CRUD
    └── routes/
        ├── collaborators.py   # Routes collaborateurs
        ├── types.py           # Routes types
        ├── projects.py        # Routes projets
        ├── technos.py         # Routes technologies
        ├── competences.py     # Routes compétences
        ├── project_history.py # Routes historique
        ├── relations.py       # Routes tables de liaison
        ├── imports.py         # Routes import CSV/JSON
        ├── scoring.py         # Moteur de scoring automatique
        ├── matrix.py          # Matrice de compétences
        ├── allocation.py      # Module d'allocation projet
        ├── dashboard.py       # Dashboard et statistiques
        └── cv_parser.py       # Parsing de CV (PDF/TXT/DOCX)
```

---

## Notes importantes

1. La base de données est créée automatiquement au premier lancement
2. Les dates sont au format `YYYY-MM-DD` ou `YYYY-MM`
3. Les niveaux de compétences sont de 1 à 5
4. La contrainte `UNIQUE(id_collaborator, id_techno)` empêche les doublons dans la table competence
5. Les champs `date_add` et `date_upd` sont gérés automatiquement

---

## Routes MVP Avancées

### 9. Scoring Automatique

#### POST `/scoring/calculate`
Recalcule tous les scores automatiquement pour toutes les compétences.

**Algorithme :**
```
Score = (niveau_déclaré × 0.3) + (score_projets × 0.4) + (ancienneté_bonus × 0.3)
- score_projets : basé sur le nombre de projets (max 5)
- ancienneté_bonus : max(0, 5 - mois_depuis_dernière_utilisation/12)
- Borné entre 1 et 5
```

**Exemple :**
```bash
curl -X POST http://localhost:5000/scoring/calculate
```

**Réponse :**
```json
{
  "message": "Recalcul terminé",
  "updated": 45,
  "errors": []
}
```

#### POST `/scoring/calculate/collaborator/<id>`
Recalcule les scores pour un collaborateur spécifique.

#### POST `/scoring/calculate/competence/<id>`
Recalcule le score pour une compétence spécifique.

#### GET `/scoring/parameters`
Retourne les paramètres de l'algorithme de scoring.

---

### 10. Matrice de Compétences

#### GET `/matrix/competences`
Retourne la matrice de compétences (développeurs × technologies).

**Query params :**
- `techno` : filtrer par technologie
- `niveau_min` : filtrer par niveau minimum
- `collaborator` : filtrer par nom de collaborateur

**Exemple :**
```bash
curl "http://localhost:5000/matrix/competences?niveau_min=3"
```

**Réponse :**
```json
{
  "matrix": [
    {
      "collaborator_id": 1,
      "collaborator_name": "Jean Dupont",
      "competences": {
        "React": {
          "niveau": 4.2,
          "color": "vert"
        },
        "PHP": {
          "niveau": 3.5,
          "color": "orange"
        }
      }
    }
  ],
  "technologies": ["React", "PHP", "Python"],
  "total_collaborators": 6,
  "total_technologies": 15
}
```

**Codes couleur :**
- `vert` : Expert (4-5)
- `orange` : Intermédiaire (2-3)
- `rouge` : Débutant (0-1)
- `gris` : Jamais utilisé

#### GET `/matrix/competences/simple`
Retourne une matrice simplifiée (format tableau).

**Réponse :**
```json
{
  "headers": ["Collaborateur", "React", "PHP", "Python"],
  "rows": [
    ["Jean Dupont", 4.2, 3.5, 0],
    ["Sophie Martin", 3.1, 0, 5.0]
  ]
}
```

#### GET `/matrix/competences/heatmap`
Retourne les données formatées pour une heatmap.

---

### 11. Allocation de Projet

#### POST `/allocation/suggest`
Suggère les meilleurs développeurs pour un nouveau projet.

**Body :**
```json
{
  "technologies": ["React", "Node.js", "MongoDB"],
  "team_size": 3
}
```

**Réponse :**
```json
{
  "suggestions_by_techno": {
    "React": [
      {
        "collaborator_id": 1,
        "name": "Jean Dupont",
        "niveau_calcule": 4.2,
        "is_expert": true
      }
    ]
  },
  "best_overall_fits": [
    {
      "collaborator_id": 1,
      "name": "Jean Dupont",
      "nb_technos_matched": 3,
      "avg_score": 4.5,
      "match_percentage": 100
    }
  ],
  "gaps": [
    {
      "techno": "MongoDB",
      "reason": "Aucun expert disponible (niveau < 4)",
      "best_niveau": 3.2
    }
  ]
}
```

#### GET `/allocation/capacity`
Vue agrégée de la capacité globale de l'équipe par technologie.

**Query params :**
- `niveau_min` : niveau minimum à considérer (défaut: 3)

**Exemple :**
```bash
curl "http://localhost:5000/allocation/capacity?niveau_min=3"
```

**Réponse :**
```json
{
  "capacity": [
    {
      "techno": "React",
      "total_collaborators": 5,
      "avg_niveau": 3.8,
      "nb_experts": 3,
      "nb_intermediaires": 2,
      "capacity_level": "high"
    }
  ]
}
```

#### GET `/allocation/gaps`
Identifie les gaps critiques (technologies avec < 2 experts).

**Réponse :**
```json
{
  "gaps": [
    {
      "techno": "Rust",
      "nb_experts": 0,
      "risk_level": "critical",
      "recommendation": "Recruter un expert ou former l'équipe"
    }
  ],
  "total_gaps": 5,
  "critical_gaps": 2
}
```

---

### 12. Dashboard

#### GET `/dashboard/overview`
Vue globale avec toutes les métriques principales.

**Réponse :**
```json
{
  "stats": {
    "total_collaborators": 6,
    "total_technologies": 23,
    "total_competences": 45,
    "total_projects": 6,
    "avg_niveau": 3.7
  }
}
```

#### GET `/dashboard/top-technologies`
Top 10 technologies maîtrisées par l'équipe.

**Query params :**
- `limit` : nombre de technologies (défaut: 10)

**Réponse :**
```json
{
  "top_technologies": [
    {
      "techno": "React",
      "nb_collaborators": 5,
      "avg_niveau": 3.8,
      "nb_experts": 3
    }
  ]
}
```

#### GET `/dashboard/at-risk-technologies`
Technologies à risque (< 2 experts).

**Query params :**
- `threshold` : nombre minimum d'experts (défaut: 2)

#### GET `/dashboard/collaborator/<id>/radar`
Profil radar d'un développeur.

**Exemple :**
```bash
curl http://localhost:5000/dashboard/collaborator/1/radar
```

**Réponse :**
```json
{
  "collaborator": {
    "id": 1,
    "name": "Jean Dupont"
  },
  "radar_data": [
    {
      "techno": "React",
      "niveau_declare": 4,
      "niveau_calcule": 4.2
    },
    {
      "techno": "PHP",
      "niveau_declare": 4,
      "niveau_calcule": 3.5
    }
  ]
}
```

#### GET `/dashboard/heatmap`
Heatmap globale des compétences.

**Query params :**
- `top_n` : limiter aux N technologies les plus utilisées

#### GET `/dashboard/statistics`
Statistiques détaillées (distribution niveaux, top projets, etc.).

---

### 13. Parsing de CV

#### POST `/cv/parse`
Parse un CV et extrait les technologies automatiquement.

**Form data :**
- `file` : fichier CV (PDF, TXT, DOCX)
- `custom_technologies` : liste optionnelle de technologies supplémentaires (JSON array)
- `collaborator_name` : nom du collaborateur (optionnel)

**Exemple :**
```bash
curl -X POST http://localhost:5000/cv/parse \
  -F "file=@cv_jean_dupont.pdf" \
  -F "collaborator_name=Jean Dupont"
```

**Réponse :**
```json
{
  "message": "CV analysé avec succès",
  "collaborator": "Jean Dupont",
  "total_technologies_detected": 8,
  "technologies": [
    {
      "technologie": "React",
      "occurrences": 12,
      "niveau_estime": 5
    },
    {
      "technologie": "Python",
      "occurrences": 5,
      "niveau_estime": 3
    }
  ],
  "text_length": 3450
}
```

**Estimation du niveau :**
- 1-2 occurrences → niveau 2
- 3-5 occurrences → niveau 3
- 6-10 occurrences → niveau 4
- >10 occurrences → niveau 5

#### POST `/cv/parse-and-import`
Parse un CV et importe automatiquement les compétences dans la base.

**Form data :**
- `file` : fichier CV
- `firstname` : prénom (requis)
- `lastname` : nom (requis)
- `custom_technologies` : technologies supplémentaires (optionnel)

**Exemple :**
```bash
curl -X POST http://localhost:5000/cv/parse-and-import \
  -F "file=@cv.pdf" \
  -F "firstname=Jean" \
  -F "lastname=Dupont"
```

**Réponse :**
```json
{
  "message": "CV importé avec succès",
  "collaborator": "Jean Dupont",
  "collaborator_id": 1,
  "created": 8,
  "updated": 2,
  "total_technologies_detected": 10
}
```

#### GET `/cv/supported-technologies`
Retourne la liste des 150+ technologies détectables automatiquement.

---

## Flux de travail complet

### 1. Importer les données initiales

```bash
# Importer les compétences déclarées (CSV)
curl -X POST http://localhost:5000/import/competences/csv \
  -F "file=@competences.csv"

# Importer les projets historiques (JSON)
curl -X POST http://localhost:5000/import/projects/json \
  -F "file=@projets.json"

# Parser des CVs (optionnel)
curl -X POST http://localhost:5000/cv/parse-and-import \
  -F "file=@cv_jean_dupont.pdf" \
  -F "firstname=Jean" \
  -F "lastname=Dupont"
```

### 2. Calculer les scores

```bash
# Recalculer tous les scores automatiquement
curl -X POST http://localhost:5000/scoring/calculate
```

### 3. Visualiser les compétences

```bash
# Voir la matrice de compétences
curl http://localhost:5000/matrix/competences

# Voir le dashboard
curl http://localhost:5000/dashboard/overview

# Voir les technologies à risque
curl http://localhost:5000/dashboard/at-risk-technologies
```

### 4. Allouer un nouveau projet

```bash
# Suggérer une équipe pour un nouveau projet
curl -X POST http://localhost:5000/allocation/suggest \
  -H "Content-Type: application/json" \
  -d '{"technologies": ["React", "Node.js", "MongoDB"], "team_size": 3}'
```

---

## Fonctionnalités MVP Complètes

✅ **1. Collecte de données**
- Import CSV/JSON compétences et projets
- Parsing automatique de CV (PDF, TXT, DOCX)
- Détection de 150+ technologies

✅ **2. Moteur de scoring automatique**
- Calcul basé sur l'historique des projets
- Prise en compte de l'ancienneté
- Algorithme transparent et paramétrable

✅ **3. Matrice de compétences interactive**
- Filtres par technologie, niveau, développeur
- Code couleur (vert/orange/rouge/gris)
- Formats multiples (détaillé, simple, heatmap)

✅ **4. Module d'allocation projet**
- Suggestion automatique des meilleurs développeurs
- Identification des gaps critiques
- Vue de capacité globale par technologie

✅ **5. Dashboard de pilotage**
- Vue globale avec métriques clés
- Top 10 technologies maîtrisées
- Technologies à risque (<2 experts)
- Graphique radar par développeur
- Heatmap des compétences
