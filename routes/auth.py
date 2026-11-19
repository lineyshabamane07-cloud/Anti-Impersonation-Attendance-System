# OWNER: Mrunal Kale
# TODO: POST /login (bcrypt check, set session, redirect by role), /logout,
#       and the @role_required decorator (put it in a new file decorators.py).
from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def login():
    return render_template("auth/login.html")
