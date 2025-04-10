from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Expert, Consultation
from config import Config
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
# Configure CORS to allow requests from the frontend
CORS(app, resources={r"/*": {"origins": "*"}})

# Load configuration
app.config.from_object(Config)

# Initialize database
db.init_app(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
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
        print("Received registration data:", data)  # Debug log
        
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            print("Missing required fields")  # Debug log
            return jsonify({'message': 'Missing required fields'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            print("Email already exists")  # Debug log
            return jsonify({'message': 'Email already registered'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            print("Username already exists")  # Debug log
            return jsonify({'message': 'Username already taken'}), 400
        
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        print("User registered successfully")  # Debug log
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        print("Registration error:", str(e))  # Debug log
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

# Route to get user's consultation history
@app.route('/user/consultations', methods=['GET'])
@token_required
def get_user_consultations(current_user):
    try:
        # Fetch consultations and join with Expert table
        consultations = db.session.query(
            Consultation, Expert.name
        ).outerjoin(
            Expert, Consultation.expert_id == Expert.id
        ).filter(
            Consultation.user_id == current_user.id
        ).order_by(
            Consultation.created_at.desc()
        ).all()

        history = []
        for consult, expert_name in consultations:
            history.append({
                'id': consult.id,
                'concerns': consult.concerns,
                'status': consult.status,
                'created_at': consult.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'scheduled_time': consult.scheduled_time.strftime('%Y-%m-%d %H:%M:%S') if consult.scheduled_time else None,
                'expert_name': expert_name # Add expert name
            })

        # Prepare user info
        user_info = {
            'username': current_user.username,
            'email': current_user.email,
            'member_since': current_user.created_at.strftime('%B %Y') # Format join date
        }

        # Return both history and user info
        return jsonify({'history': history, 'user_info': user_info}), 200
    except Exception as e:
        print(f"Error fetching consultations for user {current_user.id}: {str(e)}")
        return jsonify({'message': 'Failed to fetch consultation history'}), 500

# Route for skincare concerns submission
@app.route('/submit-skincare-concerns', methods=['POST'])
@token_required
def submit_skincare_concerns(current_user):
    data = request.get_json()
    new_concern = Consultation(
        user_id=current_user.id,
        concerns=data['concerns']
    )
    db.session.add(new_concern)
    db.session.commit()
    return jsonify({"message": "Skincare concerns submitted successfully"}), 200

# Create tables before running the app
def init_db():
    with app.app_context():
        # Drop all tables (for development)
        db.drop_all()
        print("Existing database tables dropped.")
        # Create all database tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()  # Initialize database tables
    app.run(debug=True)
