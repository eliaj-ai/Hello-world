"""The product catalogue - the single source of truth for product content.

WHY THIS IS A PYTHON FILE AND NOT THE DATABASE
----------------------------------------------
Marketing copy is reviewed like code: it goes through Git, so every wording
change has an author and a history. The `Product` database table mirrors this
catalogue (run `flask seed-products`) so an admin dashboard can take over
later without the website having to change.

HONESTY RULES USED HERE
-----------------------
Every product below separates two kinds of statement:

  * `confirmed`  - functionality the company has actually described.
  * `proposed`   - ideas that are NOT built or promised yet. The templates
                   always label these clearly as proposed.

Nothing in this file invents customers, statistics, awards or partnerships.
Where information is genuinely missing, a `PLACEHOLDER` marker is used so it
is obvious what still needs to be filled in.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class Product:
    """One SaaS product.

    `frozen=True` makes instances read-only, so a bug in a template can never
    silently rewrite the catalogue.
    """

    slug: str
    name: str
    tagline: str
    audience: str
    card_summary: str          # short text for the homepage card
    intro: str                 # opening paragraph on the product page
    status: str                # honest development status
    accent: str                # CSS colour token used for this product
    icon: str                  # key into the icon set in partials/icons.html
    problems: List[str] = field(default_factory=list)
    confirmed: List[str] = field(default_factory=list)
    proposed: List[str] = field(default_factory=list)
    why_choose: List[str] = field(default_factory=list)
    cta_label: str = "Talk to us about this product"
    meta_description: Optional[str] = None


PRODUCTS: List[Product] = [
    Product(
        slug="via-ciao",
        name="Via Ciao",
        tagline="A web application built for travel agencies.",
        audience="Travel agencies",
        card_summary=(
            "A SaaS platform for travel agencies that want to offer their "
            "customers a stronger digital experience."
        ),
        intro=(
            "Via Ciao is a web application designed specifically for travel "
            "agencies. Its purpose is to help agencies deliver better digital "
            "services to the travellers they look after, without every agency "
            "needing to build and maintain software of its own."
        ),
        status="In development",
        accent="ocean",
        icon="compass",
        problems=[
            "Many travel agencies still coordinate bookings and customer "
            "questions across email, phone calls and spreadsheets.",
            "Building custom software in-house is expensive, and it needs "
            "ongoing maintenance long after launch.",
            "Travellers increasingly expect the same self-service digital "
            "experience from an agency that they get from a large platform.",
        ],
        confirmed=[
            "A web application built for the travel agency market.",
            "Delivered as software-as-a-service, so agencies use it through "
            "the browser with no installation.",
            "Focused on helping agencies improve the digital service they "
            "give their own customers.",
        ],
        proposed=[
            "PLACEHOLDER - the detailed feature list for Via Ciao has not "
            "been finalised yet. Specific capabilities will be published "
            "here once they are confirmed.",
        ],
        why_choose=[
            "Purpose-built for travel agencies rather than adapted from a "
            "generic tool.",
            "No infrastructure to run: updates and hosting are handled for you.",
            "Priced and shaped as SaaS, so it grows with the agency.",
        ],
        cta_label="Request a Via Ciao walkthrough",
        meta_description=(
            "Via Ciao is a SaaS web application for travel agencies, built to "
            "help them deliver better digital services to their customers."
        ),
    ),
    Product(
        slug="hotel-app",
        name="Hotel App",
        tagline="Digital services for hotel guests, delivered through the browser.",
        audience="Hotels",
        card_summary=(
            "A web application hotels can offer their guests, providing "
            "useful digital services during the stay."
        ),
        intro=(
            "Hotel App is a web application for hotels. It gives a hotel a "
            "digital channel to its guests, so useful services can be offered "
            "online instead of only at the front desk."
        ),
        status="In development",
        accent="violet",
        icon="building",
        problems=[
            "Guest requests concentrate at the reception desk, which creates "
            "queues at busy times.",
            "Information a guest needs - opening times, directions, house "
            "rules - is often spread across printed material that goes out of "
            "date.",
            "Smaller hotels rarely have the budget to commission their own "
            "guest application.",
        ],
        confirmed=[
            "A web application aimed at hotels.",
            "Provides digital services to the hotel's guests.",
            "Delivered as SaaS, so a hotel does not run its own servers.",
        ],
        proposed=[
            "PROPOSED - the specific guest-facing features have not been "
            "decided yet. They will be listed here once confirmed, rather "
            "than advertised in advance.",
        ],
        why_choose=[
            "Guests reach services from their own phone, with nothing to install.",
            "One product serving many hotels means improvements reach "
            "everyone, not just one property.",
            "Reduces routine questions arriving at reception.",
        ],
        cta_label="Discuss Hotel App for your property",
        meta_description=(
            "Hotel App is a SaaS web application that lets hotels offer "
            "digital services to their guests through the browser."
        ),
    ),
    Product(
        slug="scan-fox",
        name="Scan Fox",
        tagline="Find cheap flights. Discover deals. Share them.",
        audience="Travellers, and travel-related businesses",
        card_summary=(
            "Scans for very cheap flights, identifies the deals worth "
            "sharing, and turns them into social media content."
        ),
        intro=(
            "Scan Fox searches for very cheap flights and identifies deals "
            "that are worth passing on. Those deals can then be shared to "
            "social media platforms such as TikTok, turning flight-price "
            "research into content an audience actually wants."
        ),
        status="In development",
        accent="amber",
        icon="radar",
        problems=[
            "Genuinely cheap fares appear and disappear quickly, so they are "
            "easy to miss.",
            "Checking many routes and dates by hand takes a great deal of time.",
            "Travel accounts on social media need a steady supply of deals to "
            "post, and finding them manually does not scale.",
        ],
        confirmed=[
            "Searches for very cheap flights.",
            "Identifies flight deals from what it finds.",
            "Deals can be shared to social media platforms such as TikTok.",
        ],
        proposed=[
            "PROPOSED - automated posting schedules, alert subscriptions and "
            "route-watching are natural next steps, but none of them are "
            "built yet.",
            "PROPOSED - a business tier for travel-related companies that "
            "want deals for their own audience.",
        ],
        why_choose=[
            "Deal discovery and content creation handled in one workflow.",
            "Built around how travel audiences on short-video platforms "
            "actually behave.",
            "Removes the manual searching that makes deal accounts hard to run.",
        ],
        cta_label="Get in touch about Scan Fox",
        meta_description=(
            "Scan Fox scans for very cheap flights, identifies deals, and "
            "helps share them on social media platforms such as TikTok."
        ),
    ),
    Product(
        slug="localguide4me",
        name="LocalGuide4me",
        tagline="Find a local guide in the city you are visiting.",
        audience="Travellers and tourists",
        card_summary=(
            "Connects travellers with local guides, searchable by city, for "
            "experiences led by people who live there."
        ),
        intro=(
            "LocalGuide4me helps travellers find local guides in a specific "
            "city. Instead of a generic tour, visitors can connect with "
            "someone who knows the place, and discover it through them."
        ),
        status="In development",
        accent="emerald",
        icon="map-pin",
        problems=[
            "Finding a trustworthy local guide in an unfamiliar city is hard "
            "and usually happens through scattered listings.",
            "Independent guides have few good ways to reach the travellers "
            "who are looking for exactly what they offer.",
            "Travellers who want something beyond the standard tourist route "
            "have little to go on.",
        ],
        confirmed=[
            "Helps travellers find local guides.",
            "Guides can be searched by city.",
            "Supports discovering local experiences.",
            "Connects travellers directly with guides.",
        ],
        proposed=[
            "PROPOSED - reviews, verification, messaging and booking flows "
            "are being considered but are not confirmed functionality.",
        ],
        why_choose=[
            "City-based search, so results are relevant to where you actually are.",
            "Puts travellers in touch with local people rather than a call centre.",
            "Gives independent guides a route to travellers looking for them.",
        ],
        cta_label="Ask about LocalGuide4me",
        meta_description=(
            "LocalGuide4me connects travellers with local guides, searchable "
            "by city, for experiences led by people who live there."
        ),
    ),
]

# Fast lookup by slug, built once when the module is imported.
_BY_SLUG = {product.slug: product for product in PRODUCTS}


def get_products():
    """Return every product, in display order."""
    return PRODUCTS


def get_product(slug):
    """Return one product by its slug, or None if there is no such product."""
    return _BY_SLUG.get(slug)


def seed_products_table():
    """Copy this catalogue into the `products` database table.

    Existing rows are updated rather than duplicated, so the command is safe
    to run more than once. Returns the number of new rows created.
    """
    from app.extensions import db
    from app.models import Product as ProductRow

    created = 0
    for order, item in enumerate(PRODUCTS):
        row = db.session.query(ProductRow).filter_by(slug=item.slug).one_or_none()
        if row is None:
            row = ProductRow(slug=item.slug)
            db.session.add(row)
            created += 1
        row.name = item.name
        row.tagline = item.tagline
        row.audience = item.audience
        row.summary = item.card_summary
        row.display_order = order
        row.is_published = True

    db.session.commit()
    return created
