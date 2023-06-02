#!/usr/bin/env python3
"""
Implementation of Expiration of Session Authentication Module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Expiration Class"""

    def __init__(self):
        """ Constructor class Method"""

        try:
            SESSION_DURATION = getenv('SESSION_DURATION')
            session_duration = int(SESSION_DURATION)
        except Exception:
            session_duration = 0

        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """create session id for a user"""

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """return user_id using session_id"""

        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None

        user_detail = self.user_id_by_session_id.get(session_id)
        if user_detail is None:
            return None

        if self.session_duration <= 0:
            return user_detail.get("user_id")

        created_at = user_detail.get("created_at")
        if created_at is None:
            return None

        expected_duration = created_at + timedelta(
                seconds=self.session_duration)

        if expected_duration < datetime.now():
            return None

        return user_detail.get("user_id")
