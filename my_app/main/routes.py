from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from .. import mail # Use .. to go up one level to the package __init__

# Note: We don't need db here, but if you did, you'd import it from '..'

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='Home')

@main.route('/about')
def about():
    return render_template('about.html', title='About Us')

@main.route('/contact', methods=['GET', 'POST'])
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
