import os
import logging
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager

# Import the configuration from config.py
from config import Config
# Import the database object and models from models.py
from models import db, User, Quote

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO)

# --- Extensions Initialization (outside of factory) ---
# These are created here but not configured until the app is created.
mail = Mail()
login_manager = LoginManager()
# When a user needs to log in, they are redirected to the login view.
# The 'main.' prefix refers to the blueprint's name.
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

# --- Application Factory ---
def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    This pattern is useful for creating multiple app instances for testing
    or different configurations.
    """
    app = Flask(__name__)
    # Load configuration from the Config object
    app.config.from_object(config_class)

    # --- Initialize Extensions with App ---
    # The extensions are now bound to the specific app instance.
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # --- Register Blueprints ---
    # Import and register the blueprint from routes.py.
    # The import is done here to avoid circular dependencies.
    from routes import main_routes
    app.register_blueprint(main_routes)

    # --- Flask-Login User Loader ---
    # This callback is used to reload the user object from the user ID stored in the session.
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Create Database Tables and Initial Data ---
    # The app_context is needed for SQLAlchemy to know which app instance it's working with.
    with app.app_context():
        # Create database tables for all models
        db.create_all()
        # Populate the database with initial data if it's empty
        create_initial_data()

    return app

def create_initial_data():
    """Creates initial data for the database if it's empty."""
    # Check if we have any quotes, if not, add them.
    if not Quote.query.first():
        initial_quotes = [
            {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
            {"quote": "Leadership and learning are indispensable to each other.", "author": "John F. Kennedy"},
            {"quote": "A leader is one who knows the way, goes the way, and shows the way.", "author": "John C. Maxwell"},
            {"quote": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
            {"quote": "To handle yourself, use your head; to handle others, use your heart.", "author": "Eleanor Roosevelt"}
        ]
        for item in initial_quotes:
            db.session.add(Quote(quote=item['quote'], author=item['author']))
        db.session.commit()
        logging.info("Initial quotes added to the database.")

# --- Main Execution Block ---
# This block runs only when the script is executed directly.
if __name__ == '__main__':
    # Create the Flask app instance using the factory
    app = create_app()
    # Run the development server
    app.run(debug=True)
