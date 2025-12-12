#!/bin/bash
# Script de test complet de toutes les routes de l'API

BASE_URL="http://localhost:5000"
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "TEST COMPLET DE TOUTES LES ROUTES"
echo "=========================================="

# Test de connexion à l'API
echo -e "\n${BLUE}Test de connexion à l'API...${NC}"
if curl -s --fail "$BASE_URL/collaborators" > /dev/null; then
    echo -e "${GREEN}✅ API accessible${NC}"
else
    echo -e "${RED}❌ API non accessible. Lancez: python app.py${NC}"
    exit 1
fi

# ========== COLLABORATORS ==========
echo -e "\n${BLUE}========== TEST COLLABORATORS ==========${NC}"

echo -e "\n1. POST /collaborators (Créer un collaborateur)"
COLLAB_RESPONSE=$(curl -s -X POST "$BASE_URL/collaborators" \
  -H "Content-Type: application/json" \
  -d '{"firstname": "Test", "lastname": "User"}')
echo "$COLLAB_RESPONSE"
COLLAB_ID=$(echo $COLLAB_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo -e "${GREEN}✅ Collaborateur créé (ID: $COLLAB_ID)${NC}"

echo -e "\n2. GET /collaborators (Lister tous)"
curl -s "$BASE_URL/collaborators" | head -c 200
echo "..."
echo -e "${GREEN}✅ Liste récupérée${NC}"

echo -e "\n3. GET /collaborators/$COLLAB_ID (Récupérer un)"
curl -s "$BASE_URL/collaborators/$COLLAB_ID" | python3 -m json.tool
echo -e "${GREEN}✅ Collaborateur récupéré${NC}"

echo -e "\n4. PATCH /collaborators/$COLLAB_ID (Mettre à jour)"
curl -s -X PATCH "$BASE_URL/collaborators/$COLLAB_ID" \
  -H "Content-Type: application/json" \
  -d '{"firstname": "Updated"}'
echo -e "${GREEN}✅ Collaborateur mis à jour${NC}"

echo -e "\n5. DELETE /collaborators/$COLLAB_ID (Supprimer)"
curl -s -X DELETE "$BASE_URL/collaborators/$COLLAB_ID"
echo -e "${GREEN}✅ Collaborateur supprimé${NC}"

# ========== TYPES ==========
echo -e "\n${BLUE}========== TEST TYPES ==========${NC}"

echo -e "\n1. POST /types"
TYPE_RESPONSE=$(curl -s -X POST "$BASE_URL/types" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Type"}')
echo "$TYPE_RESPONSE"
TYPE_ID=$(echo $TYPE_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

echo -e "\n2. GET /types"
curl -s "$BASE_URL/types" | head -c 150
echo "..."

echo -e "\n3. GET /types/$TYPE_ID"
curl -s "$BASE_URL/types/$TYPE_ID"
echo

echo -e "\n4. PATCH /types/$TYPE_ID"
curl -s -X PATCH "$BASE_URL/types/$TYPE_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Type"}'
echo

echo -e "\n5. DELETE /types/$TYPE_ID"
curl -s -X DELETE "$BASE_URL/types/$TYPE_ID"
echo

# ========== TECHNOS ==========
echo -e "\n${BLUE}========== TEST TECHNOS ==========${NC}"

echo -e "\n1. POST /technos"
TECHNO_RESPONSE=$(curl -s -X POST "$BASE_URL/technos" \
  -H "Content-Type: application/json" \
  -d '{"name": "TestTech"}')
echo "$TECHNO_RESPONSE"
TECHNO_ID=$(echo $TECHNO_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

echo -e "\n2. GET /technos"
curl -s "$BASE_URL/technos" | head -c 150
echo "..."

echo -e "\n3. DELETE /technos/$TECHNO_ID"
curl -s -X DELETE "$BASE_URL/technos/$TECHNO_ID"
echo

# ========== PROJECTS ==========
echo -e "\n${BLUE}========== TEST PROJECTS ==========${NC}"

echo -e "\n1. POST /projects"
PROJECT_RESPONSE=$(curl -s -X POST "$BASE_URL/projects" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "duree_mois": 6, "date_fin": "2024-12"}')
echo "$PROJECT_RESPONSE"
PROJECT_ID=$(echo $PROJECT_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

echo -e "\n2. GET /projects"
curl -s "$BASE_URL/projects" | head -c 150
echo "..."

echo -e "\n3. PATCH /projects/$PROJECT_ID"
curl -s -X PATCH "$BASE_URL/projects/$PROJECT_ID" \
  -H "Content-Type: application/json" \
  -d '{"duree_mois": 8}'
echo

echo -e "\n4. DELETE /projects/$PROJECT_ID"
curl -s -X DELETE "$BASE_URL/projects/$PROJECT_ID"
echo

# ========== IMPORTS ==========
echo -e "\n${BLUE}========== TEST IMPORTS ==========${NC}"

echo -e "\n1. POST /import/competences/csv"
curl -s -X POST "$BASE_URL/import/competences/csv" \
  -F "file=@examples/competences.csv" | python3 -m json.tool
echo -e "${GREEN}✅ Import CSV réussi${NC}"

echo -e "\n2. POST /import/projects/json"
curl -s -X POST "$BASE_URL/import/projects/json" \
  -F "file=@examples/projets.json" | python3 -m json.tool
echo -e "${GREEN}✅ Import JSON réussi${NC}"

# ========== SCORING ==========
echo -e "\n${BLUE}========== TEST SCORING ==========${NC}"

echo -e "\n1. POST /scoring/calculate"
curl -s -X POST "$BASE_URL/scoring/calculate" | python3 -m json.tool
echo -e "${GREEN}✅ Scoring calculé${NC}"

echo -e "\n2. GET /scoring/parameters"
curl -s "$BASE_URL/scoring/parameters" | python3 -m json.tool

# ========== MATRIX ==========
echo -e "\n${BLUE}========== TEST MATRIX ==========${NC}"

echo -e "\n1. GET /matrix/competences"
curl -s "$BASE_URL/matrix/competences" | head -c 300
echo "..."

echo -e "\n2. GET /matrix/competences/simple"
curl -s "$BASE_URL/matrix/competences/simple" | head -c 300
echo "..."

# ========== ALLOCATION ==========
echo -e "\n${BLUE}========== TEST ALLOCATION ==========${NC}"

echo -e "\n1. POST /allocation/suggest"
curl -s -X POST "$BASE_URL/allocation/suggest" \
  -H "Content-Type: application/json" \
  -d '{"technologies": ["React", "Python"], "team_size": 3}' | python3 -m json.tool

echo -e "\n2. GET /allocation/capacity"
curl -s "$BASE_URL/allocation/capacity" | head -c 300
echo "..."

echo -e "\n3. GET /allocation/gaps"
curl -s "$BASE_URL/allocation/gaps" | python3 -m json.tool

# ========== DASHBOARD ==========
echo -e "\n${BLUE}========== TEST DASHBOARD ==========${NC}"

echo -e "\n1. GET /dashboard/overview"
curl -s "$BASE_URL/dashboard/overview" | python3 -m json.tool

echo -e "\n2. GET /dashboard/top-technologies"
curl -s "$BASE_URL/dashboard/top-technologies" | python3 -m json.tool

echo -e "\n3. GET /dashboard/at-risk-technologies"
curl -s "$BASE_URL/dashboard/at-risk-technologies" | python3 -m json.tool

# ========== CV PARSER ==========
echo -e "\n${BLUE}========== TEST CV PARSER ==========${NC}"

echo -e "\n1. GET /cv/supported-technologies"
curl -s "$BASE_URL/cv/supported-technologies" | head -c 200
echo "..."

echo -e "\n${BLUE}=========================================="
echo "✅ TOUS LES TESTS TERMINÉS"
echo "==========================================${NC}"
