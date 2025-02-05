import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create the Flask app instance
app = Flask(__name__)

# Enable CORS to allow your frontend to communicate with the backend
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (for testing purposes)

# Route for testing the backend
@app.route('/hello', methods=['GET'])
def hello_world():
    # Respond with a simple hello message
    response = jsonify({"message": "Hello, world!"})
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow cross-origin requests
    return response

# Route to validate math equations submitted via the frontend
@app.route('/validate', methods=['POST'])
def validate_equation():
    # Get the data from the request (expected to be in JSON format)
    data = request.json
    num1 = data.get("num1")
    num2 = data.get("num2")
    result = data.get("result")
    
    # Check if any values are missing
    if num1 is None or num2 is None or result is None:
        return jsonify({"error": "Missing values"}), 400
    
    # Try to convert the values to integers, and handle errors
    try:
        num1 = int(num1)
        num2 = int(num2)
        result = int(result)
    except ValueError:
        return jsonify({"error": "Invalid input"}), 400
    
    # Validate if the sum of num1 and num2 equals the result
    if num1 + num2 == result:
        return jsonify({"valid": True, "message": "Correct!"})
    else:
        return jsonify({"valid": False, "message": "Incorrect. Try again!"})

# Start the Flask app when this file is run directly
if __name__ == '__main__':
    # Get the port from the environment variable (use 10000 as default for Render)
    port = int(os.environ.get("PORT", 10000))
    # Run the Flask app on all available network interfaces
    app.run(host="0.0.0.0", port=port)
