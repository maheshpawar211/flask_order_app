import os

from flask import Flask, jsonify

from config import config_by_name
from .api import api_bp
from .cli import register_cli_commands
from .extensions import db, ma, migrate


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    env_name = config_name or os.getenv("APP_ENV", "development")
    app.config.from_object(config_by_name.get(env_name, config_by_name["development"]))

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    register_cli_commands(app)

    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"message": "Internal server error"}), 500

    return app
