"""General pages: homepage, about, and the search-engine files."""

from flask import Blueprint, Response, render_template, url_for

from app.services.catalog import get_products
from app.utils.seo import absolute_url, page_title

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template(
        "pages/home.html",
        title=page_title(),
        meta_description=(
            "SaaS AI Solutions builds specialised web applications, delivered "
            "as SaaS products, for travel agencies, hotels and travellers."
        ),
        products=get_products(),
    )


@main_bp.route("/about")
def about():
    return render_template(
        "pages/about.html",
        title=page_title("About"),
        meta_description=(
            "About SaaS AI Solutions: how we identify a real business problem, "
            "build a specialised web application, launch it and keep improving it."
        ),
    )


@main_bp.route("/robots.txt")
def robots():
    """Tells search engine crawlers what they may index."""
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {absolute_url(url_for('main.sitemap'))}",
        "",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


@main_bp.route("/sitemap.xml")
def sitemap():
    """Lists every public page so search engines can find them all."""
    pages = [
        {"loc": absolute_url(url_for("main.home")), "priority": "1.0"},
        {"loc": absolute_url(url_for("products.index")), "priority": "0.9"},
        {"loc": absolute_url(url_for("main.about")), "priority": "0.7"},
        {"loc": absolute_url(url_for("contact.contact")), "priority": "0.7"},
    ]
    pages += [
        {
            "loc": absolute_url(url_for("products.detail", slug=product.slug)),
            "priority": "0.8",
        }
        for product in get_products()
    ]

    xml = render_template("seo/sitemap.xml", pages=pages)
    return Response(xml, mimetype="application/xml")
