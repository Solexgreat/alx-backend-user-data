#!/usr/bin/env python3
"""Route module for the API
"""
from flask import Flask, jsonify, request, abort, redirect
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

    # Get data from form request, change to request.get_json() for body
    email = request.form.get('email')
    password = request.form.get('password')


    try:
        user = AUTH.register_user(email, password)
        if user is not None:
            return jsonify(
                {"email": user.email, 
                 "message": "user created"
                 })
    except ValueError:
        return jsonify({"message": 
                        "email already registered"}), 400
