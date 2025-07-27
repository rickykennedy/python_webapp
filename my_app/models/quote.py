# Import the db instance from the application package's __init__.py
from .. import db

class Quote(db.Model):
    """Model for storing quotes."""
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """String representation of the Quote model."""
        return f'<Quote {self.quote} by {self.author}>'
