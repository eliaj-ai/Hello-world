"""Product pages: the overview grid and one page per product."""

from flask import Blueprint, abort, render_template

from app.services.catalog import get_product, get_products
from app.utils.seo import page_title

# `url_prefix` puts every route in this file under /products.
products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("/")
def index():
    return render_template(
        "pages/products.html",
        title=page_title("Products"),
        meta_description=(
            "Our SaaS products: Via Ciao for travel agencies, Hotel App for "
            "hotels, Scan Fox for cheap flight deals, and LocalGuide4me for "
            "finding local guides."
        ),
        products=get_products(),
    )


@products_bp.route("/<slug>")
def detail(slug):
    product = get_product(slug)
    if product is None:
        # An unknown slug is a genuine 404 rather than an error, so the
        # visitor sees the friendly not-found page.
        abort(404)

    others = [item for item in get_products() if item.slug != slug]

    return render_template(
        "pages/product_detail.html",
        title=page_title(product.name),
        meta_description=product.meta_description or product.tagline,
        product=product,
        other_products=others,
    )
