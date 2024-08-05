from flask import Blueprint, request, session, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from datetime import datetime
from .models import db, User, Retailer, Category, Product, Feedback, UserHistory, Message, Wishlist
import os

main = Blueprint('main', __name__)
api = Api(main)

admin_emails = {
    os.getenv('ADMIN_EMAIL_1'),
    os.getenv('ADMIN_EMAIL_2'),
    os.getenv('ADMIN_EMAIL_3')
}

# Authentication and User Management
class Signup(Resource):
    def post(self):
        data = request.get_json()
        is_admin = data['email'] in admin_emails
        new_user = User(
            username=data['username'],
            email=data['email'],
            is_retailer=data.get('is_retailer', False),
            is_admin=is_admin
        )
        new_user.password = data['password']
        if new_user.is_retailer:
            new_user.retailer = Retailer(name=data['username'], user=new_user, approved=False)
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.verify_password(data['password']):
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
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            user.username = data['username']
            user.email = data['email']
            if 'password' in data:
                user.password = data['password']
            db.session.commit()
            return user.to_dict(), 200
        return {'error': 'User not found'}, 404

# Retailer Resource
class RetailerResource(Resource):
    def get(self, retailer_id=None):
        if retailer_id:
            retailer = Retailer.query.get(retailer_id)
            if retailer:
                return retailer.to_dict(), 200
            return {'error': 'Retailer not found'}, 404
        retailers = Retailer.query.all()
        return [retailer.to_dict() for retailer in retailers], 200

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
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get(category_id)
            if category:
                return category.to_dict(), 200
            return {'error': 'Category not found'}, 404
        categories = Category.query.all()
        return [category.to_dict() for category in categories], 200

    def post(self):
        data = request.get_json()
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return new_category.to_dict(), 201

# Product Resource
class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return product.to_dict(), 200
            return {'error': 'Product not found'}, 404
        products = Product.query.all()
        return [product.to_dict() for product in products], 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        user = User.query.get(user_id)
        if not user.is_retailer:
            return {'error': 'Only retailers can post products'}, 403

        data = request.get_json()
        new_product = Product(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            delivery_cost=data['delivery_cost'],
            payment_mode=data['payment_mode'],
            retailer_id=user.id, 
            category_id=data['category_id'],
            image_url=data['image_url']
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict(), 201

    def put(self, product_id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        product = Product.query.get(product_id)
        if not product or product.retailer_id != user.id:
            return {'error': 'Only the retailer who posted the product can update it'}, 403

        data = request.get_json()
        product.name = data['name']
        product.price = data['price']
        product.description = data['description']
        product.delivery_cost = data['delivery_cost']
        product.payment_mode = data['payment_mode']
        product.category_id = data['category_id']
        product.image_url = data['image_url']
        db.session.commit()
        return product.to_dict(), 200

    def delete(self, product_id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        product = Product.query.get(product_id)
        if not product or product.retailer_id != user.id:
            return {'error': 'Only the retailer who posted the product can delete it'}, 403

        db.session.delete(product)
        db.session.commit()
        return {}, 204

# Feedback Resource
class FeedbackResource(Resource):
    def get(self, feedback_id=None):
        if feedback_id:
            feedback = Feedback.query.get(feedback_id)
            if feedback:
                return feedback.to_dict(), 200
            return {'error': 'Feedback not found'}, 404
        feedbacks = Feedback.query.all()
        return [feedback.to_dict() for feedback in feedbacks], 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        data = request.get_json()
        new_feedback = Feedback(
            user_id=user_id,
            product_id=data['product_id'],
            comment=data['comment']
        )
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback.to_dict(), 201

# Wishlist Resource
class WishlistResource(Resource):
    def get(self, wishlist_id=None):
        if wishlist_id:
            wishlist = Wishlist.query.get(wishlist_id)
            if wishlist:
                return wishlist.to_dict(), 200
            return {'error': 'Wishlist item not found'}, 404
        wishlists = Wishlist.query.all()
        return [wishlist.to_dict() for wishlist in wishlists], 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        data = request.get_json()
        new_wishlist_item = Wishlist(
            user_id=user_id,
            product_id=data['product_id']
        )
        db.session.add(new_wishlist_item)
        db.session.commit()
        return new_wishlist_item.to_dict(), 201

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
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        data = request.get_json()
        new_message = Message(
            sender_id=user_id,
            receiver_id=data['receiver_id'],
            product_id=data.get('product_id'),
            retailer_id=data.get('retailer_id'),
            content=data['content']
        )
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201

# Dashboard for Admin
class AdminDashboard(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        if not user.is_admin:
            return {'error': 'Only admins can access this'}, 403

        retailers = Retailer.query.filter_by(approved=False).all()
        users = User.query.all()
        products = Product.query.all()
        analytics = {
            'total_users': len(users),
            'total_retailers': len(retailers),
            'total_products': len(products)
        }

        return {
            'retailers': [retailer.to_dict() for retailer in retailers],
            'users': [user.to_dict() for user in users],
            'products': [product.to_dict() for product in products],
            'analytics': analytics
        }, 200

    def post(self, retailer_id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        if not user.is_admin:
            return {'error': 'Only admins can access this'}, 403

        retailer = Retailer.query.get(retailer_id)
        if not retailer:
            return {'error': 'Retailer not found'}, 404

        retailer.approved = True
        db.session.commit()
        return retailer.to_dict(), 200

# Dashboard for Retailers
class RetailerDashboard(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        if not user.is_retailer:
            return {'error': 'Only retailers can access this'}, 403

        products = Product.query.filter_by(retailer_id=user.id).all()
        messages = Message.query.filter_by(retailer_id=user.id).all()

        return {
            'products': [product.to_dict() for product in products],
            'messages': [message.to_dict() for message in messages]
        }, 200


# Dashboard for Users
class UserDashboard(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        wishlists = Wishlist.query.filter_by(user_id=user.id).all()
        feedbacks = Feedback.query.filter_by(user_id=user.id).all()
        messages = Message.query.filter_by(sender_id=user.id).all()
        search_history = UserHistory.query.filter_by(user_id=user.id).all()

        return {
            'user': user.to_dict(),
            'wishlists': [wishlist.to_dict() for wishlist in wishlists],
            'feedbacks': [feedback.to_dict() for feedback in feedbacks],
            'messages': [message.to_dict() for message in messages],
            'search_history': [history.to_dict() for history in search_history]
        }, 200
    
class ApproveRetailer(Resource):
    def post(self, retailer_id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        if not user.is_admin:
            return {'error': 'Only admins can access this'}, 403

        retailer = Retailer.query.get(retailer_id)
        if not retailer:
            return {'error': 'Retailer not found'}, 404

        retailer.approved = True
        db.session.commit()
        return retailer.to_dict(), 200




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
api.add_resource(AdminDashboard, '/admin_dashboard', '/admin_dashboard/<int:retailer_id>')
api.add_resource(RetailerDashboard, '/retailer_dashboard')
api.add_resource(UserDashboard, '/user_dashboard')
api.add_resource(ApproveRetailer, '/approve_retailer/<int:retailer_id>')

@main.route('/')
def index():
    return "Welcome to BuyGenius"
