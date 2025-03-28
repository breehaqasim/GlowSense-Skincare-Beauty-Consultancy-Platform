from flask import Flask, request, jsonify

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return "Welcome to Glow Sense Skincare & Beauty Consultancy Platform"

# Route for user registration (Skeleton route)
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Here, you'd implement user registration logic (e.g., saving to DB)
    return jsonify({"message": "User registered successfully"}), 201

# Route for submitting skincare concerns (Skeleton route)
@app.route('/submit-skincare-concerns', methods=['POST'])
def submit_skincare_concerns():
    data = request.get_json()
    # Implement the logic to handle skincare concerns submission
    return jsonify({"message": "Skincare concerns submitted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)

