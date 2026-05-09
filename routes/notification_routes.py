from flask import Blueprint, jsonify
from datetime import datetime, timedelta

from database import db
from models import Student, ParentNotification

notification_bp = Blueprint("notification_bp", __name__)


def delete_old_notifications():
    old_date = datetime.utcnow() - timedelta(days=3)
    ParentNotification.query.filter(
        ParentNotification.created_at < old_date
    ).delete()
    db.session.commit()


@notification_bp.route("/parent/<college_id>", methods=["GET"])
def get_parent_notifications(college_id):
    try:
        delete_old_notifications()

        student = Student.query.filter_by(college_id=college_id).first()

        if not student:
            return jsonify({"message": "Student not found"}), 404

        notifications = ParentNotification.query.filter_by(
            student_id=student.id
        ).order_by(ParentNotification.created_at.desc()).all()

        result = []

        for note in notifications:
            result.append({
                "id": note.id,
                "title": note.title,
                "message": note.message,
                "isRead": note.is_read,
                "createdAt": note.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify(result), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Server error", "error": str(e)}), 500