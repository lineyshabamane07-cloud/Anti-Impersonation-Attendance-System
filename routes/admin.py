
from flask import Blueprint, render_template, request, session

from decorators import role_required
from services import auth_service, report_service

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():

    return render_template(
        "admin/dashboard.html",
        user=session["user"]
    )


@admin_bp.route("/attempts")
@role_required("admin")
def attempts():

    show_all = request.args.get("all") == "1"

    rows = report_service.list_attempts(
        only_problems=not show_all
    )

    return render_template(
        "admin/attempts.html",
        rows=rows,
        show_all=show_all
    )


@admin_bp.route("/users")
@role_required("admin")
def users():

    return render_template(
        "admin/users.html",
        rows=auth_service.list_users()
    )

