from flask import Blueprint, request, jsonify
from database import db
from models import Parent, Student, OtpVerification
from datetime import datetime, timedelta
import random
import re

parent_bp = Blueprint("parent", __name__)


def generate_otp():
    return str(random.randint(100000, 999999))


@parent_bp.route("/send-login-otp", methods=["POST"])
def send_parent_login_otp():
    data = request.json

    phone_no = data.get("phoneNo")
    college_id = data.get("collegeId")

    if not all([phone_no, college_id]):
        return jsonify({"message": "Phone number and College ID are required"}), 400

    if not re.fullmatch(r"\d{10}", phone_no):
        return jsonify({"message": "Phone number must be exactly 10 digits"}), 400

    parent = Parent.query.filter_by(
        phone_no=phone_no,
        student_college_id=college_id
    ).first()

    if not parent:
        return jsonify({"message": "Parent not registered with this student"}), 404

    student = Student.query.filter_by(college_id=college_id).first()

    if not student:
        return jsonify({"message": "Linked student not found"}), 404

    old_otps = OtpVerification.query.filter_by(
        target=phone_no,
        otp_type="PARENT_LOGIN"
    ).all()

    for old in old_otps:
        db.session.delete(old)

    otp = generate_otp()

    new_otp = OtpVerification(
        target=phone_no,
        otp=otp,
        otp_type="PARENT_LOGIN",
        verified=False,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.session.add(new_otp)
    db.session.commit()

    print(f"PARENT OTP for {phone_no}: {otp}")

    return jsonify({
        "message": "OTP sent successfully",
        "devOtp": otp
    }), 200


@parent_bp.route("/verify-login-otp", methods=["POST"])
def verify_parent_login_otp():
    data = request.json

    phone_no = data.get("phoneNo")
    college_id = data.get("collegeId")
    otp = data.get("otp")

    if not all([phone_no, college_id, otp]):
        return jsonify({"message": "Phone number, College ID and OTP are required"}), 400

    parent = Parent.query.filter_by(
        phone_no=phone_no,
        student_college_id=college_id
    ).first()

    if not parent:
        return jsonify({"message": "Parent not registered with this student"}), 404

    record = OtpVerification.query.filter_by(
        target=phone_no,
        otp=otp,
        otp_type="PARENT_LOGIN"
    ).first()

    if not record:
        return jsonify({"message": "Invalid OTP"}), 400

    if record.expires_at < datetime.utcnow():
        return jsonify({"message": "OTP expired"}), 400

    student = Student.query.filter_by(college_id=college_id).first()

    if not student:
        return jsonify({"message": "Linked student not found"}), 404

    record.verified = True
    db.session.commit()

    return jsonify({
        "message": "Parent login successful",
        "role": "PARENT",
        "parent": {
            "id": parent.id,
            "phoneNo": parent.phone_no,
            "collegeId": parent.student_college_id
        },
        "student": {
            "id": student.id,
            "collegeId": student.college_id,
            "fullName": student.full_name,
            "email": student.email,
            "phoneNo": student.phone_no,
            "insideHostel": student.inside_hostel
        }
    }), 200