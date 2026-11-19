# OWNER: Tanmai Divekar
# TODO: dashboard, start-session form, live QR page, /session/<id>/qr (JSON),
#       /session/<id>/live (JSON), end session, report page.
from flask import Blueprint, render_template

faculty_bp = Blueprint("faculty", __name__)


@faculty_bp.route("/dashboard")
def dashboard():
    return render_template("faculty/dashboard.html")
