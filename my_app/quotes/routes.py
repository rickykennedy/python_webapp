from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required

# Use .. to go up one level to the package __init__ to get db
# Import the db instance from the new extensions.py file
from ..extensions import db

# Import the Quote model from the models package
from ..models import Quote

# Create a Blueprint for quote-related routes
quotes = Blueprint('quotes', __name__)

@quotes.route('/quote')
def quote_list():
    """Displays the list of all quotes."""
    all_quotes = Quote.query.all()
    if not all_quotes:
        flash('No quotes available at the moment.', 'info')
    return render_template('leadership.html', title='Leadership Quotes', quotes=all_quotes)

@quotes.route('/quote/add', methods=['GET', 'POST'])
@login_required
def add_quote():
    """Provides a form to add a new quote and handles the submission."""
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
            return redirect(url_for('quotes.quote_list'))
        except Exception as e:
            current_app.logger.exception("Failed to add quote")
            db.session.rollback()
            flash(f'Failed to add quote. Error: {e}', 'error')
            return render_template('add_quote.html', title='Add Quote', quote=quote_text, author=author)

    return render_template('add_quote.html', title='Add Quote')
