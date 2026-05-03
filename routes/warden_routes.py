from flask import Blueprint, request, jsonify
from models import Warden
from werkzeug.security import check_password_hash

warden_bp = Blueprint("warden", __name__)


@warden_bp.route("/login", methods=["POST"])
def warden_login():
    data = request.json

    login_id = data.get("loginId")
    password = data.get("password")

    if not all([login_id, password]):
        return jsonify({"message": "Warden ID or Email and Password are required"}), 400

    warden = Warden.query.filter(
        (Warden.email == login_id) | (Warden.warden_id == login_id)
    ).first()

    if not warden:
        return jsonify({"message": "Warden not found. Please contact admin."}), 404

    if not check_password_hash(warden.password_hash, password):
        return jsonify({"message": "Invalid password"}), 401

    return jsonify({
        "message": "Warden login successful",
        "role": "WARDEN",
        "warden": {
            "id": warden.id,
            "email": warden.email,
            "wardenId": warden.warden_id,
            "role": warden.role
        }
    }), 200