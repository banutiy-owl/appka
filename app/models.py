from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)
    document_id = db.Column(db.String(20), unique=True, nullable=False)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    combination_1 = db.Column(db.String(16), nullable=True)
    combination_2 = db.Column(db.String(16), nullable=True)
    combination_3 = db.Column(db.String(16), nullable=True)
    combination_4 = db.Column(db.String(16), nullable=True)
    combination_5 = db.Column(db.String(16), nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0) 


    def __repr__(self):
        return f"User('{self.username}', '{self.document_id}', '{self.card_number}')"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    recipient_card_number = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.amount}', '{self.title}', '{self.recipient}', '{self.timestamp}')"


class BannedIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False, unique=True)
    ban_expiry = db.Column(db.Float, nullable=False)