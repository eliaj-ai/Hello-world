"""The Product table.

Right now the website renders products from `app/services/catalog.py`, which
keeps the marketing copy in version control where it can be reviewed. This
table mirrors that catalogue so a future admin dashboard can edit products
without a code change. Run `flask seed-products` to populate it.
"""

from datetime import datetime, timezone

from app.extensions import db


def _utcnow():
    return datetime.now(timezone.utc)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # The URL-friendly identifier, e.g. "via-ciao" -> /products/via-ciao
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)

    name = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(200))
    audience = db.Column(db.String(160))
    summary = db.Column(db.Text)

    # Controls the order products appear in on the website.
    display_order = db.Column(db.Integer, default=0, nullable=False)
    is_published = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )

    def __repr__(self):
        return f"<Product {self.slug}>"
