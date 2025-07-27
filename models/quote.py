#
# class Quote(db.Model):
#     """
#     Model for storing quotes.
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     quote = db.Column(db.String(255), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#
#     def __repr__(self):
#         """
#         String representation of the Quote model.
#         Returns a string that includes the quote and the author.
#         """
#         return f'<Quote {self.quote} by {self.author}>'
