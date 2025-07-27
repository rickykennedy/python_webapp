# Import the db instance from the application package's __init__.py
from .. import db

class ContactMessage(db.Model):
    """Model for storing contact messages."""
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """String representation of the ContactMessage model."""
        return f'<ContactMessage {self.name} - {self.subject}>'
