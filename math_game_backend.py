from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate_equation():
    data = request.json
    num1 = data.get("num1")
    num2 = data.get("num2")
    result = data.get("result")
    
    if num1 is None or num2 is None or result is None:
        return jsonify({"error": "Missing values"}), 400
    
    try:
        num1 = int(num1)
        num2 = int(num2)
        result = int(result)
    except ValueError:
        return jsonify({"error": "Invalid input"}), 400
    
    if num1 + num2 == result:
        return jsonify({"valid": True, "message": "Correct!"})
    else:
        return jsonify({"valid": False, "message": "Incorrect. Try again!"})

if __name__ == '__main__':
    app.run(debug=True)
