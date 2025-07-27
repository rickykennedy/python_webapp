# import os
# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mail import Mail, Message
# from flask_sqlalchemy import SQLAlchemy
# from config import Config  # Assuming you have a config.py file with your configuration settings
# from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy import or_  # Import or_ for combining query conditions
# # from sqlalchemy import create_engine, Column, Integer, String
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker
#
# import logging
#
# logging.basicConfig(level=logging.INFO)
# logging.info("Initial quotes added to the database")
# # initialize the Flask application
# app = Flask(__name__)
#
# # --- Flask Configuration for Secret Key and Mail ---
# # A secret key is required for flashing messages and session management.
# # In a real application, use a strong, randomly generated key stored securely.
# # TODO: Configure the secret key properly for mailing purposes.
# # app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key_for_dev')
# #
# # # Flask-Mail configuration from environment variables
# # app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
# # app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
# # app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
# # app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 't')
# # app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# # app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# # app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME') # Default sender is usually the MAIL_USERNAME
# app.config.from_object(Config)
#
# # Initialize Flask-Mail
# mail = Mail(app)
#
# print(app.config)
# # Format: postgresql+psycopg2://user:password@host:port/database
# # engine = create_engine("portostgresql+psycopg2://postgres:floricky@localhost:5432/postgres")
# # Base = declarative_base()
# # Flask-SQLAlchemy configuration
# # The database URI is fetched from the DATABASE_URL environment variable
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# # app.config['SQLALCHEMY_DATABASE_URI'] = "jdbc:postgresql://postgres:floricky@localhost:5432/postgres"
# # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
# #     'DATABASE_URL',
# #     'postgresql+psycopg2://postgres:floricky@localhost:5432/postgres'
# # )
# # Suppress SQLAlchemy's track modification warnings, as it consumes extra memory
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
#
# # --- Database Model (if needed) ---
# # Example model for storing contact messages (if you want to save them in a database)
# class ContactMessage(db.Model):
#     """Model for storing contact messages.
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     subject = db.Column(db.String(200), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#
#     def __repr__(self):
#         """
#         String representation of the ContactMessage model.
#         Returns a string that includes the name and subject of the message.
#         """
#         return f'<ContactMessage {self.name} - {self.subject}>'
#
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
#
#
# class User(db.Model, UserMixin):
#     """
#     User model for the database.
#     Inherits from db.Model for SQLAlchemy and UserMixin for Flask-Login.
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(256), unique=True, nullable=False)
#     email = db.Column(db.String(256), unique=True, nullable=False)
#     password_hash = db.Column(db.String(256), nullable=False)
#
#     def set_password(self, password):
#         """Hashes the password and stores it."""
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         """Checks if the provided password matches the stored hash."""
#         return check_password_hash(self.password_hash, password)
#
#     def __repr__(self):
#         """String representation of the User object."""
#         return f'<User {self.username}>'
#
#
# # --- Flask Routes ---
# @app.route('/')
# def index():
#     return render_template('index.html', title='Home')
#
#
# @app.route('/about')
# def about():
#     """
#     Renders the about page of the website.
#     """
#     return render_template('about.html', title='About Us')
#
#
# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     """
#     Renders the contact page of the website.
#     """
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         subject = request.form.get('subject')
#         message_body = request.form.get('message')
#
#         # Basic validation
#         if not name or not email or not subject or not message_body:
#             flash('All fields are required!', 'error')  # 'error' is a category for styling
#             return render_template('contact.html', title='Contact Us',
#                                    name=name, email=email, subject=subject, message_body=message_body)
#
#         try:
#             # Create the email message
#             msg = Message(
#                 subject=f"Contact Form: {subject}",
#                 sender=app.config['MAIL_DEFAULT_SENDER'],  # Your configured sender email
#                 recipients=[app.config['MAIL_USERNAME']]  # Send to your own email address
#             )
#             # Add HTML content for better formatting in email clients
#             msg.html = render_template('email_template.html',
#                                        name=name, email=email, subject=subject, message_body=message_body)
#
#             mail.send(msg)
#             flash('Your message has been sent successfully!', 'success')  # 'success' category
#             return redirect(url_for('contact'))  # Redirect to clear the form after successful submission
#         except Exception as e:
#             flash(f'Failed to send message. Please try again later. Error: {e}', 'error')
#             # Stay on the contact page with pre-filled form in case of error
#             return render_template('contact.html', title='Contact Us',
#                                    name=name, email=email, subject=subject, message_body=message_body)
#
#     # If GET request, render the contact form
#     return render_template('contact.html', title='Contact Us')
#
#
# # Initialize Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)
# # Set the login view for Flask-Login (where to redirect unauthenticated users)
# login_manager.login_view = 'login'
# # Set the message category for login required messages
# login_manager.login_message_category = 'info'
#
#
# ### Login management section
# # This section handles user login management.
#
# # --- Flask-Login User Loader ---
# @login_manager.user_loader
# def load_user(user_id):
#     """
#     Required by Flask-Login to reload the user object from the user ID stored in the session.
#     """
#     return User.query.get(int(user_id))
#
#
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     """
#     Signup route.
#     GET: Displays the signup form.
#     POST: Processes the signup form submission.
#     """
#     # If user is already logged in, redirect to dashboard
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))
#
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         email = request.form.get('email')
#
#         # Basic validation
#         if not username or not password or not email:
#             flash('Username, email and password are required!', 'danger')
#             return render_template('signup.html')
#
#         # Check if username already exists
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             flash('Username already exists. Please choose a different one.', 'warning')
#             return render_template('signup.html')
#
#         # Validate email format (basic validation)
#         if '@' not in email or '.' not in email.split('@')[-1]:
#             flash('Invalid email format. Please enter a valid email address.', 'danger')
#             return render_template('signup.html')
#
#         # Check if email already exists
#         existing_email = User.query.filter_by(email=email).first()
#         if existing_email:
#             flash('Email already exists. Please use a different email.', 'warning')
#             return render_template('signup.html')
#
#         # Create new user
#         new_user = User(username=username, email=email)
#         new_user.set_password(password)  # Hash the password
#         db.session.add(new_user)
#         db.session.commit()
#
#         flash('Account created successfully! Please log in.', 'success')
#         return redirect(url_for('login'))
#
#     return render_template('signup.html')
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """
#     Login route.
#     GET: Displays the login form.
#     POST: Processes the login form submission.
#     """
#     # If user is already logged in, redirect to dashboard
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))
#
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         # Find user by username
#         # user = User.query.filter_by(username=username).first()
#         user = User.query.filter(
#             or_(User.username == username, User.email == username)
#         ).first()
#
#         # If user is not found, user will be None
#         # if not user:
#         #     user = User.query.filter_by(email=username).first()  # Check by email if username not found
#
#         # Check if user exists and password is correct
#         if user and user.check_password(password):
#             login_user(user)  # Log in the user
#             flash('Logged in successfully!', 'success')
#             # Redirect to the page user was trying to access, or dashboard
#             next_page = request.args.get('next')
#             return redirect(next_page or url_for('dashboard'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#
#     return render_template('login.html')
#
#
# @app.route('/logout')
# @login_required  # Ensures only logged-in users can access this route
# def logout():
#     """
#     Logout route. Logs out the current user.
#     """
#     logout_user()
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('login'))
#
#
# @app.route('/dashboard')
# @login_required  # Ensures only logged-in users can access this route
# def dashboard():
#     """
#     Dashboard route. Accessible only to authenticated users.
#     """
#     return render_template('dashboard.html', username=current_user.username)
#
#
# ### Quote section
# # This section handles the leadership quotes functionality.
# @app.route('/quote')
# def quote():
#     """
#     Renders the leadership quotes page.
#     """
#     quotes = Quote.query.all()
#     if not quotes:
#         # If no quotes are found, you might want to handle it gracefully
#         flash('No quotes available at the moment.', 'info')
#         return render_template('leadership.html', title='Leadership Quotes', quotes=[])
#     return render_template('leadership.html', title='Leadership Quotes', quotes=quotes)
#
#
# @app.route('/quote/add', methods=['GET', 'POST'])
# def add_quote():
#     """
#        Route to add a new quote.
#        Handles both GET (render form) and POST (process submission).
#    """
#     if request.method == 'POST':
#         quote_text = request.form.get('quote_text').strip()
#         author = request.form.get('author_name').strip()
#
#         # Basic validation
#         if not quote_text or not author:
#             flash('Both quote and author are required!', 'error')
#             return render_template('add_quote.html', title='Add Quote',
#                                    quote=quote_text, author=author)
#
#         try:
#             new_quote = Quote(quote=quote_text, author=author)
#             db.session.add(new_quote)
#             # Commit the new quote to the database
#             db.session.commit()
#             flash('Quote added successfully!', 'success')
#             return redirect(url_for('quote'))  # Redirect to the quotes page after adding
#         except Exception as e:
#             app.logger.exception("Failed to add quote")
#             # Rollback the session in case of error
#             db.session.rollback()
#             flash(f'Failed to add quote. Please try again later. Error: {e}', 'error')
#             return render_template('add_quote.html', title='Add Quote',
#                                    quote=quote_text, author=author)
#
#     # If GET request, render the add quote form
#     return render_template('add_quote.html', title='Add Quote')
#
#
# # --- Main execution block ---
# if __name__ == '__main__':
#     # Ensure the database is created before running the app
#     with app.app_context():
#         # Create all database tables if they don't exist
#         db.create_all()
#
#         # if table is empty, create initial quote
#         if not Quote.query.first():
#             initial_quotes = [
#                 {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
#                 {"quote": "Leadership and learning are indispensable to each other.", "author": "John F. Kennedy"},
#                 {"quote": "A leader is one who knows the way, goes the way, and shows the way.",
#                  "author": "John C. Maxwell"},
#                 {"quote": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
#                 {"quote": "To handle yourself, use your head; to handle others, use your heart.",
#                  "author": "Eleanor Roosevelt"},
#                 {
#                     "quote": "Before you are a leader, success is all about growing yourself. When you become a leader, success is all about growing others.",
#                     "author": "Jack Welch"},
#                 {
#                     "quote": "The greatest leader is not necessarily the one who does the greatest things. He is the one that gets the people to do the greatest things.",
#                     "author": "Ronald Reagan"},
#                 {"quote": "Lead from the back — and let others believe they are in front.", "author": "Nelson Mandela"},
#                 {"quote": "The function of leadership is to produce more leaders, not more followers.",
#                  "author": "Ralph Nader"},
#                 {
#                     "quote": "Effective leadership is not about making speeches or being liked; leadership is defined by results not attributes.",
#                     "author": "Peter Drucker"}
#             ]
#             for quote in initial_quotes:
#                 q = Quote(quote=quote['quote'], author=quote['author'])
#                 db.session.add(q)
#             # Commit the initial quotes to the database
#             db.session.commit()
#             print("Initial quotes added to the database")
#
#     # Run the Flask development server.
#     # debug=True allows for automatic reloading on code changes and provides a debugger.
#     app.run(debug=True)
