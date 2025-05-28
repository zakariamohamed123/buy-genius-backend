from app import create_app, db
from app.models import User, Retailer, Category, Product

from datetime import datetime

# Initialize the Flask app using the factory
app = create_app()

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create categories
        electronics = Category(name="Electronics")
        fashion = Category(name="Fashion")
        home = Category(name="Home & Kitchen")
        db.session.add_all([electronics, fashion, home])
        db.session.commit()

        # Create admin user
        admin = User(
            username="admin",
            email="admin@buygenius.com",
            is_admin=True
        )
        admin.password = "admin123"
        db.session.add(admin)
        db.session.commit()

        # Create retailers (vendors)
        vendors = [
            {"name": "Naivas Supermarket", "whatsapp": "+254712345678"},
            {"name": "Jumia Kenya", "whatsapp": "+254712345679"},
            {"name": "Amazon Global", "whatsapp": "+15417543010"},
            {"name": "Kilimall Kenya", "whatsapp": "+254712345680"},
            {"name": "Souq UAE", "whatsapp": "+971501234567"}
        ]

        retailers = []
        for i, vendor in enumerate(vendors):
            user = User(
                username=f"vendor{i+1}",
                email=f"vendor{i+1}@example.com",
                is_retailer=True
            )
            user.password = "vendor123"
            db.session.add(user)
            db.session.flush()
            
            retailer = Retailer(
                name=vendor["name"],
                user_id=user.id,
                whatsapp_number=vendor["whatsapp"],
                approved=True
            )
            db.session.add(retailer)
            retailers.append(retailer)
        
        db.session.commit()

        # Create sample products
        products_data = [
            {
                "name": "Samsung Galaxy S23",
                "category": electronics,
                "variants": [
                    {"price": 115000, "delivery": 500, "value": 125000, "marginal": 0.15, "retailer": retailers[1]},
                    {"price": 120000, "delivery": 0, "value": 130000, "marginal": 0.12, "retailer": retailers[2]},
                    {"price": 110000, "delivery": 1000, "value": 120000, "marginal": 0.10, "retailer": retailers[3]},
                    {"price": 125000, "delivery": 800, "value": 135000, "marginal": 0.08, "retailer": retailers[4]}
                ]
            },
            {
                "name": "HP EliteBook 840",
                "category": electronics,
                "variants": [
                    {"price": 95000, "delivery": 1500, "value": 105000, "marginal": 0.12, "retailer": retailers[0]},
                    {"price": 89000, "delivery": 2000, "value": 98000, "marginal": 0.10, "retailer": retailers[1]},
                    {"price": 110000, "delivery": 0, "value": 120000, "marginal": 0.09, "retailer": retailers[2]}
                ]
            },
            {
                "name": "Levi's 501 Original Fit",
                "category": fashion,
                "variants": [
                    {"price": 4500, "delivery": 300, "value": 5000, "marginal": 0.05, "retailer": retailers[0]},
                    {"price": 5000, "delivery": 0, "value": 5500, "marginal": 0.10, "retailer": retailers[3]},
                    {"price": 4800, "delivery": 500, "value": 5300, "marginal": 0.04, "retailer": retailers[4]}
                ]
            }
        ]

        for product_data in products_data:
            for variant in product_data["variants"]:
                product = Product(
                    name=product_data["name"],
                    price=variant["price"],
                    description=f"Brand new {product_data['name']} from {variant['retailer'].name}",
                    delivery_cost=variant["delivery"],
                    payment_mode="Cash/Card/M-Pesa",
                    retailer_id=variant["retailer"].id,
                    category_id=product_data["category"].id,
                    estimated_value=variant["value"],
                    marginal_benefit=variant["marginal"],
                    image_url=f"https://example.com/images/{product_data['name'].replace(' ', '-').lower()}.jpg"
                )
                db.session.add(product)
        
        db.session.commit()
        print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
