
import secrets
from datetime import datetime, timedelta

from config import Config
from models.db import query, execute
from services import mock_data


def create_session(class_id, lat, lng, radius_m=None,
                   refresh_s=None, duration_min=10):
    """
    Create an attendance session.
    Returns the new session ID.
    """

    if Config.USE_MOCK:
        return 1

    radius_m = (
        radius_m if radius_m is not None
        else Config.DEFAULT_GEOFENCE_METERS
    )

    refresh_s = (
        refresh_s if refresh_s is not None
        else Config.QR_REFRESH_SECONDS
    )

    now = datetime.now()
    ends_at = now + timedelta(minutes=duration_min)

    session_id = execute(
        "INSERT INTO sessions "
        "(class_id, lat, lng, radius_m, refresh_s, "
        "started_at, ends_at, status) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, 'active')",
        (
            class_id,
            lat,
            lng,
            radius_m,
            refresh_s,
            now,
            ends_at
        )
    )

    return session_id


def get_current_token(session_id):
    """
    Return the currently valid QR token.
    Generate a new token when the previous one expires.
    """

    if Config.USE_MOCK:
        return mock_data.current_token(
            session_id,
            Config.QR_REFRESH_SECONDS
        )

    now = datetime.now()

    session = query(
        "SELECT * FROM sessions WHERE id = %s",
        (session_id,),
        one=True
    )

    if (
        session is None
        or session["status"] != "active"
        or now > session["ends_at"]
    ):
        return {"token": None, "expires_in": 0}

    latest = query(
        "SELECT token, expires_at FROM qr_tokens "
        "WHERE session_id = %s AND expires_at > %s "
        "ORDER BY id DESC LIMIT 1",
        (session_id, now),
        one=True
    )

    if latest is None:
        token = secrets.token_urlsafe(16)
        expires_at = min(
            now + timedelta(seconds=session["refresh_s"]),
            session["ends_at"]
        )

        execute(
            "INSERT INTO qr_tokens "
            "(session_id, token, issued_at, expires_at) "
            "VALUES (%s, %s, %s, %s)",
            (session_id, token, now, expires_at)
        )

        latest = {
            "token": token,
            "expires_at": expires_at
        }

    seconds_left = int(
        (latest["expires_at"] - now).total_seconds()
    )

    return {
        "token": latest["token"],
        "expires_in": max(0, seconds_left)
    }


def end_session(session_id):
    """
    End an active attendance session.
    """

    if Config.USE_MOCK:
        return None

    execute(
        "UPDATE sessions SET status = 'ended' "
        "WHERE id = %s",
        (session_id,)
    )
