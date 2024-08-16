import json
from datetime import datetime
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# User data
user_data = [
    {"id":9,"username":"Monroe","email":"marylnmonroe@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-08T17:19:43.960850","password":"1010"},
    {"id":11,"username":"Mason","email":"mason@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-08T17:31:10.303426","password":"1010"},
    {"id":12,"username":"Jena","email":"kendal.jena@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-08T18:19:19.564290","password":"1010"},
    {"id":13,"username":"ken","email":"ken.ngatia@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-08T20:18:19.459345","password":"1010"},
    {"id":14,"username":"zak","email":"zak@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-08T22:13:13.259206","password":"zak"},
    {"id":15,"username":"maddy","email":"karurimaddy@gmail.com","is_retailer":False,"is_admin":False,"created_at":"2024-08-08T23:33:35.237984","password":"1010"},
    {"id":16,"username":"Henry","email":"henry111@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-09T00:19:58.070982","password":"1010"},
    {"id":17,"username":"susan","email":"susan.kui@gmail.com","is_retailer":False,"is_admin":False,"created_at":"2024-08-09T16:26:43.126992","password":"1010"},
    {"id":18,"username":"Sam","email":"samsmith@gmail.com","is_retailer":False,"is_admin":False,"created_at":"2024-08-10T08:23:19.039844","password":"1010"},
    {"id":21,"username":"admin3","email":"admin3@example.com","is_retailer":False,"is_admin":True,"created_at":"2024-08-10T12:13:24.231402","password":"adminpassword"},
    {"id":22,"username":"margaret","email":"karurimargaret111@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-10T12:35:10.629195","password":"1010"},
    {"id":23,"username":"anita","email":"anita@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-10T13:03:24.926614","password":"1010"},
    {"id":25,"username":"maggie","email":"maggiek@gmail.com","is_retailer":False,"is_admin":False,"created_at":"2024-08-10T13:11:47.202788","password":"1010"},
    {"id":26,"username":"brian","email":"briankaruri@gmail.com","is_retailer":False,"is_admin":False,"created_at":"2024-08-10T13:53:16.291989","password":"1010"},
    {"id":27,"username":"baddie","email":"baddie@gmail.com","is_retailer":True,"is_admin":False,"created_at":"2024-08-10T18:19:53.428356","password":"1010"},
    {"id":31,"username":"brayo","email":"brayohmwas@gmail.com","is_retailer":False,"is_admin":False,"created_at":"2024-08-13T17:51:00.535524","password":"1010"}
]

def seed_users():
    # Create the application context
    app = create_app()  # Ensure this matches how you create your Flask app in `app.py`
    
    with app.app_context():
        for user in user_data:
            # Check if user already exists
            existing_user = User.query.filter_by(id=user['id']).first()
            
            if existing_user:
                # Update existing user
                existing_user.username = user['username']
                existing_user.email = user['email']
                existing_user.is_retailer = user['is_retailer']
                existing_user.is_admin = user['is_admin']
                existing_user.created_at = datetime.fromisoformat(user['created_at'])
                
                # Always hash the password and set it
                hashed_password = generate_password_hash(user['password'])
                existing_user.password = hashed_password
            else:
                # Create new user
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

        db.session.commit()


if __name__ == "__main__":
    seed_users()
