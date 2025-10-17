# app/__init__.py
import os
from flask import Flask, render_template
from .db import db


def create_app(config_class='app.config.Config'):
    """Application factory pattern."""

    # --- CORRECTION ---
    # Define absolute paths from the location of this file (__file__)
    # This is the most reliable method.
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        instance_path=os.path.join(APP_ROOT, '../instance'),
        static_folder=os.path.join(APP_ROOT, 'static'),
        template_folder=os.path.join(APP_ROOT, 'templates')
    )
    # --- END CORRECTION ---

    app.config.from_object(config_class)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from .routes.api import api_bp
    from .routes.admin import admin_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Create database tables in application context
    with app.app_context():
        db.create_all()

    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('index.html')

    return app