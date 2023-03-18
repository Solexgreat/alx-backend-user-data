#!/usr/bin/env python3
"""Route module for the API
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
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

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Validate the Login info 
       and create a login session
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = AUTH.valid_login(email, password)
    if user:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email,
                        "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else: 
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
