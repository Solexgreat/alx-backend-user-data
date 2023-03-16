#!/usr/bin/env python3
"""
"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)

@app.route("/", method='GET')
def welcome():
    """
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', method='POST')
def register_user():
    """Register User
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({f"email {email}, message: user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
