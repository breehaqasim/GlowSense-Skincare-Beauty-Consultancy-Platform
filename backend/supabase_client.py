from supabase import create_client, Client
import os
from config import Config

# Check if Supabase credentials are available
if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in .env file")

try:
    # Initialize Supabase client
    supabase: Client = create_client(
        supabase_url=Config.SUPABASE_URL,
        supabase_key=Config.SUPABASE_KEY
    )
    
    # Test the connection
    supabase.auth.get_session()
    print("Successfully connected to Supabase!")
    
except Exception as e:
    print(f"Error connecting to Supabase: {str(e)}")
    raise 