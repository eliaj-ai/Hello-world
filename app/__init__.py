"""Application factory.

`create_app()` builds and returns a configured Flask application. Using a
factory (rather than a single global `app` object) means the tests can create
a separate application with its own throwaway database, and it keeps the
project ready for multiple environments.
"""

import os
from pathlib import Path

from flask import Flask, render_template

from config import config

from .extensions import csrf, db


def create_app(config_name=None):
    """Build the application.

    Args:
        config_name: "development", "testing" or "production".
                     Falls back to the FLASK_ENV environment variable.
    """
    config_name = config_name or os.environ.get("FLASK_ENV", "default")
    config_class = config.get(config_name, config["default"])

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    config_class.init_app(app)

    # SQLite needs the folder holding the database file to exist.
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    _register_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    _register_security_headers(app)
    _register_template_globals(app)
    _register_cli_commands(app)

    return app


def _register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)

    # Importing the models registers them with SQLAlchemy's metadata, which
    # is what `db.create_all()` needs in order to build the tables.
    from app import models  # noqa: F401  (imported for its side effects)

    with app.app_context():
        db.create_all()


def _register_blueprints(app):
    """Attach each group of routes.

    Blueprints let us split the URLs across several files instead of one
    giant module: main pages, product pages, and the contact form.
    """
    from app.routes.contact import contact_bp
    from app.routes.main import main_bp
    from app.routes.products import products_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(contact_bp)


def _register_error_handlers(app):
    """Show friendly branded pages instead of raw error text."""

    @app.errorhandler(404)
    def not_found(error):  # noqa: ARG001 - Flask passes the error object
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):  # noqa: ARG001
        # Roll back any half-finished database work so the next request
        # starts from a clean session.
        db.session.rollback()
        return render_template("errors/500.html"), 500

    @app.errorhandler(429)
    def too_many_requests(error):  # noqa: ARG001
        return render_template("errors/429.html"), 429


def _register_security_headers(app):
    """Add HTTP headers that tell the browser to behave defensively.

    These are cheap, standard protections against common attacks such as
    clickjacking and content-type sniffing.
    """

    @app.after_request
    def set_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Permissions-Policy", "geolocation=(), microphone=(), camera=()"
        )
        # The site loads no third-party scripts, styles, fonts or images, so
        # a strict Content-Security-Policy costs us nothing.
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self'; "
            "script-src 'self'; base-uri 'self'; form-action 'self'; "
            "frame-ancestors 'none'",
        )
        if not app.debug and not app.testing:
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        return response


def _register_template_globals(app):
    """Values every template can use without passing them from each route."""
    from datetime import datetime

    from app.services.catalog import get_products

    @app.context_processor
    def inject_globals():
        return {
            "company_name": app.config["COMPANY_NAME"],
            "current_year": datetime.now().year,
            "nav_products": get_products(),
            "site_url": app.config["SITE_URL"],
        }


def _register_cli_commands(app):
    """Extra `flask` terminal commands."""

    @app.cli.command("init-db")
    def init_db():
        """Create the database tables. Run with: flask init-db"""
        db.create_all()
        print("Database tables created.")

    @app.cli.command("seed-products")
    def seed_products():
        """Copy the product catalogue into the database.

        Run with: flask seed-products

        The website itself reads the catalogue from Python, so this is only
        needed once an admin dashboard exists to edit products.
        """
        from app.services.catalog import seed_products_table

        created = seed_products_table()
        print(f"Products synchronised. {created} new row(s) created.")
