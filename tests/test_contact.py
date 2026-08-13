"""Tests for the contact form: validation, storage and spam handling."""

from app.models import ContactMessage


def test_contact_page_loads(client):
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"<form" in response.data


def test_contact_form_includes_csrf_field(app):
    """The CSRF token must be rendered even though it is off during tests.

    Without it, a different website could submit this form on a visitor's
    behalf. This test checks the field is really in the HTML.
    """
    app.config["WTF_CSRF_ENABLED"] = True
    body = app.test_client().get("/contact").get_data(as_text=True)
    assert 'name="csrf_token"' in body


def test_valid_submission_is_saved(client, db, valid_contact_payload):
    response = client.post("/contact", data=valid_contact_payload)

    # A successful submission redirects, so refreshing cannot resend it.
    assert response.status_code == 302
    assert "/contact/success" in response.headers["Location"]

    saved = db.session.query(ContactMessage).one()
    assert saved.name == "Jane Doe"
    assert saved.email == "jane@example.com"
    assert saved.company == "Example Travel"
    assert saved.is_handled is False


def test_email_is_stored_lowercase(client, db, valid_contact_payload):
    valid_contact_payload["email"] = "JANE@EXAMPLE.COM"
    client.post("/contact", data=valid_contact_payload)
    assert db.session.query(ContactMessage).one().email == "jane@example.com"


def test_empty_company_is_stored_as_none(client, db, valid_contact_payload):
    valid_contact_payload["company"] = "   "
    client.post("/contact", data=valid_contact_payload)
    assert db.session.query(ContactMessage).one().company is None


def test_missing_required_fields_are_rejected(client, db):
    response = client.post("/contact", data={"name": "", "email": "", "message": ""})

    # The page is re-shown with errors rather than redirecting.
    assert response.status_code == 200
    assert db.session.query(ContactMessage).count() == 0


def test_invalid_email_is_rejected(client, db, valid_contact_payload):
    valid_contact_payload["email"] = "not-an-email"
    response = client.post("/contact", data=valid_contact_payload)

    assert response.status_code == 200
    assert b"valid email address" in response.data
    assert db.session.query(ContactMessage).count() == 0


def test_short_message_is_rejected(client, db, valid_contact_payload):
    valid_contact_payload["message"] = "hi"
    response = client.post("/contact", data=valid_contact_payload)

    assert response.status_code == 200
    assert db.session.query(ContactMessage).count() == 0


def test_over_long_name_is_rejected(client, db, valid_contact_payload):
    valid_contact_payload["name"] = "a" * 200
    client.post("/contact", data=valid_contact_payload)
    assert db.session.query(ContactMessage).count() == 0


def test_honeypot_submission_is_discarded(client, db, valid_contact_payload):
    """A bot that fills the hidden field is silently ignored."""
    valid_contact_payload["website"] = "http://spam.example"
    response = client.post("/contact", data=valid_contact_payload)

    # The bot sees the normal success redirect ...
    assert response.status_code == 302
    # ... but nothing was stored.
    assert db.session.query(ContactMessage).count() == 0


def test_rate_limit_blocks_flooding(client, db, valid_contact_payload):
    """Too many submissions from one address get a 429 page."""
    from app.routes.contact import _RATE_LIMIT_MAX, _submission_log

    _submission_log.clear()

    for _ in range(_RATE_LIMIT_MAX):
        assert client.post("/contact", data=valid_contact_payload).status_code == 302

    blocked = client.post("/contact", data=valid_contact_payload)
    assert blocked.status_code == 429
    assert db.session.query(ContactMessage).count() == _RATE_LIMIT_MAX

    _submission_log.clear()


def test_submitted_text_is_escaped_not_executed(client, db, valid_contact_payload):
    """Cross-site scripting check.

    A message containing HTML must be stored as plain text and, when shown
    again, escaped rather than treated as markup.
    """
    valid_contact_payload["subject"] = "<script>alert('xss')</script>"
    valid_contact_payload["message"] = "short"  # forces the form to redisplay

    response = client.post("/contact", data=valid_contact_payload)
    body = response.get_data(as_text=True)

    assert "<script>alert('xss')</script>" not in body
    assert "&lt;script&gt;" in body


def test_success_page_loads(client):
    response = client.get("/contact/success")
    assert response.status_code == 200
    assert b"received" in response.data
