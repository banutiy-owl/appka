from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import main_bp
from app import db, cache
from app.models import User, Transaction

@main_bp.route('/dashboard')
@login_required
@cache.cached(timeout=300, key_prefix='dashboard')
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('main/dashboard.html', transactions=transactions)

@main_bp.route('/profile')
@login_required
@cache.cached(timeout=300, key_prefix='profile')
def profile():
    return render_template('main/profile.html')

@main_bp.route('/transfer', methods=['GET', 'POST'])
@login_required
@cache.cached(timeout=300, key_prefix='transfer')
def transfer():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        recipient_card_number = request.form.get('recipient')

        recipient = User.query.filter_by(card_number=recipient_card_number).first()

        if not recipient:
            warning='User not found. Transfer failed.'
            flash(warning, 'error')
            return render_template('main/transfer.html', warning=warning)

        new_transaction = Transaction(amount=amount, title='Transfer', user_id=current_user.id, recipient_card_number=recipient_card_number)
        db.session.add(new_transaction)
        db.session.commit()

        recipient_transaction = Transaction(amount=amount, title='Received', user_id=recipient.id,  recipient_card_number=current_user.card_number)
        db.session.add(recipient_transaction)
        db.session.commit()

        flash('Transfer successful!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('main/transfer.html')
