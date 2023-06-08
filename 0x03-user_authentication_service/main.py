#!/usr/bin/env python3
"""End-to-end integration test module
"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Validating registration for new User
    """
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post("{}/users".format(BASE_URL), data=payload)

    json_message = {"email": email, "message": "user created"}

    assert (response.status_code == 200)
    assert (response.json() == json_message)


def log_in_wrong_password(email: str, password: str) -> None:
    """Validating login using wrong credential password
    """
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post("{}/sessions".format(BASE_URL), data=payload)

    assert (response.status_code == 401)


def log_in(email: str, password: str) -> str:
    """Validating login using correct credentials
    """
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post("{}/sessions".format(BASE_URL), data=payload)

    json_message = {"email": email, "message": "logged in"}

    assert (response.status_code == 200)
    assert (response.json() == json_message)

    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Validating profile endpoint for users not logged In
    """
    response = requests.get("{}/profile".format(BASE_URL))

    assert (response.status_code == 403)


def profile_logged(session_id: str) -> None:
    """ Validating profile endpoint for logged In users
    """
    cookies = {
        "session_id": session_id
    }
    response = requests.get("{}/profile".format(BASE_URL), cookies=cookies)

    json_message = {"email": EMAIL}

    assert (response.status_code == 200)
    assert (response.json() == json_message)


def log_out(session_id: str) -> None:
    """ Validating LogOut endpoint
    """
    cookies = {
        "session_id": session_id
    }
    response = requests.delete("{}/sessions".format(BASE_URL), cookies=cookies)

    json_message = {"message": "Bienvenue"}

    assert (response.status_code == 200)
    assert (response.json() == json_message)


def reset_password_token(email: str) -> str:
    """Validating password reset token endpoint
    """
    payload = {
        "email": email
    }
    response = requests.post("{}/reset_password".format(BASE_URL),
                             data=payload)

    token = response.json().get("reset_token")
    json_message = {"email": email, "reset_token": token}

    assert (response.status_code == 200)
    assert (response.json() == json_message)

    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Validating password update endpoint
    """
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put("{}/reset_password".format(BASE_URL), data=payload)

    json_message = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == json_message


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
