from flask import Blueprint, request, jsonify
from src.models import techno_model

bp = Blueprint('technos', __name__)

@bp.route("/technos", methods=["GET"])
def get_technos():
    technos = techno_model.get_all()
    return jsonify(technos), 200

@bp.route("/technos/<int:techno_id>", methods=["GET"])
def get_techno(techno_id):
    techno = techno_model.get_by_id(techno_id)
    if not techno:
        return jsonify({"error": "Techno not found"}), 404
    return jsonify(techno), 200

@bp.route("/technos", methods=["POST"])
def add_techno():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "name is required"}), 400

    try:
        item_id = techno_model.create({"name": name})
        return jsonify({"message": f"Techno {name} added!", "id": item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/technos/<int:techno_id>", methods=["PATCH"])
def update_techno(techno_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    techno = techno_model.get_by_id(techno_id)
    if not techno:
        return jsonify({"error": "Techno not found"}), 404

    if "name" not in data:
        return jsonify({"error": "name field is required"}), 400

    try:
        techno_model.update(techno_id, {"name": data["name"]})
        return jsonify({"message": f"Techno {techno_id} updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/technos/<int:techno_id>", methods=["DELETE"])
def delete_techno(techno_id):
    techno = techno_model.get_by_id(techno_id)
    if not techno:
        return jsonify({"error": "Techno not found"}), 404

    try:
        techno_model.delete(techno_id)
        return jsonify({"message": f"Techno {techno_id} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
