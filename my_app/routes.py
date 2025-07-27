from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_

# Use relative imports to get the db/mail objects and models
from . import db, mail
from .models import ContactMessage, Quote, User
from flask_mail import Message

# Create a Blueprint
main_routes = Blueprint('main', __name__)

# --- General Routes ---
@main_routes.route('/')
def index():
    return render_template('index.html', title='Home')

@main_routes.route('/about')
def about():
    return render_template('about.html', title='About Us')

@main_routes.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        if not all([name, email, subject, message_body]):
            flash('All fields are required!', 'error')
            return render_template('contact.html', title='Contact Us', name=name, email=email, subject=subject, message_body=message_body)

        try:
            msg = Message(
                subject=f"Contact Form: {subject}",
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[current_app.config['MAIL_USERNAME']]
            )
            msg.html = render_template('email_template.html', name=name, email=email, subject=subject, message_body=message_body)
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {e}")
            flash(f'Failed to send message. Please try again later.', 'error')
            return render_template('contact.html', title='Contact Us', name=name, email=email, subject=subject, message_body=message_body)

    return render_template('contact.html', title='Contact Us')

# --- Authentication Routes ---
@main_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([username, email, password]):
            flash('Username, email, and password are required!', 'danger')
            return render_template('signup.html')

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists.', 'warning')
            return render_template('signup.html')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('signup.html')

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter(or_(User.username == username, User.email == username)).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username/email and password', 'danger')

    return render_template('login.html')

@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# --- Quote Routes ---
@main_routes.route('/quote')
def quote():
    quotes = Quote.query.all()
    if not quotes:
        flash('No quotes available at the moment.', 'info')
    return render_template('leadership.html', title='Leadership Quotes', quotes=quotes)

@main_routes.route('/quote/add', methods=['GET', 'POST'])
@login_required
def add_quote():
    if request.method == 'POST':
        quote_text = request.form.get('quote_text', '').strip()
        author = request.form.get('author_name', '').strip()

        if not quote_text or not author:
            flash('Both quote and author are required!', 'error')
            return render_template('add_quote.html', title='Add Quote', quote=quote_text, author=author)

        try:
            new_quote = Quote(quote=quote_text, author=author)
            db.session.add(new_quote)
            db.session.commit()
            flash('Quote added successfully!', 'success')
            return redirect(url_for('main.quote'))
        except Exception as e:
            current_app.logger.exception("Failed to add quote")
            db.session.rollback()
            flash(f'Failed to add quote. Error: {e}', 'error')
            return render_template('add_quote.html', title='Add Quote', quote=quote_text, author=author)

    return render_template('add_quote.html', title='Add Quote')
