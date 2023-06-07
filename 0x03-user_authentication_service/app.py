#!/usr/bin/env python3
"""
Route model for webApp
"""
from auth import Auth
from flask import Flask, abort, jsonify, request


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcomeMessage() -> str:
    """Returns a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_users():
    try:
        email = request.form["email"]
        password = request.form["password"]
        user = AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(user.email),
                        "message": "user created"})
    except KeyError:
        abort(400)

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"])
def login_user() -> str:
    """Logs in a user and returns session ID
    """
    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": "{}".format(email),
                        "message": "logged in"})

    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
