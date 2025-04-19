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
            user_response = supabase.auth.get_user(token)
            # Extract the user data from the response
            user = user_response.user
            return f(user, *args, **kwargs)
        except Exception as e:
            print(f"Token verification error: {str(e)}")
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
        
        # Fetch username from users table
        user_data = supabase.table('users').select('username').eq('id', user.id).single().execute()
        username = user_data.data.get('username') if user_data.data else user.email
        
        print(f"Login successful for user: {user.email}")  # Debug log
        
        return jsonify({
            'token': session.access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': username
            }
        })
    except Exception as e:
        print(f"Login error details: {str(e)}")  # Detailed error log
        return jsonify({'message': 'Invalid email or password'}), 401

# Route to get user's consultation history with expert details
@app.route('/user/consultations', methods=['GET'])
@token_required
def get_user_consultations(current_user):
    try:
        print(f"Fetching consultations for user: {current_user.id}")  # Debug log
        
        # Fetch consultations with expert information using the new schema
        consultations = supabase.table('consultations')\
            .select('''
                *,
                experts (
                    name,
                    specialization,
                    email
                )
            ''')\
            .eq('user_id', current_user.id)\
            .order('created_at', desc=True)\
            .execute()
        
        # Fetch user info
        user_info = supabase.table('users')\
            .select('username, email, created_at')\
            .eq('id', current_user.id)\
            .single()\
            .execute()
        
        # Format the response
        formatted_consultations = []
        for consultation in consultations.data:
            expert_info = consultation.get('experts', {})
            formatted_consultations.append({
                'id': consultation.get('id'),
                'concerns': consultation.get('concerns'),
                'status': consultation.get('status'),
                'created_at': consultation.get('created_at'),
                'scheduled_time': consultation.get('scheduled_time'),
                'expert': {
                    'name': expert_info.get('name') if expert_info else None,
                    'specialization': expert_info.get('specialization') if expert_info else None,
                    'email': expert_info.get('email') if expert_info else None
                } if expert_info else None
            })
        
        return jsonify({
            'consultations': formatted_consultations,
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
        
        # Extract the inquiry type and concerns from the combined concerns string
        concerns_text = data.get('concerns', '')
        inquiry_type = concerns_text.split(':')[0].strip() if ':' in concerns_text else 'Other'
        concerns = concerns_text.split(':', 1)[1].strip() if ':' in concerns_text else concerns_text
        
        # Get expert_id from the request
        expert_id = data.get('expert_id')
        
        # Create consultation record with UUID
        consultation_data = {
            'user_id': current_user.id,
            'concerns': f"Type: {inquiry_type}\n\nDetails: {concerns}",
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'scheduled_time': None
        }
        
        # Add expert_id if provided
        if expert_id:
            consultation_data['expert_id'] = expert_id
        
        print(f"Creating consultation for user: {current_user.id}")  # Debug log
        
        # Insert into consultations table
        result = supabase.table('consultations').insert(consultation_data).execute()
        
        if not result.data:
            return jsonify({"message": "Failed to save consultation"}), 500
            
        return jsonify({
            "message": "Skincare concerns submitted successfully",
            "consultation_id": result.data[0]['id'] if result.data else None
        }), 200
        
    except Exception as e:
        print(f"Error submitting concerns: {str(e)}")
        return jsonify({"message": f"Failed to submit concerns: {str(e)}"}), 500

# Route for getting matched experts
@app.route('/get-matched-experts', methods=['GET'])
@token_required
def get_matched_experts(current_user):
    try:
        print("Starting expert matching process...")  # Debug log
        
        # Get the user's latest consultation to check their inquiry type
        latest_consultation = supabase.table('consultations')\
            .select('concerns')\
            .eq('user_id', current_user.id)\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
            
        inquiry_type = None
        if latest_consultation.data:
            concerns_text = latest_consultation.data[0].get('concerns', '')
            if 'Type:' in concerns_text:
                inquiry_type = concerns_text.split('Type:')[1].split('\n')[0].strip().lower()
        
        print(f"Searching for experts with specialization: {inquiry_type}")  # Debug log
        
        # Query experts based on specialization matching inquiry type
        if inquiry_type:
            experts = supabase.table('experts')\
                .select('id, name, email, specialization, bio, experience, consultation_price')\
                .ilike('specialization', f'%{inquiry_type}%')\
                .execute()
        else:
            # If no inquiry type, get all experts
            experts = supabase.table('experts')\
                .select('id, name, email, specialization, bio, experience, consultation_price')\
                .execute()
            
        print(f"Found {len(experts.data)} matching experts")  # Debug log
        
        if not experts.data:
            return jsonify({
                'message': 'No experts found for your specific concerns.',
                'experts': []
            }), 200
            
        return jsonify({
            'experts': experts.data
        }), 200
        
    except Exception as e:
        print(f"Error fetching experts: {str(e)}")
        return jsonify({'message': 'Failed to fetch experts', 'error': str(e)}), 500

# Route for booking consultation
@app.route('/book-consultation', methods=['POST'])
@token_required
def book_consultation(current_user):
    try:
        data = request.get_json()
        
        # Create consultation record
        consultation_data = {
            'user_id': current_user.id,
            'expert_id': data.get('expert_id'),
            'status': 'scheduled',
            'scheduled_time': f"{data.get('consultation_date')} {data.get('consultation_time')}",
            'consultation_type': data.get('consultation_type'),
            'patient_name': data.get('patient_name'),
            'patient_email': data.get('patient_email'),
            'patient_phone': data.get('patient_phone'),
            'patient_age': data.get('patient_age'),
            'patient_gender': data.get('patient_gender'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Insert into consultations table
        result = supabase.table('consultations').insert(consultation_data).execute()
        
        if not result.data:
            return jsonify({"message": "Failed to book consultation"}), 500
            
        return jsonify({
            "message": "Consultation booked successfully",
            "consultation_id": result.data[0]['id'] if result.data else None
        }), 200
        
    except Exception as e:
        print(f"Error booking consultation: {str(e)}")
        return jsonify({"message": f"Failed to book consultation: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
