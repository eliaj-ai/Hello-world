"""The ContactMessage table: one row per contact-form submission."""

from datetime import datetime, timezone

from app.extensions import db


def _utcnow():
    """Timezone-aware UTC timestamp.

    Storing times in UTC avoids confusion when the site is used from
    different countries.
    """
    return datetime.now(timezone.utc)


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    company = db.Column(db.String(160))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # Kept for spam investigation and rate limiting. This is personal data,
    # so a real deployment should have a retention policy for it.
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))

    # Set to True once somebody has dealt with the message. A future admin
    # dashboard uses this to separate new enquiries from handled ones.
    is_handled = db.Column(db.Boolean, default=False, nullable=False, index=True)

    created_at = db.Column(db.DateTime(timezone=True), default=_utcnow, nullable=False)

    def __repr__(self):
        return f"<ContactMessage {self.id} from {self.email}>"
