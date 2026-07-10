"""Application configuration.

All settings live here, and every sensitive value is read from the
environment (the .env file) rather than being written into the source code.
That way secrets never end up in Git.

There is one class per environment. `create_app()` picks the right one.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Absolute path to the project root, so paths work no matter where the
# application is started from.
BASE_DIR = Path(__file__).resolve().parent

# Read key=value pairs from .env into the environment (if the file exists).
load_dotenv(BASE_DIR / ".env")


def _env_bool(name, default=False):
    """Read an environment variable that represents true/false."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _normalise_database_url(url):
    """Accept the `postgres://` URLs some hosting providers hand out.

    SQLAlchemy 2.x only understands the `postgresql://` form, so we rewrite
    it. Returns None if no URL was configured.
    """
    if not url:
        return None
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    """Settings shared by every environment."""

    # --- Security -----------------------------------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # CSRF tokens stay valid for the whole session rather than expiring
    # while somebody is still writing a long message.
    WTF_CSRF_TIME_LIMIT = None

    # Session cookie hardening.
    SESSION_COOKIE_HTTPONLY = True   # JavaScript cannot read the cookie
    SESSION_COOKIE_SAMESITE = "Lax"  # blocks most cross-site request abuse
    SESSION_COOKIE_SECURE = False    # overridden to True in production

    # --- Database -----------------------------------------------------
    SQLALCHEMY_DATABASE_URI = _normalise_database_url(
        os.environ.get("DATABASE_URL")
    ) or "sqlite:///" + str(BASE_DIR / "instance" / "app.db")

    # Turning this off saves memory; we do not use the event system.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Email (inactive until configured) ----------------------------
    MAIL_ENABLED = _env_bool("MAIL_ENABLED", False)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = _env_bool("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    CONTACT_RECIPIENT = os.environ.get("CONTACT_RECIPIENT")

    # --- Site ---------------------------------------------------------
    SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:5000")
    COMPANY_NAME = "SaaS AI Solutions"

    @staticmethod
    def init_app(app):
        """Hook for environment-specific setup. Overridden below."""


class DevelopmentConfig(Config):
    DEBUG = True
    # A throwaway key is acceptable locally so the app starts without setup.
    SECRET_KEY = Config.SECRET_KEY or "dev-only-insecure-key-do-not-use-in-production"


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SECRET_KEY = "testing-key"
    # An in-memory database: fast, and thrown away when the tests finish.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Disabled so tests can post forms without fetching a token first.
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    # Cookies are only sent over HTTPS in production.
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = "https"

    @staticmethod
    def init_app(app):
        # Refuse to start without a real secret key. Failing loudly here is
        # much safer than silently running an insecure site.
        if not app.config.get("SECRET_KEY"):
            raise RuntimeError(
                "SECRET_KEY must be set in the environment when FLASK_ENV=production."
            )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
