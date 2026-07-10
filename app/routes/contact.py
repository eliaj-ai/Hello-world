"""The contact form: display, validation, storage and confirmation."""

import time
from collections import defaultdict

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)

from app.extensions import db
from app.forms import ContactForm
from app.models import ContactMessage
from app.services.mail import send_contact_notification
from app.utils.seo import page_title

contact_bp = Blueprint("contact", __name__)

# --- A deliberately simple rate limiter ------------------------------------
# Submissions are tracked per IP address in memory. This is enough to stop
# casual form flooding on a single server. A production deployment running
# several server processes should move this to Redis or a proper extension
# such as Flask-Limiter, because each process keeps its own copy of this.
_RATE_LIMIT_MAX = 5           # submissions allowed ...
_RATE_LIMIT_WINDOW = 60 * 10  # ... per 10 minutes, per IP address
_submission_log = defaultdict(list)


def _client_ip():
    """Best-effort visitor IP address.

    Behind a proxy, `request.remote_addr` is the proxy itself. The real
    address arrives in X-Forwarded-For. Only trust that header if a trusted
    proxy is actually in front of the app - see the README.
    """
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()[:45]
    return (request.remote_addr or "unknown")[:45]


def _is_rate_limited(ip):
    """True if this IP has submitted too many times recently."""
    now = time.time()
    recent = [t for t in _submission_log[ip] if now - t < _RATE_LIMIT_WINDOW]
    _submission_log[ip] = recent
    return len(recent) >= _RATE_LIMIT_MAX


def _record_submission(ip):
    _submission_log[ip].append(time.time())


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    # `validate_on_submit()` is True only for a POST whose CSRF token is
    # valid AND whose fields pass every rule in ContactForm.
    if form.validate_on_submit():
        ip = _client_ip()

        if _is_rate_limited(ip):
            abort(429)

        # The honeypot field is invisible to people. If it has content, a bot
        # filled it in. We pretend the submission succeeded so the bot does
        # not learn it was detected, but we store nothing.
        if form.website.data:
            current_app.logger.info("Honeypot triggered from %s. Message discarded.", ip)
            return redirect(url_for("contact.success"))

        message = ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            company=(form.company.data or "").strip() or None,
            subject=form.subject.data.strip(),
            message=form.message.data.strip(),
            ip_address=ip,
            user_agent=request.headers.get("User-Agent", "")[:255],
        )

        db.session.add(message)
        db.session.commit()
        _record_submission(ip)

        # Email is off unless configured; a failure here is not the visitor's
        # problem, because their message is already stored.
        send_contact_notification(message)

        # Redirect after a successful POST so refreshing the confirmation
        # page cannot send the message a second time.
        return redirect(url_for("contact.success"))

    return render_template(
        "pages/contact.html",
        title=page_title("Contact"),
        meta_description=(
            "Get in touch with SaaS AI Solutions about Via Ciao, Hotel App, "
            "Scan Fox, LocalGuide4me, or a project of your own."
        ),
        form=form,
    )


@contact_bp.route("/contact/success")
def success():
    return render_template(
        "pages/contact_success.html",
        title=page_title("Message sent"),
        meta_description="Your message has been received by SaaS AI Solutions.",
    )
