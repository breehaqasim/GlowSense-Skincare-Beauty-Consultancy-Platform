import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask secret key
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")

    # Supabase configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    if not SUPABASE_URL:
        raise ValueError("No SUPABASE_URL set. Please add it to your .env file")

    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    if not SUPABASE_KEY:
        raise ValueError("No SUPABASE_KEY set. Please add it to your .env file")

    # Remove SQLAlchemy configuration as we're using Supabase
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False 