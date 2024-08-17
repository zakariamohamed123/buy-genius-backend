import json
from datetime import datetime
from app import create_app, db
from app.models import User, Product, Category  # Ensure Category model is imported
from werkzeug.security import generate_password_hash

# User data (including admin3 details)
user_data = [
    {"id": 9, "username": "Monroe", "email": "marylnmonroe@gmail.com", "is_retailer": True, "is_admin": False, "created_at": "2024-08-08T17:19:43.960850", "password": "1010"},
    {"id": 11, "username": "Mason", "email": "mason@gmail.com", "is_retailer": True, "is_admin": False, "created_at": "2024-08-08T17:31:10.303426", "password": "1010"},
    {"id": 12, "username": "Jena", "email": "kendal.jena@gmail.com", "is_retailer": True, "is_admin": False, "created_at": "2024-08-08T18:19:19.564290", "password": "1010"},
    {"id": 13, "username": "admin3", "email": "admin3@gmail.com", "is_retailer": False, "is_admin": True, "created_at": "2024-08-10T10:00:00.000000", "password": "adminpassword"},
]

# Category data
category_data = [
    {"id": 1, "name": "Electronics"},
    {"id": 2, "name": "Fashion"},
    {"id": 3, "name": "Home Appliances"},
    {"id": 4, "name": "Books"},
    {"id": 5, "name": "Health & Beauty"},
    # Add more categories if needed
]

# Product data (with category_id 1 assigned to Electronics)
product_data = [
    {
        "id": 73,
        "name": "Lenovo Laptop",
        "price": 85000,
        "description": "500 Gb ROM 8GB RAM",
        "delivery_cost": 150,
        "payment_mode": "After Delivery",
        "retailer_id": 2,
        "category_id": 1,  # Electronics
        "created_at": "2024-08-08T22:32:17.783080",
        "image_url": "https://images.pexels.com/photos/25589787/pexels-photo-25589787/free-photo-of-laptop-with-blank-screen.jpeg?auto=compress&cs=tinysrgb&w=600",
    },
    {
        "id": 74,
        "name": "Samsung S24 ultra",
        "price": 70000,
        "description": "Best Affordable phone",
        "delivery_cost": 350,
        "payment_mode": "After Delivery",
        "retailer_id": 2,
        "category_id": 1,  # Electronics
        "created_at": "2024-08-08T23:53:54.469201",
        "image_url": "https://images.pexels.com/photos/50614/pexels-photo-50614.jpeg?auto=compress&cs=tinysrgb&w=600",
    },
    # Add more products if needed
]

def seed_users():
    app = create_app()
    
    with app.app_context():
        # Seed categories
        for category in category_data:
            existing_category = Category.query.filter_by(id=category['id']).first()
            
            if existing_category:
                existing_category.name = category['name']
            else:
                new_category = Category(
                    id=category['id'],
                    name=category['name']
                )
                db.session.add(new_category)
        
        # Seed users
        for user in user_data:
            existing_user = User.query.filter_by(id=user['id']).first()
            
            if existing_user:
                existing_user.username = user['username']
                existing_user.email = user['email']
                existing_user.is_retailer = user['is_retailer']
                existing_user.is_admin = user['is_admin']
                existing_user.created_at = datetime.fromisoformat(user['created_at'])
                existing_user.password = generate_password_hash(user['password'])
            else:
                new_user = User(
                    id=user['id'],
                    username=user['username'],
                    email=user['email'],
                    is_retailer=user['is_retailer'],
                    is_admin=user['is_admin'],
                    created_at=datetime.fromisoformat(user['created_at']),
                    password=generate_password_hash(user['password'])
                )
                db.session.add(new_user)
        
        # Seed products
        for product in product_data:
            existing_product = Product.query.filter_by(id=product['id']).first()
            
            if existing_product:
                existing_product.name = product['name']
                existing_product.price = product['price']
                existing_product.description = product['description']
                existing_product.delivery_cost = product['delivery_cost']
                existing_product.payment_mode = product['payment_mode']
                existing_product.retailer_id = product['retailer_id']
                existing_product.category_id = product['category_id']
                existing_product.created_at = datetime.fromisoformat(product['created_at'])
                existing_product.image_url = product['image_url']
            else:
                new_product = Product(
                    id=product['id'],
                    name=product['name'],
                    price=product['price'],
                    description=product['description'],
                    delivery_cost=product['delivery_cost'],
                    payment_mode=product['payment_mode'],
                    retailer_id=product['retailer_id'],
                    category_id=product['category_id'],
                    created_at=datetime.fromisoformat(product['created_at']),
                    image_url=product['image_url']
                )
                db.session.add(new_product)

        db.session.commit()

if __name__ == "__main__":
    seed_users()
