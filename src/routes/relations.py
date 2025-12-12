from flask import Blueprint, request, jsonify
from src.models import techno_type_model, techno_project_model, collaborator_project_model

bp = Blueprint('relations', __name__)

# ---------------- Techno ↔ Type ----------------
@bp.route("/techno_type", methods=["GET"])
def get_techno_type():
    relations = techno_type_model.get_all()
    return jsonify(relations), 200

@bp.route("/techno_type", methods=["POST"])
def add_techno_type():
    data = request.get_json()
    id_techno = data.get("id_techno")
    id_type = data.get("id_type")

    if not id_techno or not id_type:
        return jsonify({"error": "id_techno and id_type are required"}), 400

    try:
        techno_type_model.create({
            "id_techno": id_techno,
            "id_type": id_type
        })
        return jsonify({"message": f"Techno {id_techno} linked to Type {id_type}!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/techno_type/<int:id_techno>/<int:id_type>", methods=["DELETE"])
def delete_techno_type(id_techno, id_type):
    try:
        success = techno_type_model.delete(id_techno, id_type)
        if not success:
            return jsonify({"error": "Relation not found"}), 404
        return jsonify({"message": f"Relation between Techno {id_techno} and Type {id_type} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------- Techno ↔ Project ----------------
@bp.route("/techno_project", methods=["GET"])
def get_techno_project():
    relations = techno_project_model.get_all()
    return jsonify(relations), 200

@bp.route("/techno_project", methods=["POST"])
def add_techno_project():
    data = request.get_json()
    id_techno = data.get("id_techno")
    id_project = data.get("id_project")

    if not id_techno or not id_project:
        return jsonify({"error": "id_techno and id_project are required"}), 400

    try:
        techno_project_model.create({
            "id_techno": id_techno,
            "id_project": id_project
        })
        return jsonify({"message": f"Techno {id_techno} linked to Project {id_project}!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/techno_project/<int:id_techno>/<int:id_project>", methods=["DELETE"])
def delete_techno_project(id_techno, id_project):
    try:
        success = techno_project_model.delete(id_techno, id_project)
        if not success:
            return jsonify({"error": "Relation not found"}), 404
        return jsonify({"message": f"Relation between Techno {id_techno} and Project {id_project} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------- Collaborator ↔ Project ----------------
@bp.route("/collaborator_project", methods=["GET"])
def get_collaborator_project():
    relations = collaborator_project_model.get_all()
    return jsonify(relations), 200

@bp.route("/collaborator_project", methods=["POST"])
def add_collaborator_project():
    data = request.get_json()
    id_collaborator = data.get("id_collaborator")
    id_project = data.get("id_project")

    if not id_collaborator or not id_project:
        return jsonify({"error": "id_collaborator and id_project are required"}), 400

    try:
        collaborator_project_model.create({
            "id_collaborator": id_collaborator,
            "id_project": id_project
        })
        return jsonify({"message": f"Collaborator {id_collaborator} linked to Project {id_project}!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/collaborator_project/<int:id_collaborator>/<int:id_project>", methods=["DELETE"])
def delete_collaborator_project(id_collaborator, id_project):
    try:
        success = collaborator_project_model.delete(id_collaborator, id_project)
        if not success:
            return jsonify({"error": "Relation not found"}), 404
        return jsonify({"message": f"Relation between Collaborator {id_collaborator} and Project {id_project} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
