from database import db
from datetime import datetime

class StudentRegistry(db.Model):
    __tablename__ = "student_registry"

    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.String(50), unique=True, nullable=False)
    is_registered = db.Column(db.Boolean, default=False)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_no = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    inside_hostel = db.Column(db.Boolean, default=True)

class OtpVerification(db.Model):
    __tablename__ = "otp_verifications"

    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(120), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    otp_type = db.Column(db.String(20), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Warden(db.Model):
    __tablename__ = "wardens"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    warden_id = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="WARDEN")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Parent(db.Model):
    __tablename__ = "parents"

    id = db.Column(db.Integer, primary_key=True)
    phone_no = db.Column(db.String(10), nullable=False)
    student_college_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)