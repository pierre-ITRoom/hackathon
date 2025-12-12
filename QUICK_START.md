# Quick Start - API Gestion des Compétences

## Installation ultra-rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
python app.py
```

L'API est disponible sur **http://localhost:5000**

---

## Test rapide (30 secondes)

```bash
# Terminal 1 - Lancer l'API
python app.py

# Terminal 2 - Charger les fixtures et tester
curl -X POST http://localhost:5000/import/competences/csv -F "file=@examples/competences.csv"
curl -X POST http://localhost:5000/import/projects/json -F "file=@examples/projets.json"
curl -X POST http://localhost:5000/scoring/calculate
curl http://localhost:5000/dashboard/overview | python3 -m json.tool
```

---

## Routes principales

### Données de base
```bash
# Collaborateurs
GET    /collaborators
POST   /collaborators
PATCH  /collaborators/<id>
DELETE /collaborators/<id>

# Technologies (idem pour /types, /projects)
GET    /technos
POST   /technos
PATCH  /technos/<id>
DELETE /technos/<id>
```

### Import de données
```bash
POST /import/competences/csv     # Upload CSV
POST /import/competences/json    # Upload JSON
POST /import/projects/json       # Upload projets
POST /cv/parse-and-import        # Parser CV
```

### Fonctionnalités MVP
```bash
# Scoring
POST /scoring/calculate

# Matrice
GET  /matrix/competences
GET  /matrix/competences?niveau_min=4

# Allocation
POST /allocation/suggest
  Body: {"technologies": ["React", "Python"], "team_size": 3}

# Dashboard
GET  /dashboard/overview
GET  /dashboard/top-technologies
GET  /dashboard/at-risk-technologies
GET  /dashboard/collaborator/<id>/radar
```

---

## Exemples concrets

### Créer un collaborateur
```bash
curl -X POST http://localhost:5000/collaborators \
  -H "Content-Type: application/json" \
  -d '{"firstname": "Jean", "lastname": "Dupont"}'
```

### Suggérer une équipe pour un projet
```bash
curl -X POST http://localhost:5000/allocation/suggest \
  -H "Content-Type: application/json" \
  -d '{"technologies": ["React", "Node.js"], "team_size": 3}' \
  | python3 -m json.tool
```

### Voir la matrice de compétences
```bash
curl "http://localhost:5000/matrix/competences?niveau_min=3" \
  | python3 -m json.tool
```

---

## Tests

### Tester toutes les routes
```bash
./test_all_routes.sh
```

### Générer beaucoup de fixtures
```bash
python3 generate_fixtures.py
```

### Tester les DELETE
```bash
./test_delete.sh
```

---

## Fichiers de fixtures

| Fichier | Contenu |
|---------|---------|
| `examples/competences.csv` | 20 compétences, 6 devs |
| `examples/projets.json` | 6 projets |
| `examples/competences_massives.csv` | 140+ compétences, 20 devs |
| `examples/projets_massifs.json` | 30 projets |

---

## Workflow complet

```bash
# 1. Importer les données
curl -X POST http://localhost:5000/import/competences/csv \
  -F "file=@examples/competences_massives.csv"

curl -X POST http://localhost:5000/import/projects/json \
  -F "file=@examples/projets_massifs.json"

# 2. Calculer les scores automatiques
curl -X POST http://localhost:5000/scoring/calculate

# 3. Voir le dashboard
curl http://localhost:5000/dashboard/overview | python3 -m json.tool

# 4. Voir les technologies à risque
curl http://localhost:5000/dashboard/at-risk-technologies | python3 -m json.tool

# 5. Suggérer une équipe
curl -X POST http://localhost:5000/allocation/suggest \
  -H "Content-Type: application/json" \
  -d '{"technologies": ["React", "Python", "Docker"], "team_size": 5}' \
  | python3 -m json.tool
```

---

## Dépannage

### L'API ne démarre pas
```bash
# Vérifier Python
python --version  # Doit être 3.9+

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Les imports ne marchent pas
```bash
# Vérifier que l'API tourne
curl http://localhost:5000/collaborators

# Vérifier les fichiers
ls -la examples/
```

### Repartir de zéro
```bash
# Supprimer la base de données
rm data/database.db

# Relancer l'API (recrée la DB)
python app.py
```

---

## Documentation complète

- **README.md** : Documentation complète de l'API
- **MVP_COMPLET.md** : Récapitulatif du MVP
- **FIXTURES_ET_TESTS.md** : Guide des fixtures et tests
- **examples/README.md** : Guide des fichiers exemples

---

**L'API est prête ! Il ne reste plus qu'à créer le frontend React.** 🚀
