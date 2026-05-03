from flask import Blueprint, request, jsonify
from database import db
from models import Student, StudentRegistry, OtpVerification
from werkzeug.security import generate_password_hash, check_password_hash
import re

student_bp = Blueprint("student", __name__)

@student_bp.route("/register", methods=["POST"])
def register_student():
    data = request.json

    college_id = data.get("collegeId")
    full_name = data.get("fullName")
    email = data.get("email")
    phone_no = data.get("phoneNo")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    if not all([college_id, full_name, email, phone_no, password, confirm_password]):
        return jsonify({"message": "All fields are required"}), 400

    registry_student = StudentRegistry.query.filter_by(
        college_id=college_id
    ).first()

    if not registry_student:
        return jsonify({
            "message": "Student is not registered by admin or college"
        }), 403

    if registry_student.is_registered:
        return jsonify({
            "message": "Student account already created"
        }), 409

    if not re.fullmatch(r"\d{10}", phone_no):
        return jsonify({
            "message": "Phone number must be exactly 10 digits"
        }), 400

    if password != confirm_password:
        return jsonify({
            "message": "Password and confirm password do not match"
        }), 400

    existing_email = Student.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"message": "Email already registered"}), 409

    existing_phone = Student.query.filter_by(phone_no=phone_no).first()
    if existing_phone:
        return jsonify({"message": "Phone number already registered"}), 409

    email_verified = OtpVerification.query.filter_by(
        target=email,
        otp_type="EMAIL",
        verified=True
    ).first()

    if not email_verified:
        return jsonify({"message": "Email OTP not verified"}), 400

    phone_verified = OtpVerification.query.filter_by(
        target=phone_no,
        otp_type="PHONE",
        verified=True
    ).first()

    if not phone_verified:
        return jsonify({"message": "Phone OTP not verified"}), 400

    new_student = Student(
        college_id=college_id,
        full_name=full_name,
        email=email,
        phone_no=phone_no,
        password_hash=generate_password_hash(password)
    )

    registry_student.is_registered = True

    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully"
    }), 201

@student_bp.route("/login", methods=["POST"])
def student_login():
    data = request.json

    college_id = data.get("collegeId")
    password = data.get("password")

    if not all([college_id, password]):
        return jsonify({"message": "College ID and password are required"}), 400

    student = Student.query.filter_by(college_id=college_id).first()

    if not student:
        return jsonify({"message": "Invalid credentials"}), 401

    if not check_password_hash(student.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "message": "Student login successful",
    "role": "STUDENT",
    "student": {
        "id": student.id,
        "collegeId": student.college_id,
        "fullName": student.full_name,
        "email": student.email,
        "phoneNo": student.phone_no,
        "insideHostel": student.inside_hostel
        }
    }), 200

@student_bp.route("/update-profile", methods=["PUT"])
def update_profile():
    data = request.json

    college_id = data.get("collegeId")
    full_name = data.get("fullName")
    phone_no = data.get("phoneNo")

    student = Student.query.filter_by(college_id=college_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    student.full_name = full_name
    student.phone_no = phone_no

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "student": {
            "id": student.id,
            "collegeId": student.college_id,
            "fullName": student.full_name,
            "email": student.email,
            "phoneNo": student.phone_no,
            "insideHostel": student.inside_hostel
        }
    }), 200