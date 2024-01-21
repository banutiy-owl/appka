from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import db, bcrypt
from . import auth_bp 
from app.models import User, BannedIP
from flask import jsonify, session
import time
import random

MAX_FAILED_ATTEMPTS = 3
BLOCK_TIME_SECONDS = 120

def login_fresh():
     return session.get('_fresh', False)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if not user:
            warning = 'User not found. Please try again.'
            flash(warning, 'danger')
            return render_template('auth/login.html', username=username, warning=warning)

        user_ip = request.remote_addr
        banned_ip = BannedIP.query.filter_by(ip_address=user_ip).first()

        if banned_ip:
            ban_expiry_timestamp = banned_ip.ban_expiry
            current_timestamp = time.time()

            if current_timestamp >= ban_expiry_timestamp:
                db.session.delete(banned_ip)
                db.session.commit()
            else:
                warning = 'Too many failed login attempts. Please try again later.'
                flash(warning, 'danger')
                return render_template('auth/login.html', username=username, warning=warning)

        time.sleep(2)

        return redirect(url_for('auth.password', username=username))

    return render_template('auth/login.html')



@auth_bp.route('/get_existing_values', methods=['GET'])
def get_existing_values_endpoint():
    existing_values = get_existing_values()
    return jsonify(existing_values)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    if '_fresh' in session:
        session.pop('_fresh')
    flash('Logout successful!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = ''.join([request.form[f'password{i}'] for i in range(16)])
        card_number = request.form['card_number']
        document_id = request.form['document_id']
        positions_combinations_pairs=[]

        existing_values = get_existing_values()
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if (
            username in existing_values['username'] or
            card_number in existing_values['card_number'] or
            document_id in existing_values['document_id']
        ):
            flash('Username, card number, or document ID is already taken. Please choose different values.', 'danger')
        else:
            for _ in range(5):
                pair = generate_random_combination(password)

                while pair in positions_combinations_pairs:
                    pair = generate_random_combination(password)

                positions_combinations_pairs.append(pair)
            positions_list, combinations_list = zip(*positions_combinations_pairs)
            session['positions_list'+username] = positions_list
            hashed_combinations = [bcrypt.generate_password_hash(''.join(combination)).decode('utf-8') for combination in combinations_list]

            new_user = User(
                username=username,
                password=hashed_password,
                card_number=card_number,
                document_id=document_id,
                combination_1=hashed_combinations[0],
                combination_2=hashed_combinations[1],
                combination_3=hashed_combinations[2],
                combination_4=hashed_combinations[3],
                combination_5=hashed_combinations[4]
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

def get_existing_values():
    existing_values = {
        'username': [user.username for user in User.query.all()],
        'card_number': [user.card_number for user in User.query.all()],
        'document_id': [user.document_id for user in User.query.all()]
    }
    return existing_values



@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        if bcrypt.check_password_hash(current_user.password, old_password):
            current_user.set_password(new_password)
            db.session.commit()

            flash('Password change successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Incorrect old password. Please try again.', 'danger')

    return render_template('auth/change_password.html')

@auth_bp.route('/password/<username>', methods=['GET', 'POST'])
def password(username):    
    session.modified = True
    user = User.query.filter_by(username=username).first()
    user_ip = request.remote_addr

    chosen_combination_number = session.get('chosen_combination_number')
    if chosen_combination_number is None or chosen_combination_number==0:
        chosen_combination_number = random.randint(1, 5)
        session['chosen_combination_number'] = chosen_combination_number
        session.modified = True
        
    chosen_combination_positions = session.get('positions_list_chosen')
    if chosen_combination_positions is None or chosen_combination_positions==[]:
        chosen_combination_positions = session.get('positions_list'+username)[chosen_combination_number - 1]
        session['positions_list_chosen'] = chosen_combination_positions
        session['last_chosen_combination_number'] = chosen_combination_number
        session.modified = True

    if request.method == 'POST':
        if user:
            chosen_combination = getattr(user, f'combination_{chosen_combination_number}')  
            entered_password = ''.join([
                request.form.get(f'password{i}', '') 
                for i in range(16)])
            session['chosen_combination_number'] = 0
            session['positions_list_chosen'] = []

            if bcrypt.check_password_hash(chosen_combination, entered_password):
                user.failed_login_attempts = 0
                db.session.commit()
                login_user(user)
                session['_fresh'] = True 
                flash('Login successful!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                user.failed_login_attempts += 1
                db.session.commit()
                if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                    banned_ip = BannedIP(ip_address=user_ip, ban_expiry=time.time() + BLOCK_TIME_SECONDS)
                    db.session.add(banned_ip)
                    db.session.commit()
                    warning='Too many failed login attempts. Please try again later'
                    flash(warning, 'danger')
                    time.sleep(2)
                    return render_template('auth/login.html', username=username, warning=warning)
                
                warning = 'Login unsuccessful. Check your password.'
                flash(warning, 'danger')
                time.sleep(2)
                return render_template('auth/password.html', username=username, warning=warning, chosen_combination_positions=chosen_combination_positions)
        flash('User not found. Please try again.', 'danger')
        warning = 'User not found. Please try again.'
        time.sleep(2)
        return render_template('auth/password.html', username=username, warning=warning)
    time.sleep(2)
    return render_template('auth/password.html', username=username, chosen_combination_positions=chosen_combination_positions)

def generate_random_combination(password):
    positions = sorted(random.sample(range(8), 4))
    combination = [password[i] for i in positions]
    return positions, combination
