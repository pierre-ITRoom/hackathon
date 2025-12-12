#!/bin/bash
# Script de test des routes DELETE

BASE_URL="http://localhost:5000"

echo "=========================================="
echo "TEST DES ROUTES DELETE"
echo "=========================================="

# Créer un collaborateur de test
echo -e "\n1. Création d'un collaborateur de test..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/collaborators" \
  -H "Content-Type: application/json" \
  -d '{"firstname": "Test", "lastname": "Delete"}')

echo "Réponse: $CREATE_RESPONSE"

# Extraire l'ID (simple parsing)
COLLAB_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [ -z "$COLLAB_ID" ]; then
    echo "❌ Impossible de créer le collaborateur de test"
    exit 1
fi

echo "✅ Collaborateur créé avec ID: $COLLAB_ID"

# Vérifier qu'il existe
echo -e "\n2. Vérification que le collaborateur existe..."
GET_RESPONSE=$(curl -s "$BASE_URL/collaborators/$COLLAB_ID")
echo "GET /collaborators/$COLLAB_ID:"
echo "$GET_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$GET_RESPONSE"

# Tester DELETE
echo -e "\n3. Test DELETE du collaborateur..."
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/collaborators/$COLLAB_ID")
echo "DELETE /collaborators/$COLLAB_ID:"
echo "$DELETE_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$DELETE_RESPONSE"

# Vérifier qu'il n'existe plus
echo -e "\n4. Vérification que le collaborateur a été supprimé..."
GET_AFTER_DELETE=$(curl -s "$BASE_URL/collaborators/$COLLAB_ID")
echo "GET /collaborators/$COLLAB_ID après DELETE:"
echo "$GET_AFTER_DELETE" | python3 -m json.tool 2>/dev/null || echo "$GET_AFTER_DELETE"

# Test avec une techno
echo -e "\n=========================================="
echo "TEST DELETE TECHNO"
echo "=========================================="

echo -e "\n1. Création d'une techno de test..."
CREATE_TECHNO=$(curl -s -X POST "$BASE_URL/technos" \
  -H "Content-Type: application/json" \
  -d '{"name": "TestTechno"}')

echo "Réponse: $CREATE_TECHNO"
TECHNO_ID=$(echo $CREATE_TECHNO | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [ -z "$TECHNO_ID" ]; then
    echo "❌ Impossible de créer la techno de test"
    exit 1
fi

echo "✅ Techno créée avec ID: $TECHNO_ID"

echo -e "\n2. Test DELETE de la techno..."
DELETE_TECHNO=$(curl -s -X DELETE "$BASE_URL/technos/$TECHNO_ID")
echo "DELETE /technos/$TECHNO_ID:"
echo "$DELETE_TECHNO" | python3 -m json.tool 2>/dev/null || echo "$DELETE_TECHNO"

# Test avec un projet
echo -e "\n=========================================="
echo "TEST DELETE PROJECT"
echo "=========================================="

echo -e "\n1. Création d'un projet de test..."
CREATE_PROJECT=$(curl -s -X POST "$BASE_URL/projects" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "duree_mois": 3}')

echo "Réponse: $CREATE_PROJECT"
PROJECT_ID=$(echo $CREATE_PROJECT | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Impossible de créer le projet de test"
    exit 1
fi

echo "✅ Projet créé avec ID: $PROJECT_ID"

echo -e "\n2. Test DELETE du projet..."
DELETE_PROJECT=$(curl -s -X DELETE "$BASE_URL/projects/$PROJECT_ID")
echo "DELETE /projects/$PROJECT_ID:"
echo "$DELETE_PROJECT" | python3 -m json.tool 2>/dev/null || echo "$DELETE_PROJECT"

echo -e "\n=========================================="
echo "✅ TESTS TERMINÉS"
echo "=========================================="
