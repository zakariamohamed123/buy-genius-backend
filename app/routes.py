from flask import Blueprint, request, jsonify
from . import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({'message': 'Welcome to the Flask API!'})

@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@main.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!'}), 201
