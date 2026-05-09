from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, date
import uuid

from database import db
from models import Student, EntryExitQR, EntryExitLog, ParentNotification

entry_exit_bp = Blueprint("entry_exit_bp", __name__)


def delete_old_notifications():
    old_date = datetime.utcnow() - timedelta(days=3)
    ParentNotification.query.filter(
        ParentNotification.created_at < old_date
    ).delete()
    db.session.commit()


@entry_exit_bp.route("/generate-qr", methods=["POST"])
def generate_qr():
    try:
        data = request.get_json()
        action = data.get("action")

        if not action:
            return jsonify({"message": "Action is required"}), 400

        action = action.upper()

        if action not in ["ENTRY", "EXIT"]:
            return jsonify({"message": "Action must be ENTRY or EXIT"}), 400

        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(seconds=45)

        qr = EntryExitQR(
            token=token,
            action=action,
            expires_at=expires_at
        )

        db.session.add(qr)
        db.session.commit()

        return jsonify({
            "message": "QR generated successfully",
            "token": token,
            "action": action,
            "expiresAt": expires_at.strftime("%Y-%m-%d %H:%M:%S")
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Server error", "error": str(e)}), 500


@entry_exit_bp.route("/scan-qr", methods=["POST"])
def scan_qr():
    try:
        delete_old_notifications()

        data = request.get_json()

        college_id = data.get("collegeId")
        token = data.get("token")

        if not college_id or not token:
            return jsonify({"message": "College ID and QR token are required"}), 400

        student = Student.query.filter_by(college_id=college_id).first()

        if not student:
            return jsonify({"message": "Student not found"}), 404

        qr = EntryExitQR.query.filter_by(token=token).first()

        if not qr:
            return jsonify({"message": "Invalid QR code"}), 400

        if qr.expires_at < datetime.utcnow():
            return jsonify({"message": "QR code expired. Please scan new QR."}), 400

        log = EntryExitLog(
            student_id=student.id,
            action=qr.action
        )

        student.inside_hostel = True if qr.action == "ENTRY" else False

        notification = ParentNotification(
            student_id=student.id,
            title=f"Student {qr.action.title()} Alert",
            message=f"{student.full_name} has marked {qr.action.title()} at {datetime.now().strftime('%I:%M %p')}."
        )

        db.session.add(log)
        db.session.add(notification)
        db.session.commit()

        return jsonify({
            "message": f"{qr.action.title()} recorded successfully",
            "insideHostel": student.inside_hostel,
            "log": {
                "logId": f"LOG{log.id:03d}",
                "studentName": student.full_name,
                "studentId": student.college_id,
                "room": getattr(student, "room_no", "N/A"),
                "action": log.action.title(),
                "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Server error", "error": str(e)}), 500


@entry_exit_bp.route("/all", methods=["GET"])
def get_all_logs():
    logs = EntryExitLog.query.order_by(EntryExitLog.timestamp.desc()).all()

    result = []

    for log in logs:
        result.append({
            "logId": f"LOG{log.id:03d}",
            "studentName": log.student.full_name,
            "studentId": log.student.college_id,
            "room": getattr(log.student, "room_no", "N/A"),
            "action": log.action.title(),
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(result), 200


@entry_exit_bp.route("/student/<college_id>", methods=["GET"])
def get_student_logs(college_id):
    student = Student.query.filter_by(college_id=college_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    logs = EntryExitLog.query.filter_by(student_id=student.id).order_by(
        EntryExitLog.timestamp.desc()
    ).all()

    result = []

    for log in logs:
        result.append({
            "logId": f"LOG{log.id:03d}",
            "action": log.action.title(),
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({
        "insideHostel": student.inside_hostel,
        "logs": result
    }), 200


@entry_exit_bp.route("/stats", methods=["GET"])
def get_stats():
    try:
        today = date.today()

        # Today's entries
        today_entries = EntryExitLog.query.filter(
            db.func.date(EntryExitLog.timestamp) == today,
            EntryExitLog.action == "ENTRY"
        ).count()

        # Today's exits
        today_exits = EntryExitLog.query.filter(
            db.func.date(EntryExitLog.timestamp) == today,
            EntryExitLog.action == "EXIT"
        ).count()

        # Students currently outside hostel
        currently_out = Student.query.filter_by(
            inside_hostel=False
        ).count()

        return jsonify({
            "todayEntries": today_entries,
            "todayExits": today_exits,
            "currentlyOut": currently_out
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to fetch stats",
            "error": str(e)
        }), 500