from flask import Blueprint, Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from datetime import datetime
from .models import db, User, Retailer, Category, Product, Feedback, UserHistory, Message, Wishlist

main = Blueprint('main', __name__)
api = Api(main)

# Authentication and User Management
class Signup(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            is_retailer=data.get('is_retailer', False),
            is_admin=data.get('is_admin', False)
        )
        new_user.password = data['password']
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.verify_password(data['password']):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': 'Invalid credentials'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
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
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            delivery_cost=data['delivery_cost'],
            payment_mode=data['payment_mode'],
            retailer_id=data['retailer_id'],
            category_id=data['category_id'],
            image_url=data['image_url']
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict(), 201
    
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

@main.route('/')
def index():
    return "Welcome to BuyGenius"
