#!/usr/bin/env python3
"""
Implementation Session authentication views Module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handle user login
    method: POST [/auth_session/login]
    Return
        - Logged in user
    Else:
        - error message found
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
        if not users:
            return jsonify({"error": "no user found for this email"}), 404
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):

            from api.v1.app import auth

            session_id = auth.create_session(user.id)

            SESSION_NAME = getenv("SESSION_NAME")

            response = jsonify(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)

            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Handle user logout
    method:DELETE [/auth_session/logout]
    Return:
        - Empty dictionary if succesful
    Else:
        - error message found
    """
    from api.v1.app import auth

    destroyed_session = auth.destroy_session(request)
    if not destroyed_session:
        abort(404)

    return jsonify({}), 200
