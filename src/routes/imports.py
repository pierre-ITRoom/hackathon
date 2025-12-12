from flask import Blueprint, request, jsonify
import csv
import json
import io
import datetime
from src.config import get_db_connection
from src.models import (
    collaborator_model, techno_model, project_model,
    competence_model, project_history_model,
    collaborator_project_model, techno_project_model
)

bp = Blueprint('imports', __name__)


def get_or_create_collaborator(firstname, lastname):
    """Récupère ou crée un collaborateur"""
    conn = get_db_connection()
    collab = conn.execute(
        "SELECT * FROM collaborator WHERE firstname = ? AND lastname = ?",
        (firstname, lastname)
    ).fetchone()
    conn.close()

    if collab:
        return dict(collab)['id']
    else:
        return collaborator_model.create({
            "firstname": firstname,
            "lastname": lastname
        })


def get_or_create_techno(name):
    """Récupère ou crée une technologie"""
    conn = get_db_connection()
    techno = conn.execute(
        "SELECT * FROM techno WHERE name = ?",
        (name,)
    ).fetchone()
    conn.close()

    if techno:
        return dict(techno)['id']
    else:
        return techno_model.create({"name": name})


def get_or_create_project(name):
    """Récupère ou crée un projet"""
    conn = get_db_connection()
    proj = conn.execute(
        "SELECT * FROM project WHERE name = ?",
        (name,)
    ).fetchone()
    conn.close()

    if proj:
        return dict(proj)['id']
    else:
        return project_model.create({"name": name})


@bp.route("/import/competences/csv", methods=["POST"])
def import_competences_csv():
    """
    Import des compétences depuis un CSV
    Format attendu: nom,prenom,technologie,niveau_declare
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File must be a CSV"}), 400

    try:
        # Lire le fichier CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)

        created = 0
        updated = 0
        errors = []

        for row_num, row in enumerate(csv_reader, start=2):
            try:
                lastname = row.get('nom', '').strip()
                firstname = row.get('prenom', '').strip()
                techno_name = row.get('technologie', '').strip()
                niveau_declare = row.get('niveau_declare', '').strip()

                if not all([lastname, firstname, techno_name, niveau_declare]):
                    errors.append(f"Ligne {row_num}: Champs manquants")
                    continue

                niveau_declare = int(niveau_declare)
                if not (1 <= niveau_declare <= 5):
                    errors.append(f"Ligne {row_num}: niveau_declare doit être entre 1 et 5")
                    continue

                # Créer ou récupérer les entités
                id_collaborator = get_or_create_collaborator(firstname, lastname)
                id_techno = get_or_create_techno(techno_name)

                # Vérifier si la compétence existe déjà
                existing = competence_model.get_by_collaborator_techno(id_collaborator, id_techno)

                if existing:
                    # Mettre à jour
                    competence_model.update(existing['id'], {
                        "niveau_declare": niveau_declare,
                        "niveau_calcule": niveau_declare
                    })
                    updated += 1
                else:
                    # Créer
                    competence_model.create({
                        "id_collaborator": id_collaborator,
                        "id_techno": id_techno,
                        "niveau_declare": niveau_declare,
                        "niveau_calcule": niveau_declare
                    })
                    created += 1

            except Exception as e:
                errors.append(f"Ligne {row_num}: {str(e)}")

        return jsonify({
            "message": "Import terminé",
            "created": created,
            "updated": updated,
            "errors": errors
        }), 200

    except Exception as e:
        return jsonify({"error": f"Erreur lors du traitement du fichier: {str(e)}"}), 400


@bp.route("/import/projects/json", methods=["POST"])
def import_projects_json():
    """
    Import des projets depuis un JSON
    Format attendu: {"projets": [{"nom": "...", "technologies": [...], "equipe": [...], "duree_mois": 6, "date_fin": "2024-08"}]}
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith('.json'):
        return jsonify({"error": "File must be a JSON"}), 400

    try:
        # Lire le fichier JSON
        data = json.load(file.stream)

        if 'projets' not in data:
            return jsonify({"error": "Le JSON doit contenir une clé 'projets'"}), 400

        projets = data['projets']
        created_projects = 0
        created_history = 0
        errors = []

        for proj_num, projet in enumerate(projets, start=1):
            try:
                nom = projet.get('nom', '').strip()
                technologies = projet.get('technologies', [])
                equipe = projet.get('equipe', [])
                duree_mois = projet.get('duree_mois')
                date_fin = projet.get('date_fin')

                if not nom:
                    errors.append(f"Projet {proj_num}: nom manquant")
                    continue

                # Créer ou récupérer le projet
                id_project = get_or_create_project(nom)

                # Mettre à jour les infos du projet si fournies
                if duree_mois or date_fin:
                    update_data = {}
                    if duree_mois:
                        update_data['duree_mois'] = duree_mois
                    if date_fin:
                        update_data['date_fin'] = date_fin
                    project_model.update(id_project, update_data)

                created_projects += 1

                # Traiter les technologies
                techno_ids = []
                for techno_name in technologies:
                    id_techno = get_or_create_techno(techno_name.strip())
                    techno_ids.append(id_techno)

                    # Créer la relation techno-project (ignorer si existe)
                    try:
                        techno_project_model.create({
                            "id_techno": id_techno,
                            "id_project": id_project
                        })
                    except:
                        pass  # Relation déjà existante

                # Traiter l'équipe
                for membre in equipe:
                    # Format attendu: "Prénom Nom"
                    parts = membre.strip().split(' ', 1)
                    if len(parts) == 2:
                        firstname, lastname = parts
                    else:
                        errors.append(f"Projet {proj_num}: Format invalide pour '{membre}'")
                        continue

                    id_collaborator = get_or_create_collaborator(firstname, lastname)

                    # Créer la relation collaborator-project (ignorer si existe)
                    try:
                        collaborator_project_model.create({
                            "id_collaborator": id_collaborator,
                            "id_project": id_project
                        })
                    except:
                        pass  # Relation déjà existante

                    # Créer l'historique pour chaque techno
                    for id_techno in techno_ids:
                        history_data = {
                            "id_project": id_project,
                            "id_techno": id_techno,
                            "id_collaborator": id_collaborator
                        }

                        if duree_mois:
                            history_data['duree_mois'] = duree_mois
                        if date_fin:
                            history_data['date_fin'] = date_fin

                        project_history_model.create(history_data)
                        created_history += 1

            except Exception as e:
                errors.append(f"Projet {proj_num}: {str(e)}")

        return jsonify({
            "message": "Import terminé",
            "created_projects": created_projects,
            "created_history": created_history,
            "errors": errors
        }), 200

    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON invalide: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur lors du traitement du fichier: {str(e)}"}), 400


