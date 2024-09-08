#!/usr/bin/env python3
"""
SessionDBAuth class that uses UserSession for session management
"""
from api.v2.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class that uses UserSession for session management """

    def __init__(self) -> None:
        """ Initialize SessionDBAuth with session_duration from
        the environment """
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ Create a new session ID and store it in UserSession """

        # Check for valid user_id
        if not user_id or not isinstance(user_id, str):
            print(f"[DEBUG] Invalid user_id provided: {user_id}")
            return None

        # Create session ID using the parent method
        print(f"[DEBUG] Creating session for user_id: {user_id}")
        session_id = super().create_session(user_id)

        if session_id is None:
            print(f"[DEBUG] Failed to create session for user_id: {user_id}")
            return None

        print(f"[DEBUG] Session ID created: {session_id}")

        session_data = {
            'user_id': user_id,
            'session_id': session_id,
            'created_at': datetime.now().strftime(TIMESTAMP_FORMAT),
            'max_age': self.session_duration
        }

        print(f"[DEBUG] Session data to be saved: {session_data}")

        # Create a new UserSession and save it
        try:
            user_session = UserSession(**session_data)
            print(
                f"[DEBUG] UserSession object created: {user_session.to_json()}")
            user_session.save()
            print(f"[DEBUG] UserSession saved successfully")
        except Exception as e:
            print(f"[DEBUG] Error saving UserSession: {str(e)}")
            return None

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve user ID based on session ID from UserSession """
        if not session_id:
            return None
        try:
            # Search for the UserSession based on session_id
            user_session = UserSession.search_db({"session_id": session_id})
        except Exception:
            return None
        if not user_session:
            return None

        user_session = user_session[0]

        # Check session expiration if applicable
        if self.session_duration > 0:
            if (datetime.now() - user_session.created_at)\
                    .total_seconds() > self.session_duration:
                return None

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroy session by removing UserSession entry """

        print(
            f"\n\n[DEBUG DESTROY SESSION] destroy_session called with request: {request}")

        if not request:
            print("[DEBUG DESTROY SESSION] Request is None, cannot proceed")
            return False

        session_id = self.session_cookie(request)
        print(f"[DEBUG DESTROY SESSION] Retrieved session_id: {session_id}")

        if not session_id:
            print("[DEBUG DESTROY SESSION] Session ID is None, cannot proceed")
            return False

        # Find the UserSession by session_id
        user_session = UserSession.search_db({"session_id": session_id})
        print(
            f"[DEBUG DESTROY SESSION] UserSession search result for session_id {session_id}: {user_session}")

        if user_session:
            print(
                f"[DEBUG DESTROY SESSION] UserSession found: {user_session[0]}")
            user_session[0].remove()
            print(
                f"[DEBUG DESTROY SESSION] UserSession with session_id {session_id} has been removed")

            return True

        print(
            f"[DEBUG DESTROY SESSION] No UserSession found with session_id {session_id}, cannot destroy session")
        return False
