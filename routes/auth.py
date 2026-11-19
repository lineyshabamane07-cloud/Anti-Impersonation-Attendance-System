
import secrets

from flask import (
    Blueprint, abort, flash, redirect,
    render_template, request, session, url_for
)

from services import auth_service

auth_bp = Blueprint("auth", __name__)


def _csrf_token():
    """Generate a CSRF token."""

    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)

    return session["csrf"]


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        expected = session.get("csrf")

        if not expected or request.form.get("csrf") != expected:
            abort(400)

        result = auth_service.authenticate(
            request.form.get("user_code", "").strip(),
            request.form.get("password", "")
        )

        if result["ok"]:
            user = result["user"]

            session.clear()
            session["user"] = user

            return redirect(url_for(f"{user['role']}.dashboard"))

        flash(result["error"], "danger")

    return render_template(
        "auth/login.html",
        csrf=_csrf_token()
    )


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))
