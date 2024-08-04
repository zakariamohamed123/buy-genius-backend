# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_retailer = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    feedbacks = db.relationship('Feedback', back_populates='user', cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', back_populates='user', cascade='all, delete-orphan')
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender', cascade='all, delete-orphan')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver', cascade='all, delete-orphan')
    search_history = db.relationship('UserHistory', back_populates='user', cascade='all, delete-orphan')
    retailer = db.relationship('Retailer', uselist=False, back_populates='user')

    serialize_rules = ('-password_hash', '-feedbacks.user', '-wishlists.user', '-messages_sent.sender', '-messages_received.receiver', '-search_history.user', '-retailer.user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Retailer(db.Model, SerializerMixin):
    __tablename__ = 'retailers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    whatsapp_number = db.Column(db.String)
    
    approved = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='retailer')
    products = db.relationship('Product', back_populates='retailer', cascade='all, delete-orphan')
    messages = db.relationship('Message', foreign_keys='Message.retailer_id', back_populates='retailer', cascade='all, delete-orphan')

    serialize_rules = ('-user.retailer', '-products.retailer', '-messages.retailer')

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)
    delivery_cost = db.Column(db.Float)
    payment_mode = db.Column(db.String)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailers.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    image_url = db.Column(db.String)
    feedbacks = db.relationship('Feedback', back_populates='product', cascade='all, delete-orphan')
    messages = db.relationship('Message', foreign_keys='Message.product_id', back_populates='product', cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', back_populates='product', cascade='all, delete-orphan')
    retailer = db.relationship('Retailer', back_populates='products')
    category = db.relationship('Category', back_populates='products')

    serialize_rules = ('-retailer.products', '-category.products', '-feedbacks.product', '-messages.product', '-wishlists.product')

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    comment = db.Column(db.String)
    
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='feedbacks')
    product = db.relationship('Product', back_populates='feedbacks')

class UserHistory(db.Model, SerializerMixin):
    __tablename__ = 'user_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_term = db.Column(db.String)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='search_history')

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailers.id'), nullable=True)
    content = db.Column(db.String)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='messages_sent')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='messages_received')
    product = db.relationship('Product', back_populates='messages')
    retailer = db.relationship('Retailer', back_populates='messages')

class Wishlist(db.Model, SerializerMixin):
    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='wishlists')
    product = db.relationship('Product', back_populates='wishlists')
