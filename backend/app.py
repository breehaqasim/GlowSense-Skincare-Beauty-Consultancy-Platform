from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from supabase_client import supabase
import jwt
from datetime import datetime, timedelta
from functools import wraps
import re
import requests
from sqlalchemy import text

app = Flask(__name__)
# Configure CORS to allow requests from the frontend
CORS(app, resources={r"/*": {"origins": "*"}})

# Load configuration
app.config.from_object(Config)

# Add this near your other configuration
ABSTRACT_API_KEY = '87446ea44b434e9686adde88f110730d'  # Abstract API key for email validation
ABSTRACT_API_KEY_EMAIL = '87446ea44b434e9686adde88f110730d'  # Email validation
ABSTRACT_API_KEY_PHONE = 'b4292cb0ff264a9dabd90dc00828a301'  # Phone validation

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            # Extract token from Bearer format
            token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else auth_header
            
            # Verify token with Supabase
            user_response = supabase.auth.get_user(token)
            # Extract the user data from the response
            user = user_response.user
            return f(user, *args, **kwargs)
        except IndexError:
            return jsonify({'message': 'Invalid token format'}), 401
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
                expert:expert_id (
                    name,
                    specialization,
                    email
                ),
                selected_expert:selected_expert_id (
                    name,
                    specialization,
                    email
                )
            ''')\
            .eq('user_id', current_user.id)\
            .order('created_at', desc=True)\
            .execute()
        
        print(f"Raw consultation data: {consultations.data}")  # Debug log
        
        # Fetch user info
        user_info = supabase.table('users')\
            .select('username, email, created_at')\
            .eq('id', current_user.id)\
            .single()\
            .execute()
        
        # Format the response
        formatted_consultations = []
        for consultation in consultations.data:
            expert_info = consultation.get('expert', {})
            selected_expert_info = consultation.get('selected_expert', {})
            
            print(f"Processing consultation: {consultation.get('id')}")  # Debug log
            print(f"Expert info: {expert_info}")  # Debug log
            print(f"Selected expert info: {selected_expert_info}")  # Debug log
            
            formatted_consultations.append({
                'id': consultation.get('id'),
                'concerns': consultation.get('concerns'),
                'status': consultation.get('status'),
                'created_at': consultation.get('created_at'),
                'scheduled_time': consultation.get('scheduled_time'),
                'consultation_type': consultation.get('consultation_type'),
                'expert': {
                    'name': expert_info.get('name') if expert_info else None,
                    'specialization': expert_info.get('specialization') if expert_info else None,
                    'email': expert_info.get('email') if expert_info else None
                } if expert_info else None,
                'selected_expert': {
                    'name': selected_expert_info.get('name') if selected_expert_info else None,
                    'specialization': selected_expert_info.get('specialization') if selected_expert_info else None,
                    'email': selected_expert_info.get('email') if selected_expert_info else None
                } if selected_expert_info else None
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
        print("\n=== Starting Expert Matching Process ===")
        print(f"User ID: {current_user.id}")
        
        # Get the user's latest consultation
        latest_consultation = supabase.table('consultations')\
            .select('concerns')\
            .eq('user_id', current_user.id)\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
            
        print(f"\nLatest consultation data: {latest_consultation.data}")
        
        inquiry_type = None
        if latest_consultation.data:
            concerns_text = latest_consultation.data[0].get('concerns', '')
            print(f"\nRaw concerns text: {concerns_text}")
            
            # New extraction logic
            if 'Type:' in concerns_text:
                # Extract everything between "Type:" and "Details:"
                inquiry_type = concerns_text.split('Type:')[1].split('Details:')[0].strip().lower()
            elif ':' in concerns_text:
                # Fallback to old logic if format is different
                inquiry_type = concerns_text.split(':')[0].strip().lower()
            else:
                inquiry_type = 'other'
                
            # Remove the word 'type' if it was accidentally included
            if inquiry_type.startswith('type'):
                inquiry_type = inquiry_type.split('type:')[-1].strip()
        
        print(f"\nExtracted inquiry type: {inquiry_type}")
        
        # Query experts based on specialization matching inquiry type
        if inquiry_type and inquiry_type != 'other':
            try:
                print(f"\nFetching all experts from database...")
                # Get all experts
                experts = supabase.table('experts')\
                    .select('id, name, email, specialization, bio, experience, consultation_price')\
                    .execute()
                
                print(f"\nTotal experts in database: {len(experts.data)}")
                
                # Filter experts whose specialization matches the inquiry type
                matched_experts = []
                print("\nMatching process:")
                for expert in experts.data:
                    print(f"\nChecking expert: {expert['name']}")
                    print(f"Expert specialization: {expert['specialization']}")
                    specializations = [s.strip().lower() for s in expert['specialization'].split(',')]
                    print(f"Parsed specializations: {specializations}")
                    print(f"Comparing with inquiry type: '{inquiry_type}'")
                    
                    if any(s == inquiry_type for s in specializations):
                        print(f"✓ MATCH FOUND: {expert['name']}")
                        matched_experts.append(expert)
                    else:
                        print(f"✗ NO MATCH: Specializations don't match inquiry type")
                
                print(f"\nTotal matches found: {len(matched_experts)}")
                if matched_experts:
                    print("\nMatched experts:")
                    for expert in matched_experts:
                        print(f"- {expert['name']} ({expert['specialization']})")
                
                print("\n=== Expert Matching Process Complete ===")
                return jsonify({
                    'experts': matched_experts
                }), 200
                
            except Exception as e:
                print(f"\nError in expert matching: {str(e)}")
                return jsonify({
                    'message': 'Failed to fetch experts',
                    'error': str(e)
                }), 500
        else:
            print("\nNo valid inquiry type found - returning all experts")
            experts = supabase.table('experts')\
                .select('id, name, email, specialization, bio, experience, consultation_price')\
                .execute()
            
            return jsonify({
                'experts': experts.data
            }), 200
    except Exception as e:
        print(f"\nGlobal error in get_matched_experts: {str(e)}")
        return jsonify({
            'message': 'Failed to process expert matching',
            'error': str(e)
        }), 500

def generate_time_slots(start_time, end_time, duration_minutes=30):
    """Generate time slots between start and end time with given duration."""
    slots = []
    current = datetime.strptime(start_time, '%H:%M:%S')
    end = datetime.strptime(end_time, '%H:%M:%S')
    
    while current < end:
        slot_end = current + timedelta(minutes=duration_minutes)
        if slot_end <= end:
            slots.append({
                'start': current.strftime('%H:%M'),
                'end': slot_end.strftime('%H:%M')
            })
        current = slot_end
    
    return slots

@app.route('/check-slot-availability', methods=['GET'])
def check_slot_availability():
    try:
        expert_id = request.args.get('expert_id')
        date_str = request.args.get('date')
        
        if not expert_id or not date_str:
            return jsonify({'error': 'Missing expert_id or date parameter'}), 400
            
        # Parse the date to get day of week (0 = Monday, 6 = Sunday)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.weekday() + 1  # Convert to 1-7 format
        
        print(f"Checking availability for expert {expert_id} on date {date_str} (day of week: {day_of_week})")
        
        # Get the expert's time slots for this day
        result = supabase.table('expert_time_slots')\
            .select('start_time, end_time, slot_duration')\
            .eq('expert_id', expert_id)\
            .eq('day_of_week', day_of_week)\
            .eq('is_available', True)\
            .execute()
        
        print(f"Expert time slots result: {result.data}")
        
        if not result.data:
            print("No time slots found for this day")
            return jsonify({'available_slots': []}), 200
            
        # Generate all possible time slots for this time range
        all_slots = generate_time_slots(
            result.data[0]['start_time'],
            result.data[0]['end_time'],
            30  # Fixed 30-minute duration
        )
        
        print(f"Generated slots: {all_slots}")
        
        # Get booked slots for this expert on this date
        booked_slots = supabase.table('booked_slots')\
            .select('time_slot')\
            .eq('expert_id', expert_id)\
            .eq('consultation_date', date_str)\
            .execute()
        
        print(f"Booked slots: {booked_slots.data}")
        
        # Convert booked slots to set of start times for easy comparison
        booked_times = {slot['time_slot'] for slot in booked_slots.data} if booked_slots.data else set()
        
        print(f"Booked times: {booked_times}")
        
        # Filter out booked slots
        available_slots = [
            slot for slot in all_slots 
            if slot['start'] not in booked_times
        ]
        
        print(f"Available slots after filtering: {available_slots}")
        
        return jsonify({
            'available_slots': available_slots
        }), 200
        
    except Exception as e:
        print(f"Error checking slot availability: {str(e)}")
        print(f"Full error details:", e)
        return jsonify({'error': 'Internal server error'}), 500

# Route for booking consultation
@app.route('/book-consultation', methods=['POST'])
@token_required
def book_consultation(current_user):
    try:
        data = request.get_json()
        print(f"\n=== Starting Consultation Booking ===")
        print(f"Received data: {data}")
        print(f"Expert ID: {data.get('expert_id')}")
        
        # Verify the slot is within expert's available time slots
        date_obj = datetime.strptime(data.get('consultation_date'), '%Y-%m-%d')
        day_of_week = date_obj.weekday()
        if day_of_week == 6:  # Convert Sunday from 6 to 0
            day_of_week = 0
        
        time_obj = datetime.strptime(data.get('consultation_time'), '%H:%M').time()
        print(f"Parsed date: {date_obj}, time: {time_obj}")
        
        # Check if the slot is in expert's schedule
        expert_slot = supabase.table('expert_time_slots')\
            .select('*')\
            .eq('expert_id', data.get('expert_id'))\
            .eq('day_of_week', day_of_week)\
            .eq('is_available', True)\
            .execute()
            
        print(f"Expert slot check result: {expert_slot.data}")
            
        if not expert_slot.data:
            return jsonify({
                "message": "This time slot is not in the expert's schedule."
            }), 400
            
        slot_valid = False
        for slot in expert_slot.data:
            start = datetime.strptime(slot['start_time'], '%H:%M:%S').time()
            end = datetime.strptime(slot['end_time'], '%H:%M:%S').time()
            if start <= time_obj <= end:
                slot_valid = True
                break
                
        if not slot_valid:
            return jsonify({
                "message": "Selected time is outside expert's available hours."
            }), 400
        
        # Check if the slot is already booked
        check_slot = supabase.table('booked_slots')\
            .select('id')\
            .eq('expert_id', data.get('expert_id'))\
            .eq('consultation_date', data.get('consultation_date'))\
            .eq('time_slot', data.get('consultation_time'))\
            .execute()
            
        print(f"Slot availability check result: {check_slot.data}")
            
        if check_slot.data:
            return jsonify({
                "message": "This time slot is no longer available. Please select another slot."
            }), 409
        
        # Create booked slot record
        slot_data = {
            'expert_id': data.get('expert_id'),
            'consultation_date': data.get('consultation_date'),
            'time_slot': data.get('consultation_time'),
            'user_id': current_user.id
        }
        
        print(f"Creating booked slot with data: {slot_data}")
        
        # Insert into booked_slots table
        slot_result = supabase.table('booked_slots').insert(slot_data).execute()
        
        print(f"Booked slot creation result: {slot_result.data}")
        
        if not slot_result.data:
            return jsonify({"message": "Failed to book time slot"}), 500
        
        # Get the latest consultation for this user
        latest_consultation = supabase.table('consultations')\
            .select('id')\
            .eq('user_id', current_user.id)\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
            
        print(f"Latest consultation query result: {latest_consultation.data}")
            
        if not latest_consultation.data:
            return jsonify({"message": "No consultation found to update"}), 404
            
        consultation_id = latest_consultation.data[0]['id']
        
        # Update the existing consultation record
        consultation_data = {
            'selected_expert_id': data.get('expert_id'),
            'status': 'scheduled',
            'scheduled_time': f"{data.get('consultation_date')} {data.get('consultation_time')}",
            'consultation_type': data.get('consultation_type'),
            'patient_name': data.get('patient_name'),
            'patient_email': data.get('patient_email'),
            'patient_phone': data.get('patient_phone'),
            'patient_age': data.get('patient_age'),
            'patient_gender': data.get('patient_gender')
        }
        
        print(f"Updating consultation with data: {consultation_data}")
        
        # Update the consultation
        result = supabase.table('consultations')\
            .update(consultation_data)\
            .eq('id', consultation_id)\
            .execute()
        
        print(f"Consultation update result: {result.data}")
        print("=== Consultation Booking Complete ===\n")
        
        if not result.data:
            # If consultation update fails, delete the booked slot
            supabase.table('booked_slots').delete().eq('id', slot_result.data[0]['id']).execute()
            return jsonify({"message": "Failed to update consultation"}), 500
            
        return jsonify({
            "message": "Consultation booked successfully",
            "consultation_id": consultation_id
        }), 200
        
    except Exception as e:
        print(f"Error booking consultation: {str(e)}")
        return jsonify({"message": f"Failed to book consultation: {str(e)}"}), 500

# Route for validating consultation form fields
@app.route('/validate-consultation-fields', methods=['POST'])
def validate_consultation_fields():
    try:
        data = request.get_json()
        errors = {}
        
        # Validate name (letters and spaces only)
        name = data.get('patient_name', '').strip()
        if not name:
            errors['name'] = 'Name is required'
        elif not all(c.isalpha() or c.isspace() for c in name):
            errors['name'] = 'Name should contain only letters and spaces'
            
        # Validate email
        email = data.get('patient_email', '').strip()
        if not email:
            errors['email'] = 'Email is required'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors['email'] = 'Please enter a valid email address'
            
        # Validate phone (numbers only, 10-15 digits)
        phone = data.get('patient_phone', '').strip()
        if not phone:
            errors['phone'] = 'Phone number is required'
        elif not re.match(r'^\d{10,15}$', phone):
            errors['phone'] = 'Phone number should be between 10-15 digits'
            
        # Validate age (positive number between 0-150)
        age = data.get('patient_age')
        try:
            age = int(age)
            if age < 0 or age > 150:
                errors['age'] = 'Age should be between 0 and 150'
        except (ValueError, TypeError):
            errors['age'] = 'Please enter a valid age'
            
        # Validate gender
        gender = data.get('patient_gender')
        if not gender or gender not in ['male', 'female', 'other']:
            errors['gender'] = 'Please select a valid gender'
            
        if errors:
            return jsonify({
                'valid': False,
                'errors': errors
            }), 400
            
        return jsonify({
            'valid': True
        }), 200
        
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return jsonify({
            'valid': False,
            'errors': {'general': 'Validation failed. Please try again.'}
        }), 500

# Add new endpoint for email validation
@app.route('/validate-email', methods=['POST'])
def validate_email():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({
                'valid': False,
                'error': 'Email is required'
            }), 400
            
        # Standard email validation regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Check if email matches the pattern
        is_valid = bool(re.match(email_regex, email))
        
        return jsonify({
            'valid': is_valid,
            'details': {
                'message': 'Email format is valid' if is_valid else 'Please enter a valid email address'
            }
        })
            
    except Exception as e:
        print(f"Email validation error: {str(e)}")
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 500

# Add new endpoint for phone validation
@app.route('/validate-phone', methods=['POST'])
def validate_phone():
    try:
        data = request.get_json()
        phone = data.get('phone')
        
        if not phone:
            return jsonify({
                'valid': False,
                'error': 'Phone number is required'
            }), 400
            
        # Remove any non-digit characters
        phone_digits = ''.join(filter(str.isdigit, phone))
        
        # Check if the phone number has 10-15 digits
        is_valid = 10 <= len(phone_digits) <= 15
        
        # Format the phone number for display
        formatted_number = phone_digits
        if len(phone_digits) == 10:  # Format as: (XXX) XXX-XXXX
            formatted_number = f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}"
        
        return jsonify({
            'valid': is_valid,
            'details': {
                'is_valid': is_valid,
                'formatted_number': formatted_number,
                'message': 'Phone number is valid' if is_valid else 'Phone number should be between 10-15 digits'
            }
        })
            
    except Exception as e:
        print(f"Phone validation error: {str(e)}")
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 500

# Route for forgot password
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        print("\n=== Starting Password Reset Process ===")
        print("Request Headers:", dict(request.headers))
        print("Request Method:", request.method)
        
        data = request.get_json()
        print("Request Data:", data)
        
        email = data.get('email')
        print(f"Processing reset for email: {email}")
        
        if not email:
            print("Error: No email provided")
            return jsonify({'message': 'Email is required'}), 400
            
        print(f"Validating and sending reset email to: {email}")
            
        try:
            print("\nMaking Supabase API call...")
            print("Supabase Configuration:")
            print("- URL:", supabase.supabase_url)
            print("- Using Auth Client:", bool(supabase.auth))
            
            # Use Supabase's reset password email functionality
            result = supabase.auth.reset_password_email(
                email,
                {
                    'redirect_to': 'http://127.0.0.1:5500/frontend/reset-password.html'
                }
            )
            print("\nSupabase API Response:")
            print("- Success:", bool(result))
            print("- Result Data:", result)
            
            return jsonify({
                'message': 'Password reset link has been sent to your email',
                'debug_info': {
                    'email_sent': True,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 200
            
        except Exception as supabase_error:
            print("\nSupabase Error Details:")
            print("- Error Type:", type(supabase_error).__name__)
            print("- Error Message:", str(supabase_error))
            print("- Error Args:", getattr(supabase_error, 'args', []))
            
            error_str = str(supabase_error).lower()
            
            if "user not found" in error_str:
                print("Error: User not found in database")
                return jsonify({
                    'message': 'No account found with this email address',
                    'debug_info': {
                        'error_type': 'USER_NOT_FOUND',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                }), 404
            else:
                print(f"Unexpected Supabase error: {error_str}")
                raise supabase_error
            
    except Exception as e:
        print("\nGlobal Error Details:")
        print("- Error Type:", type(e).__name__)
        print("- Error Message:", str(e))
        print("- Error Args:", getattr(e, 'args', []))
        print("- Stack Trace:", getattr(e, '__traceback__', None))
        
        return jsonify({
            'message': 'An error occurred while processing your request. Please try again later.',
            'debug_info': {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
        }), 500

    finally:
        print("\n=== Password Reset Process Complete ===")
        print("Timestamp:", datetime.utcnow().isoformat())

# Route for resetting password
@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        if not token or not new_password:
            return jsonify({'message': 'Token and new password are required'}), 400
            
        # Use Supabase's password update functionality
        result = supabase.auth.verify_and_update_user(
            token,
            {"password": new_password}
        )
        
        print(f"Password reset result: {result}")  # Debug log
        
        return jsonify({
            'message': 'Password has been reset successfully'
        }), 200
            
    except Exception as e:
        print(f"Error in reset password: {str(e)}")  # Debug log
        return jsonify({
            'message': 'An error occurred while resetting your password'
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
