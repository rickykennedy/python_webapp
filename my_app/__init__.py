import os
import logging
from flask import Flask

# Import the configuration from the root config.py
from config import Config
# Import extensions from the new extensions.py file
from .extensions import db, mail, login_manager
# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO)

# When a user needs to log in, they are redirected to the login view.
# The 'main.' prefix refers to the blueprint's name.
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


# --- Application Factory ---
def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    This pattern is useful for creating multiple app instances for testing
    or different configurations.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from the Config object
    app.config.from_object(config_class)

    # --- Initialize Extensions with App ---
    # The extensions are now bound to the specific app instance.
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # The 'with app.app_context()' is crucial. It makes the application
    # context available for the imports and database operations that follow.
    # This resolves runtime errors if blueprints or models attempt to
    # access the app or its extensions when they are imported.
    with app.app_context():

        # Import models here to ensure they are registered with SQLAlchemy
        from .models import User, ContactMessage, Quote

        # Import blueprints and models inside the context to ensure
        # they have access to the configured application.
        # Import and register the blueprints
        from .main.routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .auth.routes import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .quotes.routes import quotes as quotes_blueprint
        app.register_blueprint(quotes_blueprint)


        # The user loader needs to be defined within the context
        # to be correctly associated with the login_manager instance.
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Create database tables for all models
        db.create_all()
        # Populate the database with initial data if it's empty
        create_initial_data()

    return app

def create_initial_data():
    """Creates initial data for the database if it's empty."""
    from .models import Quote
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
