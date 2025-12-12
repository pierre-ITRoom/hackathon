from flask import Blueprint, request, jsonify
from src.models import competence_model

bp = Blueprint('competences', __name__)

@bp.route("/competences", methods=["GET"])
def get_competences():
    competences = competence_model.get_all()
    return jsonify(competences), 200

@bp.route("/competences/<int:competence_id>", methods=["GET"])
def get_competence(competence_id):
    competence = competence_model.get_by_id(competence_id)
    if not competence:
        return jsonify({"error": "Competence not found"}), 404
    return jsonify(competence), 200

@bp.route("/competences/collaborator/<int:collaborator_id>", methods=["GET"])
def get_competences_by_collaborator(collaborator_id):
    competences = competence_model.get_by_collaborator(collaborator_id)
    return jsonify(competences), 200

@bp.route("/competences/techno/<int:techno_id>", methods=["GET"])
def get_competences_by_techno(techno_id):
    competences = competence_model.get_by_techno(techno_id)
    return jsonify(competences), 200

@bp.route("/competences/collaborator/<int:collaborator_id>/techno/<int:techno_id>", methods=["GET"])
def get_competence_by_collaborator_techno(collaborator_id, techno_id):
    competence = competence_model.get_by_collaborator_techno(collaborator_id, techno_id)
    if not competence:
        return jsonify({"error": "Competence not found"}), 404
    return jsonify(competence), 200

@bp.route("/competences", methods=["POST"])
def add_competence():
    data = request.get_json()
    id_collaborator = data.get("id_collaborator")
    id_techno = data.get("id_techno")
    niveau_declare = data.get("niveau_declare")
    niveau_calcule = data.get("niveau_calcule", niveau_declare)

    if not id_collaborator or not id_techno or not niveau_declare:
        return jsonify({"error": "id_collaborator, id_techno and niveau_declare are required"}), 400

    if not (1 <= niveau_declare <= 5):
        return jsonify({"error": "niveau_declare must be between 1 and 5"}), 400

    if niveau_calcule and not (1 <= niveau_calcule <= 5):
        return jsonify({"error": "niveau_calcule must be between 1 and 5"}), 400

    try:
        item_id = competence_model.create({
            "id_collaborator": id_collaborator,
            "id_techno": id_techno,
            "niveau_declare": niveau_declare,
            "niveau_calcule": niveau_calcule
        })
        return jsonify({"message": f"Competence added!", "id": item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/competences/<int:competence_id>", methods=["PATCH"])
def update_competence(competence_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    competence = competence_model.get_by_id(competence_id)
    if not competence:
        return jsonify({"error": "Competence not found"}), 404

    update_data = {}

    if "niveau_declare" in data:
        if not (1 <= data["niveau_declare"] <= 5):
            return jsonify({"error": "niveau_declare must be between 1 and 5"}), 400
        update_data["niveau_declare"] = data["niveau_declare"]

    if "niveau_calcule" in data:
        if not (1 <= data["niveau_calcule"] <= 5):
            return jsonify({"error": "niveau_calcule must be between 1 and 5"}), 400
        update_data["niveau_calcule"] = data["niveau_calcule"]

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        competence_model.update(competence_id, update_data)
        return jsonify({"message": f"Competence {competence_id} updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/competences/<int:competence_id>", methods=["DELETE"])
def delete_competence(competence_id):
    competence = competence_model.get_by_id(competence_id)
    if not competence:
        return jsonify({"error": "Competence not found"}), 404

    try:
        competence_model.delete(competence_id)
        return jsonify({"message": f"Competence {competence_id} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
