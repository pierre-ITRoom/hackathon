from flask import Blueprint, request, jsonify
from src.models import collaborator_model

bp = Blueprint('collaborators', __name__)

@bp.route("/collaborators", methods=["GET"])
def get_collaborators():
    collaborators = collaborator_model.get_all()
    return jsonify(collaborators), 200

@bp.route("/collaborators/<int:collaborator_id>", methods=["GET"])
def get_collaborator(collaborator_id):
    collaborator = collaborator_model.get_by_id(collaborator_id)
    if not collaborator:
        return jsonify({"error": "Collaborator not found"}), 404
    return jsonify(collaborator), 200

@bp.route("/collaborators", methods=["POST"])
def add_collaborator():
    data = request.get_json()
    firstname = data.get("firstname")
    lastname = data.get("lastname")

    if not firstname or not lastname:
        return jsonify({"error": "firstname and lastname are required"}), 400

    try:
        item_id = collaborator_model.create({
            "firstname": firstname,
            "lastname": lastname
        })
        return jsonify({"message": f"Collaborator {firstname} {lastname} added!", "id": item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/collaborators/<int:collaborator_id>", methods=["PATCH"])
def update_collaborator(collaborator_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    collaborator = collaborator_model.get_by_id(collaborator_id)
    if not collaborator:
        return jsonify({"error": "Collaborator not found"}), 404

    update_data = {}
    if "firstname" in data:
        update_data["firstname"] = data["firstname"]
    if "lastname" in data:
        update_data["lastname"] = data["lastname"]

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        collaborator_model.update(collaborator_id, update_data)
        return jsonify({"message": f"Collaborator {collaborator_id} updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/collaborators/<int:collaborator_id>", methods=["DELETE"])
def delete_collaborator(collaborator_id):
    collaborator = collaborator_model.get_by_id(collaborator_id)
    if not collaborator:
        return jsonify({"error": "Collaborator not found"}), 404

    try:
        collaborator_model.delete(collaborator_id)
        return jsonify({"message": f"Collaborator {collaborator_id} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
