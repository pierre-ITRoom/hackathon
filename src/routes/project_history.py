from flask import Blueprint, request, jsonify
from src.models import project_history_model

bp = Blueprint('project_history', __name__)

@bp.route("/project_history", methods=["GET"])
def get_project_history():
    history = project_history_model.get_all()
    return jsonify(history), 200

@bp.route("/project_history/<int:history_id>", methods=["GET"])
def get_history_item(history_id):
    history = project_history_model.get_by_id(history_id)
    if not history:
        return jsonify({"error": "History item not found"}), 404
    return jsonify(history), 200

@bp.route("/project_history/project/<int:project_id>", methods=["GET"])
def get_history_by_project(project_id):
    history = project_history_model.get_by_project(project_id)
    return jsonify(history), 200

@bp.route("/project_history/collaborator/<int:collaborator_id>", methods=["GET"])
def get_history_by_collaborator(collaborator_id):
    history = project_history_model.get_by_collaborator(collaborator_id)
    return jsonify(history), 200

@bp.route("/project_history/techno/<int:techno_id>", methods=["GET"])
def get_history_by_techno(techno_id):
    history = project_history_model.get_by_techno(techno_id)
    return jsonify(history), 200

@bp.route("/project_history", methods=["POST"])
def add_history():
    data = request.get_json()
    id_project = data.get("id_project")
    id_techno = data.get("id_techno")
    id_collaborator = data.get("id_collaborator")
    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")
    duree_mois = data.get("duree_mois")

    if not id_project or not id_techno or not id_collaborator:
        return jsonify({"error": "id_project, id_techno and id_collaborator are required"}), 400

    history_data = {
        "id_project": id_project,
        "id_techno": id_techno,
        "id_collaborator": id_collaborator
    }

    if date_debut:
        history_data["date_debut"] = date_debut
    if date_fin:
        history_data["date_fin"] = date_fin
    if duree_mois:
        history_data["duree_mois"] = duree_mois

    try:
        item_id = project_history_model.create(history_data)
        return jsonify({"message": "Project history added!", "id": item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/project_history/<int:history_id>", methods=["PATCH"])
def update_history(history_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    history = project_history_model.get_by_id(history_id)
    if not history:
        return jsonify({"error": "History item not found"}), 404

    update_data = {}
    if "date_debut" in data:
        update_data["date_debut"] = data["date_debut"]
    if "date_fin" in data:
        update_data["date_fin"] = data["date_fin"]
    if "duree_mois" in data:
        update_data["duree_mois"] = data["duree_mois"]

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        project_history_model.update(history_id, update_data)
        return jsonify({"message": f"History {history_id} updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/project_history/<int:history_id>", methods=["DELETE"])
def delete_history(history_id):
    history = project_history_model.get_by_id(history_id)
    if not history:
        return jsonify({"error": "History item not found"}), 404

    try:
        project_history_model.delete(history_id)
        return jsonify({"message": f"History {history_id} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
