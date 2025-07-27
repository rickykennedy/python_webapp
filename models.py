from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the database extension object.
# This object doesn't have an application associated with it yet.
db = SQLAlchemy()

class ContactMessage(db.Model):
    """Model for storing contact messages."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """
        String representation of the ContactMessage model.
        """
        return f'<ContactMessage {self.name} - {self.subject}>'


class Quote(db.Model):
    """
    Model for storing quotes.
    """
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """
        String representation of the Quote model.
        """
        return f'<Quote {self.quote} by {self.author}>'


class User(db.Model, UserMixin):
    """
    User model for the database.
    Inherits from db.Model for SQLAlchemy and UserMixin for Flask-Login.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """String representation of the User object."""
        return f'<User {self.username}>'
