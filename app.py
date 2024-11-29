from flask import Flask, request, jsonify

import db
from db import check_connection
from generator import get_analysis

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Welcome to the Phishing Detection API!"


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "email_text" not in data:
        return jsonify({"error": "email_text field is required"}), 400

    email_text = data["email_text"]

    return get_analysis(email_text)


if __name__ == '__main__':
    db.check_connection()
    app.run("0.0.0.0", port=80, debug=True)
