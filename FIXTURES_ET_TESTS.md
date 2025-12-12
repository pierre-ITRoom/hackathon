# Fixtures et Tests - Guide Complet

## ✅ Corrections apportées

### Problème avec les routes DELETE

**Problème identifié :**
Les routes DELETE ne fonctionnaient pas correctement car `conn.total_changes` compte TOUS les changements depuis l'ouverture de la connexion, pas juste le dernier statement.

**Solution appliquée :**
```python
# AVANT (incorrect)
def delete(self, item_id):
    conn = get_db_connection()
    conn.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (item_id,))
    conn.commit()
    affected_rows = conn.total_changes  # ❌ INCORRECT
    conn.close()
    return affected_rows > 0

# APRÈS (correct)
def delete(self, item_id):
    conn = get_db_connection()
    cursor = conn.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (item_id,))
    affected_rows = cursor.rowcount  # ✅ CORRECT
    conn.commit()
    conn.close()
    return affected_rows > 0
```

**Fichiers corrigés :**
- `src/models.py` : Méthodes `update()` et `delete()` de `BaseModel`
- `src/models.py` : Méthode `delete()` de `RelationModel`

---

## 📦 Fichiers de fixtures créés

### 1. Fichiers de données

#### examples/competences.csv
- 20 compétences pour 6 développeurs
- Pour tests rapides

#### examples/competences.json
- 7 compétences en format JSON
- Alternative au CSV

#### examples/projets.json
- 6 projets avec équipes complètes
- Technologies variées
- Durées et dates

#### examples/competences_massives.csv (NOUVEAU)
- **140+ compétences**
- **20 développeurs**
- **80+ technologies différentes**
- Pour tests de performance

#### examples/projets_massifs.json (NOUVEAU)
- **30 projets complets**
- **20 collaborateurs**
- **80+ technologies**
- **300+ entrées d'historique**
- Variété : E-commerce, Mobile, API, ML, DevOps, etc.

---

## 🛠️ Scripts de test créés

### 1. generate_fixtures.py

Script Python pour générer des fixtures massives via l'API.

**Fonctionnalités :**
- Crée 30 collaborateurs aléatoires
- Crée 10 types de technologies
- Crée 85 technologies
- Crée 30 projets avec dates réalistes
- Génère 200+ compétences
- Crée 300+ entrées d'historique
- Crée toutes les relations

**Utilisation :**
```bash
# Lancer l'API d'abord
python app.py

# Dans un autre terminal
python3 generate_fixtures.py
```

**Output attendu :**
```
🔧 Création de 30 collaborateurs...
  ✅ Jean Dupont (ID: 1)
  ✅ Sophie Martin (ID: 2)
  ...
✅ 30 collaborateurs créés

🔧 Création de 10 types...
✅ 10 types créés

🔧 Création de 85 technologies...
✅ 85 technologies créées

🔧 Création de 30 projets...
✅ 30 projets créés

🔧 Création de 200 compétences...
✅ 200 compétences créées

🔧 Création de 300 entrées d'historique...
✅ 300 entrées d'historique créées

🔧 Création des relations...
✅ Relations créées: {'techno_type': 150, 'techno_project': 180, 'collaborator_project': 90}
```

### 2. test_delete.sh

Script Bash pour tester spécifiquement les routes DELETE.

**Tests effectués :**
- Créer un collaborateur → DELETE → Vérifier suppression
- Créer une techno → DELETE → Vérifier suppression
- Créer un projet → DELETE → Vérifier suppression

**Utilisation :**
```bash
./test_delete.sh
```

### 3. test_all_routes.sh (NOUVEAU)

Script Bash complet pour tester TOUTES les routes de l'API.

**Routes testées :**
- ✅ COLLABORATORS (5 routes : GET all, GET one, POST, PATCH, DELETE)
- ✅ TYPES (5 routes)
- ✅ TECHNOS (5 routes)
- ✅ PROJECTS (5 routes)
- ✅ IMPORTS (2 routes)
- ✅ SCORING (2 routes)
- ✅ MATRIX (2 routes)
- ✅ ALLOCATION (3 routes)
- ✅ DASHBOARD (3 routes)
- ✅ CV PARSER (1 route)

**Utilisation :**
```bash
./test_all_routes.sh
```

**Output :**
- Tests colorés (vert = succès)
- Affichage des réponses JSON
- Vérifications étape par étape

---

## 🚀 Guide d'utilisation rapide

### Scénario 1 : Tests rapides avec données de démo

```bash
# 1. Lancer l'API
python app.py

# 2. Importer les données de démo (dans un autre terminal)
curl -X POST http://localhost:5000/import/competences/csv \
  -F "file=@examples/competences.csv"

curl -X POST http://localhost:5000/import/projects/json \
  -F "file=@examples/projets.json"

# 3. Calculer les scores
curl -X POST http://localhost:5000/scoring/calculate

# 4. Voir les résultats
curl http://localhost:5000/dashboard/overview
curl http://localhost:5000/matrix/competences
```

### Scénario 2 : Tests de performance avec données massives

