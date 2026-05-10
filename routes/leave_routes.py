from flask import Blueprint, request, jsonify
from datetime import datetime

from database import db
from models import LeaveRequest, Student, Parent, ParentNotification

leave_bp = Blueprint("leave_bp", __name__)


@leave_bp.route("/apply", methods=["POST"])
def apply_leave():
    try:
        data = request.get_json()

        student_id = data.get("student_id")
        leave_type = data.get("leave_type")
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        reason = data.get("reason")

        if not all([student_id, leave_type, from_date, to_date, reason]):
            return jsonify({"message": "All fields are required"}), 400

        student = Student.query.get(student_id)

        if not student:
            return jsonify({"message": "Student not found"}), 404

        leave = LeaveRequest(
            student_id=student_id,
            leave_type=leave_type,
            from_date=datetime.strptime(from_date, "%Y-%m-%d").date(),
            to_date=datetime.strptime(to_date, "%Y-%m-%d").date(),
            reason=reason,
            status="Pending"
        )

        db.session.add(leave)
        db.session.commit()

        return jsonify({
            "message": "Leave application submitted successfully",
            "leave": {
                "id": leave.id,
                "student_id": leave.student_id,
                "leave_type": leave.leave_type,
                "from_date": str(leave.from_date),
                "to_date": str(leave.to_date),
                "reason": leave.reason,
                "status": leave.status
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error applying leave", "error": str(e)}), 500


@leave_bp.route("/student/<int:student_id>", methods=["GET"])
def get_student_leaves(student_id):
    try:
        leaves = LeaveRequest.query.filter_by(
            student_id=student_id
        ).order_by(LeaveRequest.created_at.desc()).all()

        result = []

        for leave in leaves:
            result.append({
                "id": leave.id,
                "leave_type": leave.leave_type,
                "from_date": str(leave.from_date),
                "to_date": str(leave.to_date),
                "reason": leave.reason,
                "status": leave.status,
                "created_at": leave.created_at.isoformat()
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Error fetching leaves", "error": str(e)}), 500


@leave_bp.route("/all", methods=["GET"])
def get_all_leaves():
    try:
        status = request.args.get("status")

        query = LeaveRequest.query.join(Student)

        if status and status != "All":
            query = query.filter(LeaveRequest.status == status)

        leaves = query.order_by(LeaveRequest.created_at.desc()).all()

        result = []

        for leave in leaves:
            student = leave.student

            result.append({
                "id": leave.id,
                "leave_id": f"LV{leave.id:03d}",
                "student_id": leave.student_id,
                "student_name": student.full_name,
                "student_college_id": student.college_id,
                "leave_type": leave.leave_type,
                "from_date": str(leave.from_date),
                "to_date": str(leave.to_date),
                "reason": leave.reason,
                "status": leave.status,
                "approved_by_role": leave.approved_by_role,
                "created_at": leave.created_at.isoformat()
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Error fetching leave requests", "error": str(e)}), 500


@leave_bp.route("/<int:leave_id>/status", methods=["PUT"])
def update_leave_status(leave_id):
    try:
        data = request.get_json()

        status = data.get("status")
        approved_by_role = data.get("approved_by_role")
        approved_by_id = data.get("approved_by_id")

        if status not in ["Approved", "Rejected"]:
            return jsonify({"message": "Status must be Approved or Rejected"}), 400

        if approved_by_role not in ["Admin", "Warden"]:
            return jsonify({"message": "approved_by_role must be Admin or Warden"}), 400

        leave = LeaveRequest.query.get(leave_id)

        if not leave:
            return jsonify({"message": "Leave request not found"}), 404

        leave.status = status
        leave.approved_by_role = approved_by_role
        leave.approved_by_id = approved_by_id

        student = Student.query.get(leave.student_id)

        parent = Parent.query.filter_by(
            student_college_id=student.college_id
        ).first()

        if parent:
            title = f"Leave {status} Alert"

            if status == "Approved":
                message = (
                    f"{student.full_name}'s leave from {leave.from_date} "
                    f"to {leave.to_date} has been approved by {approved_by_role}."
                )
            else:
                message = (
                    f"{student.full_name}'s leave from {leave.from_date} "
                    f"to {leave.to_date} has been rejected by {approved_by_role}."
                )

            notification = ParentNotification(
                student_id=student.id,
                title=title,
                message=message,
                is_read=False
            )

            db.session.add(notification)

        db.session.commit()

        return jsonify({
            "message": f"Leave {status.lower()} successfully",
            "leave": {
                "id": leave.id,
                "status": leave.status,
                "approved_by_role": leave.approved_by_role
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating leave status", "error": str(e)}), 500