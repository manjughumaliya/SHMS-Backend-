from flask import Blueprint, request, jsonify
from database import db
from models import Complaint, Student
from datetime import datetime

complaint_bp = Blueprint("complaint_bp", __name__)


def generate_complaint_id():
    last_complaint = Complaint.query.order_by(Complaint.id.desc()).first()

    if not last_complaint:
        return "CMP001"

    last_number = int(last_complaint.complaint_id.replace("CMP", ""))
    new_number = last_number + 1

    return f"CMP{new_number:03d}"


# Student: Raise complaint
@complaint_bp.route("/raise", methods=["POST"])
def raise_complaint():
    try:
        data = request.get_json()

        student_id = data.get("student_id")
        category = data.get("category")
        description = data.get("description")
        priority = data.get("priority")

        if not all([student_id, category, description, priority]):
            return jsonify({"message": "All fields are required"}), 400

        student = Student.query.get(student_id)

        if not student:
            return jsonify({"message": "Student not found"}), 404

        if priority not in ["Low", "Medium", "High"]:
            return jsonify({"message": "Priority must be Low, Medium, or High"}), 400

        complaint = Complaint(
            complaint_id=generate_complaint_id(),
            student_id=student_id,
            category=category,
            description=description,
            priority=priority,
            status="Open"
        )

        db.session.add(complaint)
        db.session.commit()

        return jsonify({
            "message": "Complaint submitted successfully",
            "complaint": {
                "id": complaint.id,
                "complaint_id": complaint.complaint_id,
                "category": complaint.category,
                "description": complaint.description,
                "priority": complaint.priority,
                "status": complaint.status,
                "submitted_on": complaint.submitted_on.strftime("%Y-%m-%d")
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Student: View own complaints
@complaint_bp.route("/student/<int:student_id>", methods=["GET"])
def get_student_complaints(student_id):
    try:
        complaints = Complaint.query.filter_by(student_id=student_id).order_by(
            Complaint.submitted_on.desc()
        ).all()

        result = []

        for c in complaints:
            result.append({
                "id": c.id,
                "complaint_id": c.complaint_id,
                "category": c.category,
                "description": c.description,
                "priority": c.priority,
                "status": c.status,
                "submitted_on": c.submitted_on.strftime("%Y-%m-%d")
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Admin/Warden: Get all complaints
@complaint_bp.route("/all", methods=["GET"])
def get_all_complaints():
    try:
        status = request.args.get("status")

        query = Complaint.query

        if status and status != "All":
            query = query.filter_by(status=status)

        complaints = query.order_by(Complaint.submitted_on.desc()).all()

        result = []

        for c in complaints:
            result.append({
                "id": c.id,
                "complaint_id": c.complaint_id,
                "student_id": c.student_id,
                "student_name": c.student.name if c.student else None,
                "college_id": c.student.college_id if c.student else None,
                "room_no": c.student.room_no if c.student else None,
                "category": c.category,
                "description": c.description,
                "priority": c.priority,
                "status": c.status,
                "submitted_on": c.submitted_on.strftime("%Y-%m-%d"),
                "resolved_by_role": c.resolved_by_role,
                "resolved_by_id": c.resolved_by_id
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Admin/Warden: Update complaint status
@complaint_bp.route("/update-status/<int:complaint_id>", methods=["PUT"])
def update_complaint_status(complaint_id):
    try:
        data = request.get_json()

        status = data.get("status")
        resolved_by_role = data.get("resolved_by_role")
        resolved_by_id = data.get("resolved_by_id")

        if not status:
            return jsonify({"message": "Status is required"}), 400

        if status not in ["Open", "In Progress", "Resolved", "Closed"]:
            return jsonify({
                "message": "Status must be Open, In Progress, Resolved, or Closed"
            }), 400

        complaint = Complaint.query.get(complaint_id)

        if not complaint:
            return jsonify({"message": "Complaint not found"}), 404

        complaint.status = status

        if status in ["Resolved", "Closed"]:
            complaint.resolved_by_role = resolved_by_role
            complaint.resolved_by_id = resolved_by_id

        db.session.commit()

        return jsonify({
            "message": "Complaint status updated successfully",
            "complaint": {
                "id": complaint.id,
                "complaint_id": complaint.complaint_id,
                "status": complaint.status
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Admin/Warden Dashboard Counts
@complaint_bp.route("/stats", methods=["GET"])
def complaint_stats():
    try:
        open_count = Complaint.query.filter_by(status="Open").count()
        in_progress_count = Complaint.query.filter_by(status="In Progress").count()
        resolved_count = Complaint.query.filter_by(status="Resolved").count()
        closed_count = Complaint.query.filter_by(status="Closed").count()
        total_count = Complaint.query.count()

        return jsonify({
            "total": total_count,
            "open": open_count,
            "in_progress": in_progress_count,
            "resolved": resolved_count,
            "closed": closed_count
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Delete complaint - optional admin feature
@complaint_bp.route("/delete/<int:complaint_id>", methods=["DELETE"])
def delete_complaint(complaint_id):
    try:
        complaint = Complaint.query.get(complaint_id)

        if not complaint:
            return jsonify({"message": "Complaint not found"}), 404

        db.session.delete(complaint)
        db.session.commit()

        return jsonify({"message": "Complaint deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500