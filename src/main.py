"""
Entry point for the MountainHub backend.

This module configures the Flask application, initialises the SQLAlchemy
database and registers all API blueprints. Running this script will
bootstrap the app for local development. In production environments the
``Procfile`` refers to ``src.main:app`` for Gunicorn.
"""

import os
import sys

from flask import Flask, send_from_directory
from flask_cors import CORS

# Ensure the package root is on the path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from .models import db  # noqa: E402
from .routes.user import user_bp  # noqa: E402
from .routes.trail import trail_bp  # noqa: E402
from .routes.equipment import equipment_bp  # noqa: E402
from .routes.external import external_bp  # noqa: E402
from .routes.trip_log import trip_log_bp  # noqa: E402
from .routes.guide import guide_bp  # noqa: E402


def create_app() -> Flask:
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')
    # SQLite database file stored in ``src/database/app.db``
    db_path = os.path.join(os.path.dirname(__file__), 'database')
    os.makedirs(db_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(db_path, 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise and create tables
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register CORS and blueprints
    CORS(app)
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(trail_bp, url_prefix='/api')
    app.register_blueprint(equipment_bp, url_prefix='/api')
    app.register_blueprint(external_bp, url_prefix='/api/external')
    app.register_blueprint(trip_log_bp, url_prefix='/api')
    app.register_blueprint(guide_bp, url_prefix='/api')

    # Serve static files (e.g., frontend build) if present
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path: str):
        static_folder_path = app.static_folder
        if static_folder_path and path and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        index_path = os.path.join(static_folder_path, 'index.html') if static_folder_path else None
        if index_path and os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        return "Static content not found", 404

    return app


# Create the app instance used by Gunicorn
app = create_app()


if __name__ == '__main__':
    # Run in development mode
    app.run(host='0.0.0.0', port=5000, debug=True)
