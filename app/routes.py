from flask import Blueprint, request, session, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from datetime import datetime
from .models import db, User, Retailer, Category, Product, Feedback, UserHistory, Message, Wishlist, Notification, SearchHistory
import os
from sqlalchemy.exc import IntegrityError
from functools import wraps

# Initialize Blueprint and API
main = Blueprint('main', __name__)
api = Api(main)

# List of admin emails for authorization
admin_emails = {
    os.getenv('ADMIN_EMAIL_1'),
    os.getenv('ADMIN_EMAIL_2'),
    os.getenv('ADMIN_EMAIL_3'),
    os.getenv('ADMIN_EMAIL_4')
}

# Decorator to check if a token is required
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)

    return decorator

# Authentication and User Management

class Signup(Resource):
    def post(self):
        data = request.get_json()

        if not data.get('email'):
            return {'error': 'Email is required'}, 400
        
        if not data.get('username'):
            return {'error': 'Username is required'}, 400
        
        if not data.get('password'):
            return {'error': 'Password is required'}, 400

        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already in use'}, 400

        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already in use'}, 400

        is_admin = data['email'] in admin_emails
        is_retailer = data.get('is_retailer', False)

        new_user = User(
            username=data['username'],
            email=data['email'],
            is_retailer=is_retailer,
            is_admin=is_admin
        )
        new_user.password = data['password']

        try:
            db.session.add(new_user)
            db.session.flush()

            if is_retailer:
                new_retailer = Retailer(name=data['username'], user=new_user, approved=False)
                db.session.add(new_retailer)
                
                notification = Notification(
                    message=f"New retailer {new_user.username} has requested access.",
                    retailer_id=new_retailer.id
                )
                db.session.add(notification)

            db.session.commit()
            return new_user.to_dict(), 201

        except IntegrityError:
            db.session.rollback()
            return {'error': 'Database error, please try again later'}, 500

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user and user.verify_password(data['password']):
            if user.is_retailer and not user.retailer.approved:
                return {'error': 'Retailer account not approved yet. Please wait for admin approval.'}, 403
            
            session['user_id'] = user.id
            session['is_retailer'] = user.is_retailer
            session['is_admin'] = user.is_admin
            return user.to_dict(), 200

        return {'error': 'Invalid credentials'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        session.pop('is_retailer', None)
        session.pop('is_admin', None)
        return '', 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {
                    'id': user.id,
                    'username': user.username,
                    'is_retailer': user.is_retailer,
                    'is_admin': user.is_admin
                }, 200
        return {}, 204

class ClearSession(Resource):
    def delete(self):
        session.clear()
        return {}, 204

# User Resource
class UserResource(Resource):
    @token_required
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404
        else:
            role = request.args.get('role')
            status = request.args.get('status')
            search = request.args.get('search')

            query = User.query

            if role:
                if role == "Admin":
                    query = query.filter_by(is_admin=True)
                elif role == "Retailer":
                    query = query.filter_by(is_retailer=True)
                else:
                    query = query.filter_by(is_admin=False, is_retailer=False)

            if status:
                query = query.filter_by(status=status)

            if search:
                query = query.filter(
                    (User.username.ilike(f'%{search}%')) |
                    (User.email.ilike(f'%{search}%'))
                )

            users = query.all()
            return [user.to_dict() for user in users], 200

    @token_required
    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'password' in data:
                user.password = data['password']
            db.session.commit()
            return user.to_dict(), 200
        return {'error': 'User not found'}, 404

    @token_required
    def patch(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            if 'approved' in data:
                if not user.is_admin:
                    retailer = Retailer.query.filter_by(user_id=user_id).first()
                    if retailer:
                        retailer.approved = data['approved']
                        db.session.commit()
                        return retailer.to_dict(), 200
                    return {'error': 'Retailer not found'}, 404
                else:
                    return {'error': 'Admin users cannot change approval status'}, 403
            return {'error': 'No fields to update'}, 400
        return {'error': 'User not found'}, 404

    @token_required
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            if user.is_admin:
                return {'error': 'Cannot delete an admin user'}, 403
            
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        return {'error': 'User not found'}, 404

# Retailer Resource
class RetailerResource(Resource):
    @token_required
    def get(self, retailer_id=None):
        if retailer_id:
            retailer = Retailer.query.get(retailer_id)
            if retailer:
                return retailer.to_dict(), 200
            return {'error': 'Retailer not found'}, 404
        retailers = Retailer.query.all()
        return [retailer.to_dict() for retailer in retailers], 200

    @token_required
    def post(self):
        data = request.get_json()
        new_retailer = Retailer(
            name=data['name'],
            user_id=data['user_id'],
            whatsapp_number=data['whatsapp_number']
        )
        db.session.add(new_retailer)
        db.session.commit()
        return new_retailer.to_dict(), 201

# Category Resource
class CategoryResource(Resource):
    @token_required
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get(category_id)
            if category:
                return category.to_dict(), 200
            return {'error': 'Category not found'}, 404
        categories = Category.query.all()
        return [category.to_dict() for category in categories], 200

    @token_required
    def post(self):
        data = request.get_json()
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return new_category.to_dict(), 201

# Product Resource
class ProductResource(Resource):
    @token_required
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return product.to_dict(), 200
            return {'error': 'Product not found'}, 404
        products = Product.query.all()
        return [product.to_dict() for product in products], 200

    @token_required
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        if not user.is_retailer:
            return {'error': 'Only retailers can add products'}, 403

        data = request.get_json()
        new_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            retailer_id=user.retailer.id,
            category_id=data['category_id']
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict(), 201

# Feedback Resource
class FeedbackResource(Resource):
    @token_required
    def get(self, feedback_id=None):
        if feedback_id:
            feedback = Feedback.query.get(feedback_id)
            if feedback:
                return feedback.to_dict(), 200
            return {'error': 'Feedback not found'}, 404
        feedbacks = Feedback.query.all()
        return [feedback.to_dict() for feedback in feedbacks], 200

    @token_required
    def post(self):
        data = request.get_json()
        new_feedback = Feedback(
            user_id=session.get('user_id'),
            product_id=data['product_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback.to_dict(), 201

# Message Resource
class MessageResource(Resource):
    def get(self, message_id=None):
        if message_id:
            message = Message.query.get(message_id)
            if message:
                return message.to_dict(), 200
            return {'error': 'Message not found'}, 404
        messages = Message.query.all()
        return [message.to_dict() for message in messages], 200

    def post(self):
        data = request.get_json()
        new_message = Message(
            sender_id=data['sender_id'],
            recipient_id=data['recipient_id'],
            content=data['content']
        )
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201

# Wishlist Resource
class WishlistResource(Resource):
    @token_required
    def get(self):
        user_id = session.get('user_id')
        wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
        return [item.to_dict() for item in wishlist_items], 200

    @token_required
    def post(self):
        data = request.get_json()
        new_wishlist_item = Wishlist(
            user_id=session.get('user_id'),
            product_id=data['product_id']
        )
        db.session.add(new_wishlist_item)
        db.session.commit()
        return new_wishlist_item.to_dict(), 201

# Notification Resource
class NotificationResource(Resource):
    @token_required
    def get(self):
        user_id = session.get('user_id')
        notifications = Notification.query.filter_by(user_id=user_id).all()
        return [notification.to_dict() for notification in notifications], 200

    @token_required
    def post(self):
        data = request.get_json()
        new_notification = Notification(
            user_id=session.get('user_id'),
            message=data['message']
        )
        db.session.add(new_notification)
        db.session.commit()
        return new_notification.to_dict(), 201
# Retailer Dashboard Resource
class RetailerDashboard(Resource):
    def get(self):
        # Ensure the user is authenticated and is a retailer
        if 'user_id' not in session or not session.get('is_retailer'):
            return {'error': 'Unauthorized access'}, 403

        # Retrieve and return retailer-specific data
        user_id = session.get('user_id')
        retailer = Retailer.query.filter_by(user_id=user_id).first()
        if retailer:
            return retailer.to_dict(), 200
        return {'error': 'Retailer not found'}, 404

# User Dashboard Resource
class UserDashboard(Resource):
    def get(self):
        # Ensure the user is authenticated
        if 'user_id' not in session:
            return {'error': 'Unauthorized access'}, 403

        # Retrieve and return user-specific data
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if user:
            return user.to_dict(), 200
        return {'error': 'User not found'}, 404

# Approve Retailer Resource
class ApproveRetailer(Resource):
    def post(self, retailer_id):
        # Ensure the user is authenticated and is an admin
        if 'user_id' not in session or not session.get('is_admin'):
            return {'error': 'Unauthorized access'}, 403

        retailer = Retailer.query.get(retailer_id)
        if retailer:
            retailer.approved = True
            db.session.commit()
            return {'message': 'Retailer approved successfully'}, 200
        return {'error': 'Retailer not found'}, 404

# Reject Retailer Resource
class RejectRetailer(Resource):
    def post(self, retailer_id):
        # Ensure the user is authenticated and is an admin
        if 'user_id' not in session or not session.get('is_admin'):
            return {'error': 'Unauthorized access'}, 403

        retailer = Retailer.query.get(retailer_id)
        if retailer:
            db.session.delete(retailer)
            db.session.commit()
            return {'message': 'Retailer rejected and removed successfully'}, 200
        return {'error': 'Retailer not found'}, 404

# Search Products Resource
class SearchProductsResource(Resource):
    def get(self, query):
        # Perform search based on query string
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
        return [product.to_dict() for product in products], 200

# Search History Resource
class SearchHistoryResource(Resource):
    def get(self):
        # Ensure the user is authenticated
        if 'user_id' not in session:
            return {'error': 'Unauthorized access'}, 403

        # Retrieve and return search history for the authenticated user
        user_id = session.get('user_id')
        search_history = SearchHistory.query.filter_by(user_id=user_id).all()
        return [item.to_dict() for item in search_history], 200
class AdminDashboard(Resource):
    def get(self):
        # Ensure the user is authenticated and is an admin
        if 'user_id' not in session or not session.get('is_admin'):
            return {'error': 'Unauthorized access'}, 403

        # Retrieve and return admin-specific data
        admins = User.query.filter_by(role='admin').all()
        retailers = Retailer.query.all()
        users = User.query.all()
        return {
            'admins': [admin.to_dict() for admin in admins],
            'retailers': [retailer.to_dict() for retailer in retailers],
            'users': [user.to_dict() for user in users]
        }, 200

# Register resources with the API
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(ClearSession, '/clear_session')
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(RetailerResource, '/retailers', '/retailers/<int:retailer_id>')
api.add_resource(CategoryResource, '/categories', '/categories/<int:category_id>')
api.add_resource(ProductResource, '/products', '/products/<int:product_id>')
api.add_resource(FeedbackResource, '/feedback', '/feedback/<int:feedback_id>')
api.add_resource(WishlistResource, '/wishlist', '/wishlist/<int:wishlist_id>')
api.add_resource(MessageResource, '/messages', '/messages/<int:message_id>')
api.add_resource(AdminDashboard, '/admin_dashboard')
api.add_resource(RetailerDashboard, '/retailer_dashboard')
api.add_resource(UserDashboard, '/user_dashboard')
api.add_resource(ApproveRetailer, '/approve_retailer/<int:retailer_id>')
api.add_resource(NotificationResource, '/notifications')
api.add_resource(RejectRetailer, '/reject_retailer/<int:retailer_id>')
api.add_resource(SearchProductsResource, '/search/<string:query>')
api.add_resource(SearchHistoryResource, '/search_history')

@main.route('/')
def index():
    return "Welcome to BuyGenius"
