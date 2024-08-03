# models.py
from sqlalchemy_serializer import SerializerMixin
from email_validator import validate_email, EmailNotValidError
from config import db
import bcrypt
from datetime import datetime
from sqlalchemy.orm import validates

# User model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_retailer = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    search_history = db.relationship('UserHistory', back_populates='user', cascade='all, delete-orphan')
    feedback = db.relationship('Feedback', back_populates='user', cascade='all, delete-orphan')
    inquiries = db.relationship('Inquiry', back_populates='user', cascade='all, delete-orphan')
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender', cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = ('-password_hash', '-search_history.user', '-feedback.user', '-inquiries.user', '-messages_sent.sender', '-wishlists.user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @validates('email')
    def validate_email(self, key, address):
        try:
            valid = validate_email(address) 
            email = valid.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {e}")
        return email

# Retailer model
class Retailer(db.Model, SerializerMixin):
    __tablename__ = 'retailers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    whatsapp_number = db.Column(db.String(20), nullable=True)

    products = db.relationship('Product', back_populates='retailer', cascade='all, delete-orphan')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver', cascade='all, delete-orphan')

    serialize_rules = ('-user', '-products.retailer', '-messages_received.receiver')

# Category model
class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

    serialize_rules = ('-products.category',)

# Product model
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    delivery_cost = db.Column(db.Float, nullable=True)
    payment_mode = db.Column(db.String(50), nullable=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailers.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200), nullable=True)

    feedback = db.relationship('Feedback', back_populates='product', cascade='all, delete-orphan')
    inquiries = db.relationship('Inquiry', back_populates='product', cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', back_populates='product', cascade='all, delete-orphan')

    serialize_rules = ('-retailer', '-category', '-feedback.product', '-inquiries.product', '-wishlists.product')

# Feedback model
class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    comment = db.Column(db.String(200), nullable=True)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='feedback')
    product = db.relationship('Product', back_populates='feedback')

    serialize_rules = ('-user.feedback', '-product.feedback')

# UserHistory model
class UserHistory(db.Model, SerializerMixin):
    __tablename__ = 'user_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_term = db.Column(db.String(200), nullable=True)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='search_history')

    serialize_rules = ('-user.search_history',)

#  Inquiry model
class Inquiry(db.Model, SerializerMixin):
    __tablename__ = 'inquiries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailers.id'), nullable=False)
    message = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='inquiries')
    product = db.relationship('Product', back_populates='inquiries')
    retailer = db.relationship('Retailer', back_populates='inquiries')

    serialize_rules = ('-user.inquiries', '-product.inquiries', '-retailer.inquiries')

#  Message model
class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('retailers.id'), nullable=False)
    content = db.Column(db.String(200), nullable=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', back_populates='messages_sent')
    receiver = db.relationship('Retailer', back_populates='messages_received')

    serialize_rules = ('-sender.messages_sent', '-receiver.messages_received')

# Wishlist model
class Wishlist(db.Model, SerializerMixin):
    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='wishlists')
    product = db.relationship('Product', back_populates='wishlists')

    serialize_rules = ('-user.wishlists', '-product.wishlists')

