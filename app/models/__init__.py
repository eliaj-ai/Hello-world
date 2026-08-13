"""Database models.

Importing them here means a single `from app import models` registers every
table with SQLAlchemy.
"""

from app.models.contact_message import ContactMessage
from app.models.product import Product

__all__ = ["ContactMessage", "Product"]
