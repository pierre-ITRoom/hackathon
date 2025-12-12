from flask import Blueprint, request, jsonify
from src.models import project_model

bp = Blueprint('projects', __name__)

@bp.route("/projects", methods=["GET"])
def get_projects():
    projects = project_model.get_all()
    return jsonify(projects), 200

@bp.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    project = project_model.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project), 200

@bp.route("/projects", methods=["POST"])
def add_project():
    data = request.get_json()
    name = data.get("name")
    date_fin = data.get("date_fin")
    duree_mois = data.get("duree_mois")

    if not name:
        return jsonify({"error": "name is required"}), 400

    project_data = {"name": name}
    if date_fin:
        project_data["date_fin"] = date_fin
    if duree_mois:
        project_data["duree_mois"] = duree_mois

    try:
        item_id = project_model.create(project_data)
        return jsonify({"message": f"Project {name} added!", "id": item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/projects/<int:project_id>", methods=["PATCH"])
def update_project(project_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    project = project_model.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    update_data = {}
    if "name" in data:
        update_data["name"] = data["name"]
    if "date_fin" in data:
        update_data["date_fin"] = data["date_fin"]
    if "duree_mois" in data:
        update_data["duree_mois"] = data["duree_mois"]

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        project_model.update(project_id, update_data)
        return jsonify({"message": f"Project {project_id} updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = project_model.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    try:
        project_model.delete(project_id)
        return jsonify({"message": f"Project {project_id} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
