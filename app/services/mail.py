"""Email delivery for contact-form notifications.

IMPORTANT - EMAIL IS SWITCHED OFF BY DEFAULT.

No email is sent unless MAIL_ENABLED=true and the SMTP settings are filled in
in the .env file. Until then, contact messages are simply stored in the
database and this module reports that sending was skipped.

The code below uses Python's built-in `smtplib`, so no extra dependency is
needed. Everything sensitive (server, username, password) is read from the
configuration, never written here.
"""

import smtplib
from email.message import EmailMessage

from flask import current_app


def _is_configured():
    """True when every setting needed to send email is present."""
    cfg = current_app.config
    required = (
        cfg.get("MAIL_SERVER"),
        cfg.get("MAIL_DEFAULT_SENDER"),
        cfg.get("CONTACT_RECIPIENT"),
    )
    return cfg.get("MAIL_ENABLED") and all(required)


def send_contact_notification(message):
    """Notify the company that a contact message arrived.

    Args:
        message: a saved ContactMessage row.

    Returns:
        True  - an email was sent.
        False - sending was skipped or failed. The caller must treat this as
                non-fatal: the message is already safely in the database, so
                the visitor should still see a success page.
    """
    if not _is_configured():
        current_app.logger.info(
            "Contact message %s stored. Email sending is disabled or not configured.",
            message.id,
        )
        return False

    cfg = current_app.config

    email = EmailMessage()
    email["Subject"] = f"[Website enquiry] {message.subject}"
    email["From"] = cfg["MAIL_DEFAULT_SENDER"]
    email["To"] = cfg["CONTACT_RECIPIENT"]
    # Replies go to the person who filled in the form.
    email["Reply-To"] = message.email
    email.set_content(
        "A new message was submitted through the website.\n\n"
        f"Name:    {message.name}\n"
        f"Email:   {message.email}\n"
        f"Company: {message.company or '-'}\n"
        f"Subject: {message.subject}\n\n"
        f"Message:\n{message.message}\n\n"
        f"Received: {message.created_at:%Y-%m-%d %H:%M UTC}\n"
        f"Reference: #{message.id}\n"
    )

    try:
        with smtplib.SMTP(cfg["MAIL_SERVER"], cfg["MAIL_PORT"], timeout=10) as server:
            if cfg.get("MAIL_USE_TLS"):
                server.starttls()
            if cfg.get("MAIL_USERNAME"):
                server.login(cfg["MAIL_USERNAME"], cfg["MAIL_PASSWORD"])
            server.send_message(email)
    except Exception:
        # The visitor's message is already saved, so a delivery failure must
        # not turn into an error page for them. It is logged for us instead.
        current_app.logger.exception(
            "Failed to send notification email for contact message %s.", message.id
        )
        return False

    return True
