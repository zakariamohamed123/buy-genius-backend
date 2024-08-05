import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin emails
    ADMIN_EMAIL_1 = os.getenv('ADMIN_EMAIL_1')
    ADMIN_EMAIL_2 = os.getenv('ADMIN_EMAIL_2')
    ADMIN_EMAIL_3 = os.getenv('ADMIN_EMAIL_3')
