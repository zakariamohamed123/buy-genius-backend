import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()  # Load .env file

class Config:
    # Security & Sessions
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-for-dev')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'buygenius_'

    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///local.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS Configuration
    CORS_ORIGINS = [
        "https://buy-genius.netlify.app",
        "http://localhost:3000"  # For local development
    ]

    # Admin emails
    ADMIN_EMAILS = [
        os.getenv('ADMIN_EMAIL_1'),
        os.getenv('ADMIN_EMAIL_2'),
        os.getenv('ADMIN_EMAIL_3'),
        os.getenv('ADMIN_EMAIL_4')
    ]