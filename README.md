# SaaS AI Solutions — Company Website

A professional company website and web application for **SaaS AI Solutions**, a
company that builds specialised web applications and sells them as SaaS products.

Built with **Python + Flask** on the back end and hand-written **HTML5, CSS3 and
JavaScript** on the front end. No CSS framework and no front-end build step, so
the site loads fast and the code stays easy to follow.

---

## Table of contents

1. [What this project is](#1-what-this-project-is)
2. [Features](#2-features)
3. [Technology stack](#3-technology-stack)
4. [Project structure](#4-project-structure)
5. [Installation — step by step](#5-installation--step-by-step)
6. [Running the website](#6-running-the-website)
7. [Running the tests](#7-running-the-tests)
8. [Environment variables](#8-environment-variables)
9. [Database](#9-database)
10. [How the code fits together](#10-how-the-code-fits-together-a-simple-explanation)
11. [Security](#11-security)
12. [Content honesty rules](#12-content-honesty-rules)
13. [Production deployment](#13-production-deployment)
14. [What is not built yet](#14-what-is-not-built-yet)

---

## 1. What this project is

The website presents the company and its four SaaS products, and lets visitors
get in touch through a working contact form. Every message is validated and
stored in a database.

The four products:

| Product | Built for | What it does |
|---|---|---|
| **Via Ciao** | Travel agencies | A web application helping agencies give their customers better digital services |
| **Hotel App** | Hotels | Digital services for hotel guests, through the browser |
| **Scan Fox** | Travellers, travel businesses | Scans for very cheap flights, identifies deals, shares them on social media such as TikTok |
| **LocalGuide4me** | Travellers and tourists | Finds local guides, searchable by city |

---

## 2. Features

**Website**
- Responsive design: desktop, laptop, tablet and mobile
- Working mobile navigation menu
- Homepage with hero, product showcase, "why us" and "how it works" sections
- A dedicated page for each of the four products
- About page
- Friendly 404, 500 and 429 error pages

**Contact system**
- Name, email, company, subject and message fields
- Validation in the browser *and* on the server
- CSRF protection on every submission
- Hidden honeypot field that traps spam bots
- Rate limiting: 5 submissions per IP address per 10 minutes
- Messages saved to the database
- Email notification support, switched off until you configure it

**Technical**
- Flask application factory + blueprints
- SQLAlchemy models, SQLite locally and PostgreSQL-ready
- 37 automated tests
- Security headers including a strict Content-Security-Policy
- SEO: meta descriptions, Open Graph tags, canonical URLs, `sitemap.xml`, `robots.txt`, favicon

---

## 3. Technology stack

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.9+ | Required for the project |
| Web framework | Flask 3 | Small, clear, and easy to learn |
| Database toolkit | SQLAlchemy 2 via Flask-SQLAlchemy | Writes SQL for you and blocks SQL injection |
| Database | SQLite (dev), PostgreSQL (production) | SQLite needs zero setup; the switch is one setting |
| Forms | Flask-WTF + WTForms | Validation and CSRF protection together |
| Configuration | python-dotenv | Keeps secrets out of the source code |
| Testing | pytest | The standard choice for Python |
| Front end | Hand-written HTML/CSS/JS | No build step, nothing to download from a CDN |

**Deliberately not used:** React, Tailwind, Bootstrap, jQuery. The site is mostly
content, so a framework would add weight and complexity without helping.

---

## 4. Project structure

```text
Hello-world/
│
├── app/                        The application itself
│   ├── __init__.py             create_app(): builds and configures the app
│   ├── extensions.py           Shared database and CSRF objects
│   │
│   ├── routes/                 What happens at each URL
│   │   ├── main.py             Homepage, about, robots.txt, sitemap.xml
│   │   ├── products.py         /products and /products/<name>
│   │   └── contact.py          The contact form
│   │
│   ├── models/                 Database tables
│   │   ├── contact_message.py  One row per contact form submission
│   │   └── product.py          Product table (for a future admin panel)
│   │
│   ├── forms/
│   │   └── contact.py          Contact form fields and validation rules
│   │
│   ├── services/               Logic that is not a route or a model
│   │   ├── catalog.py          All product content lives here
│   │   └── mail.py             Email sending (off until configured)
│   │
│   ├── utils/
│   │   └── seo.py              Page titles and absolute URLs
│   │
│   ├── templates/              HTML
│   │   ├── base.html           The shell every page shares
│   │   ├── partials/           Nav, footer, icons, product card
│   │   ├── pages/              Home, products, about, contact
│   │   ├── errors/             404, 500, 429
│   │   └── seo/sitemap.xml
│   │
│   └── static/
│       ├── css/                base.css, components.css, pages.css
│       ├── js/main.js          Mobile menu + form validation
│       └── images/             Favicon and social preview image
│
├── tests/                      37 automated tests
├── instance/                   The SQLite database (never committed)
├── venv/                       Installed packages (never committed)
│
├── config.py                   All settings, read from the environment
├── run.py                      Starts the development server
├── requirements.txt            The list of packages to install
├── .env.example                Template for your own .env file
├── .gitignore
└── README.md
```

---

## 5. Installation — step by step

You need **Python 3.9 or newer**. Check with `python3 --version`.

**Step 1 — go to the project folder**

```bash
cd /Users/rashajahshan/Hello-world
```

**Step 2 — create a virtual environment**

```bash
python3 -m venv venv
```

A *virtual environment* is a private folder holding this project's packages, so
they cannot clash with other projects or with your system Python. It creates a
folder called `venv`. To undo everything, delete that folder.

**Step 3 — activate it**

```bash
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows
```

Your prompt now starts with `(venv)`. That means `python` and `pip` refer to the
project's private copies. Type `deactivate` to leave.

**Step 4 — install the packages**

```bash
pip install -r requirements.txt
```

**Step 5 — create your settings file**

```bash
cp .env.example .env
```

Then open `.env` and set a real `SECRET_KEY`. Generate one with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the output into the `SECRET_KEY=` line. **Never commit `.env`** — it is
already in `.gitignore`.

---

## 6. Running the website

```bash
python run.py
```

Open **http://127.0.0.1:5000** in your browser. Press `Ctrl + C` to stop.

`127.0.0.1` means "this computer only" — nobody else can reach it.

The database file is created automatically the first time you start the site.

---

## 7. Running the tests

```bash
pytest              # run everything
pytest -v           # show each test name
pytest tests/test_contact.py    # just the contact form tests
```

You should see `37 passed`. The tests use a temporary in-memory database, so
they never touch your real data.

**What they check:** every page loads; every product page exists; the contact
form saves valid messages and rejects invalid ones; the honeypot silently
discards spam; rate limiting works; submitted HTML is escaped rather than
executed; security headers are present; and no product page presents a proposed
idea as though it were already built.

---

## 8. Environment variables

All settings live in `.env`. See `.env.example` for the full list.

| Variable | Meaning |
|---|---|
| `FLASK_ENV` | `development`, `testing` or `production` |
| `SECRET_KEY` | Signs session cookies and CSRF tokens. Long and random. **Required in production.** |
| `DATABASE_URL` | Leave empty for SQLite; set a PostgreSQL URL in production |
| `SITE_URL` | The public address, used by `sitemap.xml` and social preview tags |
| `MAIL_ENABLED` | `false` by default — no email is sent |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD` | Your email provider's settings |
| `MAIL_DEFAULT_SENDER` | The address notifications are sent from |
| `CONTACT_RECIPIENT` | The address that receives contact enquiries |

**Email is switched off.** Contact messages are stored in the database only. To
turn sending on, fill in the mail settings and set `MAIL_ENABLED=true`. Nothing
in the code needs changing.

---

## 9. Database

Two tables:

**`contact_messages`** — one row per form submission: name, email, company,
subject, message, IP address, user agent, `is_handled` flag, and timestamp.

**`products`** — mirrors the product catalogue. The website reads its content
from `app/services/catalog.py`, not from this table; the table exists so a
future admin dashboard can edit products without a code change.

Useful commands:

```bash
flask --app run.py init-db          # create the tables
flask --app run.py seed-products    # copy the catalogue into the products table
```

**Switching to PostgreSQL** — set one variable and install one driver:

```bash
pip install "psycopg[binary]"
# in .env:
DATABASE_URL=postgresql+psycopg://user:password@host:5432/dbname
```

No application code changes.

> **Note on schema changes.** `db.create_all()` creates missing tables but does
> not alter existing ones. Before changing a model in production, add
> **Flask-Migrate** (`pip install Flask-Migrate`), which handles safe schema
> updates.

---

## 10. How the code fits together — a simple explanation

When somebody visits a page, five things happen in order:

1. **`run.py`** starts the server and calls `create_app()`.
2. **`app/__init__.py`** builds the application: loads settings, connects the
   database, attaches the routes and adds security headers.
3. **A route** in `app/routes/` matches the URL. Visiting `/products/scan-fox`
   runs the `detail()` function in `products.py`.
4. **The route fetches its data** — for products, from `app/services/catalog.py`.
5. **A template** in `app/templates/` turns that data into HTML and sends it back.

Two ideas worth knowing:

**Blueprints** group related URLs into their own file. All product URLs live in
`products.py`, all contact URLs in `contact.py`. Without them, everything would
pile into one enormous file.

**Template inheritance** means `base.html` holds the parts every page shares —
the head, navigation and footer — and each page fills in just its own content.
Change the navigation once, and it changes everywhere.

---

## 11. Security

| Protection | How |
|---|---|
| CSRF | Flask-WTF token on every form. A submission without it is rejected with HTTP 400 — verified by a test. |
| SQL injection | SQLAlchemy sends values separately from the query. No string-built SQL anywhere. |
| XSS | Jinja2 escapes all output by default, so submitted HTML is displayed as text, never executed. |
| Input validation | Every field has length and format rules, checked on the server. The browser check is convenience only. |
| Secure sessions | Cookies are `HttpOnly` and `SameSite=Lax`; `Secure` is added in production. |
| Secrets | Read from the environment. No key, password or connection string is in the source code. |
| Security headers | `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`, plus HSTS in production. |
| Spam | Hidden honeypot field plus per-IP rate limiting. |
| Error handling | Custom error pages; internal details are logged, never shown to visitors. |
| Production safety | The app refuses to start in production without a real `SECRET_KEY`. |

**Two limits to be aware of:**

- **Rate limiting is per process.** It keeps its counter in memory, so running
  several server processes gives each its own count. For serious traffic, use
  **Flask-Limiter** with Redis.
- **`X-Forwarded-For` is trusted.** Behind a proxy this is correct; exposed
  directly to the internet, a visitor could spoof their IP and dodge the rate
  limit. Only run this behind a proxy you control, and add Werkzeug's
  `ProxyFix` middleware.

---

## 12. Content honesty rules

Everything written on this site follows one rule: **nothing is invented.**

- No fake customers, reviews, statistics, awards, partnerships or team members.
- No unsupported claims such as "99.99% uptime".
- Company details we do not have — founding year, address, team size, legal
  entity — appear as visible **"To be added"** placeholders.
- Every product page splits its capabilities into **Confirmed** (what the
  company has actually stated) and **Proposed — not built yet** (clearly marked
  as not available and not a commitment).

This is enforced by tests, not just good intentions: `test_models.py` fails the
build if any proposed item is not explicitly labelled, and `test_pages.py`
fails if a product page stops showing the confirmed/proposed split.

**To edit product content**, open `app/services/catalog.py`. All four products
are defined there in one place.

---

## 13. Production deployment

**1. Never use the development server.** `python run.py` is for local use only.
Use a WSGI server:

```bash
pip install gunicorn
gunicorn "run:app" --bind 0.0.0.0:8000 --workers 4
```

**2. Set the environment properly:**

```bash
FLASK_ENV=production
SECRET_KEY=<a long random value, different from development>
DATABASE_URL=postgresql+psycopg://...
SITE_URL=https://your-real-domain.com
```

**3. Checklist before going live:**

- [ ] HTTPS enabled (the app assumes it — secure cookies and HSTS depend on it)
- [ ] A real `SECRET_KEY` set, never reused from development
- [ ] PostgreSQL instead of SQLite, with backups
- [ ] Nginx or similar in front, serving `app/static/` directly
- [ ] `ProxyFix` middleware added so client IPs are correct
- [ ] Flask-Migrate added before any model changes
- [ ] Flask-Limiter with Redis if traffic is significant
- [ ] Logging and error monitoring configured
- [ ] `SITE_URL` set to the real domain, so `sitemap.xml` is correct
- [ ] `sitemap.xml` submitted to Google Search Console
- [ ] A retention policy for the IP addresses stored with contact messages
      (this is personal data under GDPR)

---

## 14. What is not built yet

Deliberately left out, to keep the first version solid:

- **User accounts and login.** Not built, by choice. The structure supports
  adding it later.
- **Admin dashboard.** Not built. The `products` table and the `is_handled`
  flag on messages exist so it can be added without redesigning anything.
- **Email sending.** The code is written and tested but stays switched off
  until real mail settings are supplied.
- **Real company details.** Placeholders until you provide them.
- **Actual product features.** This site describes the products; the products
  themselves are separate applications.

---

## Quick reference

```bash
source venv/bin/activate      # start working
python run.py                 # run the site  -> http://127.0.0.1:5000
pytest                        # run the tests
deactivate                    # stop working
```
