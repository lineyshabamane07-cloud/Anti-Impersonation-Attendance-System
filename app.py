from flask import Flask, render_template, jsonify, session, redirect, abort, request

from config import Config

from routes.auth import auth_bp
from routes.faculty import faculty_bp
from routes.student import student_bp
from routes.admin import admin_bp


DEV_USERS = {
    "faculty": {"id": 1, "name": "Demo Faculty", "role": "faculty"},
    "student": {"id": 101, "name": "Demo Student", "role": "student"},
    "admin": {"id": 2, "name": "Demo Admin", "role": "admin"},
}


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)
    app.config.setdefault("SECRET_KEY", "dev-only-change-me")

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/health")
    def health():
        return jsonify({
            "status": "ok",
            "application": "AIAS",
            "message": "AIAS server is running"
        })

    @app.route("/dev/login/<role>")
    def dev_login(role):
        # Shortcut login for building and testing. Off when DEV_MODE=false.
        if not getattr(Config, "DEV_MODE", True):
            abort(404)
        if role not in DEV_USERS:
            abort(404)
        user = dict(DEV_USERS[role])
        user_id = request.args.get("id")
        if user_id and user_id.isdigit():
            user["id"] = int(user_id)
        session.clear()
        session["user"] = user
        return redirect(f"/{role}/dashboard")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )