
"""Login checks. OWNER: Mrunal Kale.
While USE_MOCK=true it accepts three fake logins (F001, S001, A001, password demo123),
so the real login page works before the database exists.
"""

import time

from config import Config
from services.mock_data import MOCK_USERS

MAX_FAILS = 5
LOCK_SECONDS = 300

MOCK_ROLES = {
    "F001": "faculty",
    "S001": "student",
    "A001": "admin"
}

_failures = {}


def _is_locked(user_code):
    record = _failures.get(user_code)

    if record is None:
        return False

    count, last = record

    if time.time() - last >= LOCK_SECONDS:
        _failures.pop(user_code, None)
        return False

    return count >= MAX_FAILS


def _record_failure(user_code):
    count, _ = _failures.get(user_code, (0, 0))
    _failures[user_code] = (count + 1, time.time())


def _find_user(user_code, password):
    """Return user details if ID and password are correct."""

    if Config.USE_MOCK:
        role = MOCK_ROLES.get(user_code)

        if role and password == "demo123":
            return dict(MOCK_USERS[role])

        return None

    import bcrypt
    from models.db import query

    row = query(
        "SELECT id, name, role, password_hash FROM users WHERE user_code = %s AND active = 1",
        (user_code,),
        one=True,
    )

    if row is None:
        return None

    if not bcrypt.checkpw(
        password.encode(),
        row["password_hash"].encode()
    ):
        return None

    return {
        "id": row["id"],
        "name": row["name"],
        "role": row["role"]
    }


def authenticate(user_code, password):
    """Return login success or error."""

    if _is_locked(user_code):
        return {
            "ok": False,
            "error": "Too many failed attempts. Try again in a few minutes."
        }

    user = _find_user(user_code, password)

    if user is None:
        _record_failure(user_code)
        return {
            "ok": False,
            "error": "Wrong ID or password"
        }

    _failures.pop(user_code, None)

    return {
        "ok": True,
        "user": user
    }


def list_users():
    """Return users without exposing password hashes."""

    if Config.USE_MOCK:
        return [
            {
                "user_code": code,
                "name": MOCK_USERS[role]["name"],
                "role": role,
                "division": None,
                "active": 1
            }
            for code, role in MOCK_ROLES.items()
        ]

    from models.db import query

    return query(
        "SELECT user_code, name, role, division, active FROM users ORDER BY role, user_code"
    )
