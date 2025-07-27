# This file makes the 'models' directory a Python package.
# It also conveniently gathers all model classes to one place
# so they can be imported easily from other parts of the application.

from .contact_message import ContactMessage
from .quote import Quote
from .user import User

# You can also define a __all__ variable to specify what gets imported
# when a client uses 'from .models import *'
__all__ = ['ContactMessage', 'Quote', 'User']
