from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_retailer = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    retailers = db.relationship('Retailer', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    user_history = db.relationship('UserHistory', backref='user', lazy=True)
    inquiries = db.relationship('Inquiry', backref='user', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True)

class Retailer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    whatsapp_number = db.Column(db.String, nullable=True)
    products = db.relationship('Product', backref='retailer', lazy=True)
    inquiries = db.relationship('Inquiry', backref='retailer', lazy=True)
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    delivery_cost = db.Column(db.Float, nullable=True)
    payment_mode = db.Column(db.String, nullable=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String, nullable=True)
    feedbacks = db.relationship('Feedback', backref='product', lazy=True)
    inquiries = db.relationship('Inquiry', backref='product', lazy=True)
    wishlists = db.relationship('Wishlist', backref='product', lazy=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    comment = db.Column(db.String, nullable=True)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)

class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    search_term = db.Column(db.String, nullable=False)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('retailer.id'), nullable=False)
    content = db.Column(db.String, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
