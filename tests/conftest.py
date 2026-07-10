"""Shared test setup.

pytest finds this file automatically. The functions marked `@pytest.fixture`
are building blocks a test can ask for simply by naming them as arguments.

Every test runs against a fresh in-memory database, so tests never touch
your real data and never interfere with one another.
"""

import sys
from pathlib import Path

import pytest

# Make the project root importable, so `from app import create_app` works
# no matter which directory pytest was started from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app  # noqa: E402
from app.extensions import db as _db  # noqa: E402


@pytest.fixture()
def app():
    """A Flask application configured for testing."""
    application = create_app("testing")

    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    """A fake browser that can request pages without a real server."""
    return app.test_client()


@pytest.fixture()
def db(app):  # noqa: ARG001 - `app` is required so the context is active
    """The database handle, inside an active application context."""
    return _db


@pytest.fixture()
def valid_contact_payload():
    """Form data that should pass every validation rule."""
    return {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "company": "Example Travel",
        "subject": "Question about Via Ciao",
        "message": "We run a travel agency and would like to know more about Via Ciao.",
        "website": "",  # the honeypot must stay empty
    }
