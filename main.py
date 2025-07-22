import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

#initialize the Flask application
app = Flask(__name__)

# --- Flask Configuration for Secret Key and Mail ---
# A secret key is required for flashing messages and session management.
# In a real application, use a strong, randomly generated key stored securely.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key_for_dev')

# Flask-Mail configuration from environment variables
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 't')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME') # Default sender is usually the MAIL_USERNAME

# Initialize Flask-Mail
mail = Mail(app)

# Flask-SQLAlchemy configuration
# The database URI is fetched from the DATABASE_URL environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# Suppress SQLAlchemy's track modification warnings, as it consumes extra memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Model (if needed) ---
# Example model for storing contact messages (if you want to save them in a database)
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
        Returns a string that includes the quote and the author.
        """
        return f'<Quote {self.quote} by {self.author}>'


# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    """
    Renders the about page of the website.
    """
    return render_template('about.html', title='About Us')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Renders the contact page of the website.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        # Basic validation
        if not name or not email or not subject or not message_body:
            flash('All fields are required!', 'error') # 'error' is a category for styling
            return render_template('contact.html', title='Contact Us',
                                   name=name, email=email, subject=subject, message_body=message_body)

        try:
            # Create the email message
            msg = Message(
                subject=f"Contact Form: {subject}",
                sender=app.config['MAIL_DEFAULT_SENDER'], # Your configured sender email
                recipients=[app.config['MAIL_USERNAME']] # Send to your own email address
            )
            # Add HTML content for better formatting in email clients
            msg.html = render_template('email_template.html',
                                       name=name, email=email, subject=subject, message_body=message_body)

            mail.send(msg)
            flash('Your message has been sent successfully!', 'success') # 'success' category
            return redirect(url_for('contact')) # Redirect to clear the form after successful submission
        except Exception as e:
            flash(f'Failed to send message. Please try again later. Error: {e}', 'error')
            # Stay on the contact page with pre-filled form in case of error
            return render_template('contact.html', title='Contact Us',
                                   name=name, email=email, subject=subject, message_body=message_body)
        
    # If GET request, render the contact form
    return render_template('contact.html', title='Contact Us')

@app.route('/quote')
def quote():
    """
    Renders the leadership quotes page.
    """
    quotes = Quote.query.all()
    if not quotes:
        # If no quotes are found, you might want to handle it gracefully
        flash('No quotes available at the moment.', 'info')
        return render_template('leadership.html', title='Leadership Quotes', quotes=[])
    return render_template('leadership.html', title='Leadership Quotes', quotes=quotes)

@app.route('/quote/add', methods=['GET', 'POST'])
def add_quote():
    """
    Route to add a new quote.
    """
    if request.method == 'POST':
        quote_text = request.form.get('quote')
        author = request.form.get('author')

        # Basic validation
        if not quote_text or not author:
            flash('Both quote and author are required!', 'error')
            return render_template('add_quote.html', title='Add Quote',
                                   quote=quote_text, author=author)

        try:
            new_quote = Quote(quote=quote_text, author=author)
            db.session.add(new_quote)
            # Commit the new quote to the database
            db.session.commit()
            flash('Quote added successfully!', 'success')
            return redirect(url_for('quote')) # Redirect to the quotes page after adding
        except Exception as e:
            # Rollback the session in case of error
            db.session.rollback()
            flash(f'Failed to add quote. Please try again later. Error: {e}', 'error')
            return render_template('add_quote.html', title='Add Quote',
                                   quote=quote_text, author=author)

    # If GET request, render the add quote form
    return render_template('add_quote.html', title='Add Quote')

# --- Main execution block ---
if __name__ == '__main__':
    # Ensure the database is created before running the app
    with app.app_context():
        # Create all database tables if they don't exist
        db.create_all()

        #if table is empty, create initial quote
        if not Quote.query.first():
            initial_quotes = [
                {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
                {"quote": "Leadership and learning are indispensable to each other.", "author": "John F. Kennedy"},
                {"quote": "A leader is one who knows the way, goes the way, and shows the way.", "author": "John C. Maxwell"},
                {"quote": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
                {"quote": "To handle yourself, use your head; to handle others, use your heart.", "author": "Eleanor Roosevelt"},
                {"quote": "Before you are a leader, success is all about growing yourself. When you become a leader, success is all about growing others.", "author": "Jack Welch"},
                {"quote": "The greatest leader is not necessarily the one who does the greatest things. He is the one that gets the people to do the greatest things.", "author": "Ronald Reagan"},
                {"quote": "Lead from the back — and let others believe they are in front.", "author": "Nelson Mandela"},
                {"quote": "The function of leadership is to produce more leaders, not more followers.", "author": "Ralph Nader"},
                {"quote": "Effective leadership is not about making speeches or being liked; leadership is defined by results not attributes.", "author": "Peter Drucker"}
            ]
            for quote in initial_quotes:
                q = Quote(quote=quote['quote'], author=quote['author'])
                db.session.add(q)
            # Commit the initial quotes to the database    
            db.session.commit()
            print("Initial quotes added to the database")
        

    # Run the Flask development server.
    # debug=True allows for automatic reloading on code changes and provides a debugger.
    app.run(debug=True)