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

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_retailer': self.is_retailer,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'whatsapp_number': self.whatsapp_number,
            'approved': self.approved,
            'user_id': self.user_id
        }

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

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
    estimated_value = db.Column(db.Float)  
    marginal_benefit = db.Column(db.Float)  
    
    feedbacks = db.relationship('Feedback', back_populates='product', cascade='all, delete-orphan')
    messages = db.relationship('Message', foreign_keys='Message.product_id', back_populates='product', cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', back_populates='product', cascade='all, delete-orphan')
    retailer = db.relationship('Retailer', back_populates='products')
    category = db.relationship('Category', back_populates='products')

    serialize_rules = ('-retailer.products', '-category.products', '-feedbacks.product', '-messages.product', '-wishlists.product')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'delivery_cost': self.delivery_cost,
            'payment_mode': self.payment_mode,
            'retailer_id': self.retailer_id,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat(),
            'image_url': self.image_url,
            'retailer_name': self.retailer.name if self.retailer else 'Unknown',
            'retailer_user_id': self.retailer.user_id if self.retailer else None  
        }

    def calculate_cost_benefit(self):
        total_cost = self.price + (self.delivery_cost or 0)
        benefit = self.estimated_value if self.estimated_value is not None else 0
        return benefit / total_cost if total_cost > 0 else 0

    def calculate_marginal_benefit(self):
        total_cost = self.price + (self.delivery_cost or 0)
        return self.marginal_benefit / total_cost if total_cost > 0 else 0

    def calculate_marginal_benefit(self):
        total_cost = self.price + (self.delivery_cost or 0)
        return self.marginal_benefit / total_cost if total_cost > 0 else 0

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    comment = db.Column(db.String)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='feedbacks')
    product = db.relationship('Product', back_populates='feedbacks')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'comment': self.comment,
            'feedback_date': self.feedback_date.isoformat()
        }

class UserHistory(db.Model, SerializerMixin):
    __tablename__ = 'user_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_term = db.Column(db.String)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='search_history')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'search_term': self.search_term,
            'searched_at': self.searched_at.isoformat()
        }

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailers.id'), nullable=True)
    content = db.Column(db.String, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
   
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='messages_sent')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='messages_received')
    product = db.relationship('Product', back_populates='messages')
    retailer = db.relationship('Retailer', back_populates='messages')

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'product_id': self.product_id,
            'retailer_id': self.retailer_id,
            'content': self.content,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }


class Wishlist(db.Model, SerializerMixin):
    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='wishlists')
    product = db.relationship('Product', back_populates='wishlists')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product': self.product.to_dict(),  
            'added_at': self.added_at.isoformat()
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailers.id'))
    seen = db.Column(db.Boolean, default=False)

    retailer = db.relationship('Retailer', backref=db.backref('notifications', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'retailer_id': self.retailer_id,
            'seen': self.seen
        }
