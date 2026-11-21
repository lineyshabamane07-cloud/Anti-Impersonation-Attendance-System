
from flask import Blueprint, jsonify, render_template, request, session

from config import Config
from decorators import role_required
from services import qr_service, report_service

faculty_bp = Blueprint("faculty", __name__)

CLASS_ID = 1 # prototype: one demo class (DAA, SY-B, room 304)


@faculty_bp.route("/dashboard")
@role_required("faculty")
def dashboard():
  return render_template("faculty/dashboard.html", user=session["user"])


@faculty_bp.route("/session/new")
@role_required("faculty")
def new_session():
  return render_template(
    "faculty/new_session.html",
    default_radius=Config.DEFAULT_GEOFENCE_METERS,
    default_refresh=Config.QR_REFRESH_SECONDS,
  )


@faculty_bp.route("/session/start", methods=["POST"])
@role_required("faculty")
def start_session():
  data = request.get_json(silent=True) or {}
  try:
     session_id = qr_service.create_session(
       CLASS_ID,
       lat=float(data["lat"]),
       lng=float(data["lng"]),
       radius_m=int(data.get("radius_m") or Config.DEFAULT_GEOFENCE_METERS),
       refresh_s=int(data.get("refresh_s") or Config.QR_REFRESH_SECONDS),
       duration_min=int(data.get("duration_min") or 10),
     )
  except (KeyError, TypeError, ValueError):
     return jsonify({"error": "Please give a valid latitude and longitude"}), 400
  return jsonify({"session_id": session_id})


@faculty_bp.route("/session/<int:session_id>")
@role_required("faculty")
def live_page(session_id):
  return render_template("faculty/live.html", session_id=session_id)


@faculty_bp.route("/session/<int:session_id>/qr")
@role_required("faculty")
def qr_json(session_id):
  return jsonify(qr_service.get_current_token(session_id))


@faculty_bp.route("/session/<int:session_id>/live")
@role_required("faculty")
def live_json(session_id):
  return jsonify({
     "marked": report_service.list_marked(session_id),
     "summary": report_service.session_summary(session_id),
  })


@faculty_bp.route("/session/<int:session_id>/end", methods=["POST"])
@role_required("faculty")
def end_session(session_id):
  qr_service.end_session(session_id)
  return jsonify({"ok": True})


@faculty_bp.route("/session/<int:session_id>/report")
@role_required("faculty")
def report(session_id):
  return render_template(
     "faculty/report.html",
     summary=report_service.session_summary(session_id),
     marked=report_service.list_marked(session_id),
  )