@bp.route("/import/competences/json", methods=["POST"])
def import_competences_json():
    """
    Import des compétences depuis un JSON
    Format attendu: [{"nom": "Dupont", "prenom": "Jean", "technologie": "PHP", "niveau_declare": 4}]
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith('.json'):
        return jsonify({"error": "File must be a JSON"}), 400

    try:
        data = json.load(file.stream)

        if not isinstance(data, list):
            return jsonify({"error": "Le JSON doit contenir un tableau"}), 400

        created = 0
        updated = 0
        errors = []

        for item_num, item in enumerate(data, start=1):
            try:
                lastname = item.get('nom', '').strip()
                firstname = item.get('prenom', '').strip()
                techno_name = item.get('technologie', '').strip()
                niveau_declare = item.get('niveau_declare')

                if not all([lastname, firstname, techno_name, niveau_declare]):
                    errors.append(f"Item {item_num}: Champs manquants")
                    continue

                if not (1 <= niveau_declare <= 5):
                    errors.append(f"Item {item_num}: niveau_declare doit être entre 1 et 5")
                    continue

                id_collaborator = get_or_create_collaborator(firstname, lastname)
                id_techno = get_or_create_techno(techno_name)

                existing = competence_model.get_by_collaborator_techno(id_collaborator, id_techno)

                if existing:
                    competence_model.update(existing['id'], {
                        "niveau_declare": niveau_declare,
                        "niveau_calcule": niveau_declare
                    })
                    updated += 1
                else:
                    competence_model.create({
                        "id_collaborator": id_collaborator,
                        "id_techno": id_techno,
                        "niveau_declare": niveau_declare,
                        "niveau_calcule": niveau_declare
                    })
                    created += 1

            except Exception as e:
                errors.append(f"Item {item_num}: {str(e)}")

        return jsonify({
            "message": "Import terminé",
            "created": created,
            "updated": updated,
            "errors": errors
        }), 200

    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON invalide: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur lors du traitement du fichier: {str(e)}"}), 400
