from flask import Blueprint, request, jsonify
from database import db
from models import OtpVerification
from services.email_service import send_email_otp
from services.sms_service import send_phone_otp
from datetime import datetime, timedelta
import random
import re

otp_bp = Blueprint("otp", __name__)

def generate_otp():
    return str(random.randint(100000, 999999))


@otp_bp.route("/send-email", methods=["POST"])
def send_email():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    otp = generate_otp()

    old_otps = OtpVerification.query.filter_by(
        target=email,
        otp_type="EMAIL"
    ).all()

    for old in old_otps:
        db.session.delete(old)

    new_otp = OtpVerification(
        target=email,
        otp=otp,
        otp_type="EMAIL",
        verified=False,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.session.add(new_otp)
    db.session.commit()

    try:
        send_email_otp(email, otp)
        return jsonify({"message": "Email OTP sent successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to send email OTP", "error": str(e)}), 500


@otp_bp.route("/verify-email", methods=["POST"])
def verify_email():
    data = request.json
    email = data.get("email")
    otp = data.get("otp")

    record = OtpVerification.query.filter_by(
        target=email,
        otp=otp,
        otp_type="EMAIL"
    ).first()

    if not record:
        return jsonify({"message": "Invalid email OTP"}), 400

    if record.expires_at < datetime.utcnow():
        return jsonify({"message": "Email OTP expired"}), 400

    record.verified = True
    db.session.commit()

    return jsonify({"message": "Email verified successfully"}), 200


@otp_bp.route("/send-phone", methods=["POST"])
def send_phone():
    data = request.json
    phone_no = data.get("phoneNo")

    if not phone_no:
        return jsonify({"message": "Phone number is required"}), 400

    if not re.fullmatch(r"\d{10}", phone_no):
        return jsonify({"message": "Phone number must be exactly 10 digits"}), 400

    otp = generate_otp()

    # 🧹 Delete old OTPs
    old_otps = OtpVerification.query.filter_by(
        target=phone_no,
        otp_type="PHONE"
    ).all()

    for old in old_otps:
        db.session.delete(old)

    # 💾 Save new OTP
    new_otp = OtpVerification(
        target=phone_no,
        otp=otp,
        otp_type="PHONE",
        verified=False,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.session.add(new_otp)
    db.session.commit()

    print(f"PHONE OTP for {phone_no}: {otp}")

    return jsonify({
        "message": "Phone OTP generated successfully",
        "devOtp": otp
    }), 200

@otp_bp.route("/verify-phone", methods=["POST"])
def verify_phone():
    data = request.json
    phone_no = data.get("phoneNo")
    otp = data.get("otp")

    record = OtpVerification.query.filter_by(
        target=phone_no,
        otp=otp,
        otp_type="PHONE"
    ).first()

    if not record:
        return jsonify({"message": "Invalid phone OTP"}), 400

    if record.expires_at < datetime.utcnow():
        return jsonify({"message": "Phone OTP expired"}), 400

    record.verified = True
    db.session.commit()

    return jsonify({"message": "Phone verified successfully"}), 200