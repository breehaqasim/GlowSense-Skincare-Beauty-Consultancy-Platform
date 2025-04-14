from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from supabase_client import supabase
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
# Configure CORS to allow requests from the frontend
CORS(app, resources={r"/*": {"origins": "*"}})

# Load configuration
app.config.from_object(Config)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            # Verify token with Supabase
            user = supabase.auth.get_user(token)
            return f(user, *args, **kwargs)
        except:
            return jsonify({'message': 'Token is invalid'}), 401
    return decorated

# Route for home page
@app.route('/')
def home():
    return "Welcome to Glow Sense Skincare & Beauty Consultancy Platform"

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print("Received registration data:", data)
        
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Create user in Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": data['email'],
            "password": data['password'],
            "options": {
                "data": {
                    "username": data['username']
                }
            }
        })
        
        if auth_response.user:
            # Insert additional user data into our users table
            user_data = {
                "id": auth_response.user.id,
                "username": data['username'],
                "email": data['email'],
                "created_at": datetime.utcnow().isoformat()
            }
            
            supabase.table('users').insert(user_data).execute()
            
            return jsonify({
                'message': 'User registered successfully',
                'user': {
                    'id': auth_response.user.id,
                    'email': auth_response.user.email,
                    'username': data['username']
                }
            }), 201
        else:
            return jsonify({'message': 'Registration failed'}), 400
            
    except Exception as e:
        print("Registration error:", str(e))
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Login attempt for email: {data.get('email')}")  # Debug log
        
        # Sign in with Supabase
        auth_response = supabase.auth.sign_in_with_password({
            "email": data['email'],
            "password": data['password']
        })
        
        if not auth_response.user:
            print("No user returned from Supabase")  # Debug log
            return jsonify({'message': 'Invalid email or password'}), 401
            
        # Get user data
        user = auth_response.user
        session = auth_response.session
        
        print(f"Login successful for user: {user.email}")  # Debug log
        
        return jsonify({
            'token': session.access_token,
            'user': {
                'id': user.id,
                'email': user.email
            }
        })
    except Exception as e:
        print(f"Login error details: {str(e)}")  # Detailed error log
        return jsonify({'message': 'Invalid email or password'}), 401

# Route to get user's consultation history
@app.route('/user/consultations', methods=['GET'])
@token_required
def get_user_consultations(current_user):
    try:
        # Fetch consultations with expert information
        consultations = supabase.table('consultations').select(
            '*, experts(name)'
        ).eq('user_id', current_user.id).execute()
        
        # Fetch user info
        user_info = supabase.table('users').select(
            'username, email, created_at'
        ).eq('id', current_user.id).single().execute()
        
        return jsonify({
            'history': consultations.data,
            'user_info': user_info.data
        }), 200
    except Exception as e:
        print(f"Error fetching consultations: {str(e)}")
        return jsonify({'message': 'Failed to fetch consultation history'}), 500

# Route for skincare concerns submission
@app.route('/submit-skincare-concerns', methods=['POST'])
@token_required
def submit_skincare_concerns(current_user):
    try:
        data = request.get_json()
        consultation = supabase.table('consultations').insert({
            'user_id': current_user.id,
            'concerns': data['concerns'],
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat()
        }).execute()
        
        return jsonify({"message": "Skincare concerns submitted successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to submit concerns: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
