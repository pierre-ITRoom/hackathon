from flask import Blueprint, request, jsonify
from src.models import type_model

bp = Blueprint('types', __name__)

@bp.route("/types", methods=["GET"])
def get_types():
    types = type_model.get_all()
    return jsonify(types), 200

@bp.route("/types/<int:type_id>", methods=["GET"])
def get_type(type_id):
    type_item = type_model.get_by_id(type_id)
    if not type_item:
        return jsonify({"error": "Type not found"}), 404
    return jsonify(type_item), 200

@bp.route("/types", methods=["POST"])
def add_type():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "name is required"}), 400

    try:
        item_id = type_model.create({"name": name})
        return jsonify({"message": f"Type {name} added!", "id": item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/types/<int:type_id>", methods=["PATCH"])
def update_type(type_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    type_item = type_model.get_by_id(type_id)
    if not type_item:
        return jsonify({"error": "Type not found"}), 404

    if "name" not in data:
        return jsonify({"error": "name field is required"}), 400

    try:
        type_model.update(type_id, {"name": data["name"]})
        return jsonify({"message": f"Type {type_id} updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/types/<int:type_id>", methods=["DELETE"])
def delete_type(type_id):
    type_item = type_model.get_by_id(type_id)
    if not type_item:
        return jsonify({"error": "Type not found"}), 404

    try:
        type_model.delete(type_id)
        return jsonify({"message": f"Type {type_id} deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
