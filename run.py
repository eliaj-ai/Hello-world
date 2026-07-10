"""Entry point for local development.

Start the site with:

    python run.py

Then open http://127.0.0.1:5000 in your browser.

In production this file is not used directly; a WSGI server such as Gunicorn
imports the `app` object instead (see the README).
"""

import os

from app import create_app

app = create_app(os.environ.get("FLASK_ENV", "development"))


if __name__ == "__main__":
    # host="127.0.0.1" means the server is reachable only from this computer,
    # which is the safe default while developing.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))
