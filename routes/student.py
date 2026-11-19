
from flask import Blueprint, jsonify, render_template, request, session

from decorators import role_required
from services import verify_service

student_bp = Blueprint("student", __name__)


@student_bp.route("/dashboard")
@role_required("student")
def dashboard():
    return render_template(
        "student/dashboard.html",
        user=session["user"]
    )


@student_bp.route("/scan")
@role_required("student")
def scan():
    return render_template("student/scan.html")


@student_bp.route("/mark", methods=["POST"])
@role_required("student")
def mark():
    data = request.get_json(silent=True) or {}

    token = (data.get("token") or "").strip()
    device_id = (data.get("device_id") or "").strip()

    if not token or not device_id:
        return jsonify({"error": "Missing token or device id"}), 400

    # The student's id comes from the logged-in session on the server,
    # NEVER from the browser. Otherwise anyone could mark attendance as someone else.
    result = verify_service.mark_attendance(
        token,
        session["user"]["id"],
        data.get("lat"),
        data.get("lng"),
        device_id
    )

    return jsonify(result)
