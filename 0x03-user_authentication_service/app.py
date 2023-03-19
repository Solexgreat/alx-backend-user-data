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


@app.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE session
       find user by session id gotten from cookies
       :Retrun
        -   redirct to status route (GET /)
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET / profile
       :Retrun
       -    use sesion_id to find user
        - 403 if session_id or user is not found
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
        :Return
        -status 403 if email is invalid
    """
    email = request.form.get(email)
    reset_token = AUTH.get_reset_password_token(email)
    if reset_token:
        return jsonify({"email": email, "reset_token": reset_token}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
       :Return
       -status 403 if token is invalid
    """
    email = request.form.get(email)
    new_password = request.form.get(new_password)
    reset_token = request.form.get(reset_token)
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
