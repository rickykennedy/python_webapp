import os

class Config:
    """
    Configuration class for the Flask application.

    Loads configuration settings from environment variables with sensible defaults
    for a development environment.
    """
    # Secret key for session management and flashing messages.
    # It's crucial to use a strong, random key in production.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key_for_dev')

    # Flask-Mail configuration settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 't')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # The default sender is typically the same as the mail username.
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # Flask-SQLAlchemy configuration
    # The database URI is fetched from the DATABASE_URL environment variable.
    # Format for PostgreSQL: postgresql+psycopg2://user:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db')

    # Suppress SQLAlchemy's track modification warnings to save memory.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
