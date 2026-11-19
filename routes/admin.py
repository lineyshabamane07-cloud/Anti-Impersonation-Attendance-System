# OWNER: Mrunal Kale
# TODO: read-only users list + flagged attempts list.
from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")
