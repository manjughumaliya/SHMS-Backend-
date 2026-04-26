from flask import Blueprint, request, jsonify, current_app
from database import db
from models import StudentRegistry

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if (
        email == current_app.config["ADMIN_EMAIL"]
        and password == current_app.config["ADMIN_PASSWORD"]
    ):
        return jsonify({
            "message": "Admin login successful",
            "role": "ADMIN"
        }), 200

    return jsonify({"message": "Invalid admin email or password"}), 401


@admin_bp.route("/add-college-id", methods=["POST"])
def add_college_id():
    data = request.json
    college_id = data.get("collegeId")

    if not college_id:
        return jsonify({"message": "College ID is required"}), 400

    existing = StudentRegistry.query.filter_by(college_id=college_id).first()

    if existing:
        return jsonify({"message": "College ID already exists"}), 409

    new_entry = StudentRegistry(college_id=college_id)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "College ID added successfully"}), 201


@admin_bp.route("/college-ids", methods=["GET"])
def get_college_ids():
    ids = StudentRegistry.query.all()

    result = []

    for item in ids:
        result.append({
            "id": item.id,
            "collegeId": item.college_id,
            "isRegistered": item.is_registered
        })

    return jsonify(result), 200