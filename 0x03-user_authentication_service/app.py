#!/usr/bin/env python3
"""
"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)

@app.route("/", methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET/status
        :
        Return jsonify
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """POST/ User
        Register  new User
        :Return jsonify playload
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

