"""Tests for the database models and the product catalogue."""

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import ContactMessage, Product
from app.services.catalog import get_product, get_products, seed_products_table


def test_contact_message_defaults(db):
    message = ContactMessage(
        name="Test Person",
        email="test@example.com",
        subject="Hello",
        message="A message long enough to be valid.",
    )
    db.session.add(message)
    db.session.commit()

    assert message.id is not None
    assert message.is_handled is False
    assert message.created_at is not None
    assert message.company is None


def test_contact_message_requires_a_message(db):
    """The database refuses an incomplete row even if the form is bypassed."""
    db.session.add(ContactMessage(name="No Message", email="x@example.com", subject="Hi"))

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


def test_seed_products_creates_rows(db):
    created = seed_products_table()
    assert created == len(get_products())
    assert db.session.query(Product).count() == len(get_products())


def test_seed_products_is_safe_to_run_twice(db):
    """Running the seed command again must update, not duplicate."""
    seed_products_table()
    second_run = seed_products_table()

    assert second_run == 0
    assert db.session.query(Product).count() == len(get_products())


def test_product_slugs_are_unique():
    slugs = [product.slug for product in get_products()]
    assert len(slugs) == len(set(slugs))


def test_get_product_returns_none_for_unknown_slug():
    assert get_product("nope") is None


def test_every_product_has_the_content_the_pages_need():
    """Guards against a half-filled catalogue entry breaking a page."""
    for product in get_products():
        assert product.name and product.slug and product.tagline
        assert product.audience and product.card_summary and product.intro
        assert product.problems, f"{product.slug} has no problem statements"
        assert product.confirmed, f"{product.slug} has no confirmed capabilities"
        assert product.why_choose, f"{product.slug} has no benefits"


def test_proposed_items_are_explicitly_labelled():
    """Anything not yet built must be marked, so the site never overpromises."""
    for product in get_products():
        for item in product.proposed:
            assert item.startswith(("PROPOSED", "PLACEHOLDER")), (
                f"{product.slug} has an unlabelled proposed item: {item!r}"
            )