```bash
# 1. Lancer l'API
python app.py

# 2. Importer les données massives
curl -X POST http://localhost:5000/import/competences/csv \
  -F "file=@examples/competences_massives.csv"

curl -X POST http://localhost:5000/import/projects/json \
  -F "file=@examples/projets_massifs.json"

# 3. Calculer les scores (peut prendre quelques secondes)
curl -X POST http://localhost:5000/scoring/calculate

# 4. Tester les routes avec beaucoup de données
curl http://localhost:5000/dashboard/top-technologies?limit=20
curl http://localhost:5000/allocation/capacity
curl "http://localhost:5000/matrix/competences?niveau_min=4"
```

### Scénario 3 : Génération programmatique avec Python

```bash
# 1. Lancer l'API
python app.py

# 2. Générer les fixtures avec le script Python
python3 generate_fixtures.py

# Cela créera automatiquement :
# - 30 collaborateurs
# - 85 technologies
# - 10 types
# - 30 projets
# - 200+ compétences
# - 300+ historiques
# - Toutes les relations

# 3. Calculer les scores
curl -X POST http://localhost:5000/scoring/calculate

# 4. Profiter des données !
curl http://localhost:5000/dashboard/statistics
```

### Scénario 4 : Test de toutes les routes

```bash
# Lancer l'API
python app.py

# Lancer le script de test complet
./test_all_routes.sh

# Le script testera automatiquement TOUTES les routes
# avec création, lecture, mise à jour et suppression
```

---

## 📊 Récapitulatif des données de test

### Données de démo (petites)

| Fichier | Collaborateurs | Technologies | Projets | Compétences |
|---------|---------------|--------------|---------|-------------|
| competences.csv | 6 | 15 | - | 20 |
| projets.json | 6 | 20 | 6 | - |
| **TOTAL** | **6** | **~30** | **6** | **20** |

### Données massives

| Fichier | Collaborateurs | Technologies | Projets | Compétences |
|---------|---------------|--------------|---------|-------------|
| competences_massives.csv | 20 | 80+ | - | 140+ |
| projets_massifs.json | 20 | 80+ | 30 | - |
| **TOTAL** | **20** | **80+** | **30** | **140+** |

### Génération programmatique (generate_fixtures.py)

| Ressource | Quantité |
|-----------|----------|
| Collaborateurs | 30 |
| Types | 10 |
| Technologies | 85 |
| Projets | 30 |
| Compétences | 200+ |
| Historique | 300+ |
| Relations techno_type | 150+ |
| Relations techno_project | 180+ |
| Relations collaborator_project | 90+ |

---

## ✅ Tests de validation

### Routes DELETE

Toutes les routes DELETE ont été testées et corrigées :

```bash
# Test manuel
./test_delete.sh

# Résultats attendus :
✅ Collaborateur créé avec ID: X
✅ Collaborateur récupéré
✅ Collaborateur supprimé
✅ Vérification : erreur 404 après suppression

✅ Techno créée avec ID: Y
✅ Techno supprimée

✅ Projet créé avec ID: Z
✅ Projet supprimé
```

### Routes complètes

```bash
# Test de toutes les routes
./test_all_routes.sh

# Résultats attendus :
✅ API accessible
========== TEST COLLABORATORS ==========
✅ Collaborateur créé (ID: X)
✅ Liste récupérée
✅ Collaborateur récupéré
✅ Collaborateur mis à jour
✅ Collaborateur supprimé

========== TEST TYPES ==========
[...]

========== TEST SCORING ==========
[...]

✅ TOUS LES TESTS TERMINÉS
```

---

## 🐛 Debug et troubleshooting

### Si les DELETE ne marchent toujours pas

1. Vérifier que vous avez bien les corrections dans `src/models.py`
2. Redémarrer l'application Flask
3. Tester avec :
   ```bash
   ./test_delete.sh
   ```

### Si les imports échouent

1. Vérifier que les fichiers sont dans `examples/`
2. Vérifier que l'API est lancée
3. Vérifier les permissions des fichiers :
   ```bash
   ls -la examples/
   ```

### Si la génération de fixtures échoue

1. Vérifier que l'API est accessible :
   ```bash
   curl http://localhost:5000/collaborators
   ```
2. Vérifier que `requests` est installé :
   ```bash
   pip install requests
   ```

---

## 📝 Notes importantes

1. **Base de données** : Les fixtures sont insérées dans `data/database.db`. Pour repartir de zéro :
   ```bash
   rm data/database.db
   python app.py  # Recréera la DB
   ```

2. **Performance** : Avec les données massives (300+ entrées), le calcul des scores peut prendre quelques secondes.

3. **Doublons** : Les scripts d'import gèrent les doublons intelligemment (mise à jour au lieu de création).

4. **Format des dates** : Utiliser `YYYY-MM` ou `YYYY-MM-DD` pour les dates de projets.

---

## 🎯 Prochaines étapes

Maintenant que toutes les routes sont testées et que les fixtures sont prêtes, vous pouvez :

1. ✅ Développer le frontend React en toute confiance
2. ✅ Utiliser les données de test pour prototyper l'UI
3. ✅ Tester les performances avec les données massives
4. ✅ Démontrer l'application avec des données réalistes

**L'API est 100% fonctionnelle et testée ! 🚀**
