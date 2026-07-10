"""The contact form and its server-side validation rules.

Flask-WTF gives us three things for free:
  1. CSRF protection - a hidden token proving the form came from our site.
  2. Server-side validation - the browser can be bypassed, so every rule
     here is enforced again on the server, which is what actually counts.
  3. Safe re-rendering - if validation fails, the visitor's text is returned
     to them escaped, so it cannot inject HTML or JavaScript.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContactForm(FlaskForm):
    name = StringField(
        "Full name",
        validators=[
            DataRequired(message="Please tell us your name."),
            Length(min=2, max=120, message="Your name should be 2-120 characters."),
        ],
        render_kw={"placeholder": "Jane Doe", "autocomplete": "name", "maxlength": 120},
    )

    email = StringField(
        "Work email",
        validators=[
            DataRequired(message="Please enter your email address."),
            Email(message="That does not look like a valid email address."),
            Length(max=255),
        ],
        render_kw={
            "placeholder": "jane@company.com",
            "autocomplete": "email",
            "inputmode": "email",
            "maxlength": 255,
        },
    )

    company = StringField(
        "Company (optional)",
        validators=[Optional(), Length(max=160)],
        render_kw={
            "placeholder": "Your company or agency",
            "autocomplete": "organization",
            "maxlength": 160,
        },
    )

    subject = StringField(
        "Subject",
        validators=[
            DataRequired(message="Please add a subject."),
            Length(min=3, max=200, message="The subject should be 3-200 characters."),
        ],
        render_kw={"placeholder": "Which product are you interested in?", "maxlength": 200},
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Please write your message."),
            Length(
                min=10,
                max=4000,
                message="Your message should be between 10 and 4000 characters.",
            ),
        ],
        render_kw={
            "placeholder": "Tell us a little about what you need.",
            "rows": 6,
            "maxlength": 4000,
        },
    )

    # A honeypot: a field hidden from people by CSS, but visible to simple
    # spam bots. It deliberately has NO validation rule, so a filled-in
    # honeypot still counts as a valid form. The route then discards the
    # submission silently and shows the normal success page - a bot that
    # gets an error message learns it was caught and adapts, whereas one
    # that gets "success" does not. This stops a lot of automated spam
    # without troubling real visitors with a captcha.
    website = StringField(
        "Leave this field empty",
        validators=[Optional()],
        render_kw={"tabindex": "-1", "autocomplete": "off", "aria-hidden": "true"},
    )

    submit = SubmitField("Send message")
