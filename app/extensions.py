"""Shared extension objects.

These are created here, without an application attached, and connected to the
app inside `create_app()`. Keeping them in their own module avoids circular
imports between the app factory and the model files.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# The database handle used by every model.
db = SQLAlchemy()

# Cross-Site Request Forgery protection for every form submission.
csrf = CSRFProtect()
