"""Helpers for search-engine and social-media metadata."""

from flask import current_app, request


def absolute_url(path=""):
    """Turn a site path into a full https:// URL.

    Open Graph tags (the preview cards shown when a link is pasted into a
    chat or social network) require absolute URLs, not relative ones.
    """
    base = (current_app.config.get("SITE_URL") or request.url_root).rstrip("/")
    if not path:
        return base
    return f"{base}/{path.lstrip('/')}"


def page_title(title=None):
    """Build the text shown in the browser tab.

    Keeps every page consistent: "Page name | SaaS AI Solutions".
    """
    company = current_app.config.get("COMPANY_NAME", "SaaS AI Solutions")
    if not title:
        return company
    return f"{title} | {company}"
