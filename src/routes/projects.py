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

    if not name:
        return jsonify({"error": "name is required"}), 400

    try:
        item_id = project_model.create({"name": name})
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

    if "name" not in data:
        return jsonify({"error": "name field is required"}), 400

    try:
        project_model.update(project_id, {"name": data["name"]})
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
