# OWNER: Reet Lunkad
# TODO: dashboard, scan page, POST /mark (calls Lineysha's verify service),
#       result screen, history page.
from flask import Blueprint, render_template

student_bp = Blueprint("student", __name__)


@student_bp.route("/dashboard")
def dashboard():
    return render_template("student/dashboard.html")
