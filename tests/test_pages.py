"""Tests for the public pages: they load, and they say the right things."""

import pytest

from app.services.catalog import get_products


def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"SaaS AI Solutions" in response.data
    assert b"Powering the next generation" in response.data


def test_homepage_lists_every_product(client):
    response = client.get("/")
    body = response.get_data(as_text=True)
    for product in get_products():
        assert product.name in body


def test_products_index_loads(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert b"Products" in response.data


@pytest.mark.parametrize("product", get_products(), ids=lambda p: p.slug)
def test_each_product_page_loads(client, product):
    """Every product in the catalogue must have a working page."""
    response = client.get(f"/products/{product.slug}")
    assert response.status_code == 200

    body = response.get_data(as_text=True)
    assert product.name in body
    assert product.audience in body


@pytest.mark.parametrize("product", get_products(), ids=lambda p: p.slug)
def test_product_page_separates_confirmed_from_proposed(client, product):
    """The honesty rule, enforced by a test.

    Proposed ideas must always be visibly labelled, so nothing on the site
    reads as a promise the company has not made.
    """
    body = client.get(f"/products/{product.slug}").get_data(as_text=True)
    assert "Confirmed" in body
    assert "Proposed - not built yet" in body
    assert "not</strong> available" in body


def test_unknown_product_returns_404(client):
    response = client.get("/products/does-not-exist")
    assert response.status_code == 404
    assert b"We couldn&#39;t find that page" in response.data or b"404" in response.data


def test_about_page_loads(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data


def test_about_page_uses_placeholders_not_invented_facts(client):
    """Company facts we were never given must stay marked as placeholders."""
    body = client.get("/about").get_data(as_text=True)
    assert "To be added" in body


def test_404_page_for_unknown_url(client):
    assert client.get("/no-such-page").status_code == 404


def test_security_headers_are_present(client):
    headers = client.get("/").headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in headers
    assert "Referrer-Policy" in headers
