# OWNER: Lineysha Bamane   (callers: Tanmai's faculty routes)
# The function names, arguments and return shapes below are FROZEN (docs/CONTRACT.md).
# While USE_MOCK=true they return fake data. Replace each NotImplementedError with real code.
from config import Config
from services import mock_data


def create_session(class_id, lat, lng, radius_m=None, refresh_s=None, duration_min=10):
    """Create an attendance session. Returns: session_id (int)."""
    if Config.USE_MOCK:
        return 1
    raise NotImplementedError("Lineysha: INSERT into sessions, return new id")


def get_current_token(session_id):
    """Return the currently valid QR token, rotating it if expired.
    Returns: {"token": str, "expires_in": int_seconds}"""
    if Config.USE_MOCK:
        return mock_data.current_token(session_id, Config.QR_REFRESH_SECONDS)
    raise NotImplementedError("Lineysha: secrets.token_urlsafe + qr_tokens table")


def end_session(session_id):
    """Mark the session ended. Returns: None"""
    if Config.USE_MOCK:
        return None
    raise NotImplementedError("Lineysha: UPDATE sessions SET status='ended'")
