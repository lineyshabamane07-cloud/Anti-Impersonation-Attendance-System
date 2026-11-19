from flask import Flask, render_template, jsonify

from config import Config

from routes.auth import auth_bp
from routes.faculty import faculty_bp
from routes.student import student_bp
from routes.admin import admin_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
