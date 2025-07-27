# This file is dedicated to initializing Flask extensions.
# By keeping them here, we avoid circular import errors.

# --- Extensions Initialization ---
# Create extension instances without an app.
# They will be initialized with the app in the factory.
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
