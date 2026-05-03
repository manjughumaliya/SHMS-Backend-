from flask import Blueprint, request, jsonify, current_app
from database import db
from models import StudentRegistry, Student, Warden, Parent
from werkzeug.security import generate_password_hash

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
    registry_ids = StudentRegistry.query.order_by(StudentRegistry.id.asc()).all()

    result = []

    for item in registry_ids:
        student = Student.query.filter_by(college_id=item.college_id).first()

        result.append({
            "id": item.id,
            "collegeId": item.college_id,
            "fullName": student.full_name if student else "-",
            "email": student.email if student else "-",
            "phoneNo": student.phone_no if student else "-",
            "passwordHash": student.password_hash if student else "-",
            "status": (
                "Inside"
                if student and student.inside_hostel
                else "Outside"
                if student
                else "Not Registered"
            )
        })

    return jsonify(result), 200

@admin_bp.route("/add-warden", methods=["POST"])
def add_warden():
    data = request.json

    email = data.get("email")
    warden_id = data.get("wardenId")
    password = data.get("password")

    if not all([email, warden_id, password]):
        return jsonify({"message": "Email, Warden ID and Password are required"}), 400

    existing_email = Warden.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"message": "Warden email already exists"}), 409

    existing_id = Warden.query.filter_by(warden_id=warden_id).first()
    if existing_id:
        return jsonify({"message": "Warden ID already exists"}), 409

    new_warden = Warden(
        email=email,
        warden_id=warden_id,
        password_hash=generate_password_hash(password),
        role="WARDEN"
    )

    db.session.add(new_warden)
    db.session.commit()

    return jsonify({"message": "Warden added successfully"}), 201


@admin_bp.route("/wardens", methods=["GET"])
def get_wardens():
    wardens = Warden.query.order_by(Warden.id.asc()).all()

    result = []

    for warden in wardens:
        result.append({
            "id": warden.id,
            "email": warden.email,
            "wardenId": warden.warden_id,
            "role": warden.role
        })

    return jsonify(result), 200


@admin_bp.route("/reset-warden-password", methods=["POST"])
def reset_warden_password():
    data = request.json

    warden_id = data.get("wardenId")
    new_password = data.get("password")

    if not all([warden_id, new_password]):
        return jsonify({"message": "Warden ID and new password are required"}), 400

    warden = Warden.query.filter_by(warden_id=warden_id).first()

    if not warden:
        return jsonify({"message": "Warden not found"}), 404

    warden.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"message": "Warden password reset successfully"}), 200

@admin_bp.route("/add-parent", methods=["POST"])
def add_parent():
    data = request.json

    phone_no = data.get("phoneNo")
    college_id = data.get("collegeId")

    if not all([phone_no, college_id]):
        return jsonify({"message": "Phone number and College ID are required"}), 400

    student = Student.query.filter_by(college_id=college_id).first()

    if not student:
        return jsonify({"message": "Student not found. Student must register first."}), 404

    existing = Parent.query.filter_by(
        phone_no=phone_no,
        student_college_id=college_id
    ).first()

    if existing:
        return jsonify({"message": "Parent already linked with this student"}), 409

    parent = Parent(
        phone_no=phone_no,
        student_college_id=college_id
    )

    db.session.add(parent)
    db.session.commit()

    return jsonify({"message": "Parent added successfully"}), 201


@admin_bp.route("/parents", methods=["GET"])
def get_parents():
    parents = Parent.query.order_by(Parent.id.asc()).all()

    result = []

    for parent in parents:
        student = Student.query.filter_by(
            college_id=parent.student_college_id
        ).first()

        result.append({
            "id": parent.id,
            "phoneNo": parent.phone_no,
            "collegeId": parent.student_college_id,
            "studentName": student.full_name if student else "-"
        })

    return jsonify(result), 200