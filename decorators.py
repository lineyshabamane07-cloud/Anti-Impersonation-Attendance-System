from functools import wraps

from flask import abort, redirect, session, url_for


def role_required(*roles):
    """Only logged-in users with one of the given roles may open the page.
    Anonymous users go to the login page. Wrong role gets 403 Forbidden."""
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = session.get("user")
            if user is None:
                return redirect(url_for("auth.login"))
            if user.get("role") not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator