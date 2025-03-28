from flask import Flask, request, jsonify
from models import db, User, Expert, Consultation

app = Flask(__name__)

# Route for home page
@app.route('/')
def home():
    return "Welcome to Glow Sense Skincare & Beauty Consultancy Platform"

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Here you would add logic for saving the user into the database
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Route for skincare concerns submission
@app.route('/submit-skincare-concerns', methods=['POST'])
def submit_skincare_concerns():
    data = request.get_json()
    new_concern = Consultation(user_id=data['user_id'], concerns=data['concerns'])
    db.session.add(new_concern)
    db.session.commit()
    return jsonify({"message": "Skincare concerns submitted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
