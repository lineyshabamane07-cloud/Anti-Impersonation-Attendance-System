"""Fake data used while USE_MOCK=true. Lets Tanmai, Reet and Mrunal build and
demo their pages with NO dependency on Lineysha's real code or the database."""
import time

MOCK_USERS = {
    "faculty": {"id": 1, "name": "Dr. Demo Faculty", "role": "faculty"},
    "student": {"id": 101, "name": "Demo Student", "role": "student"},
    "admin":   {"id": 900, "name": "Demo Admin", "role": "admin"},
}

_STUDENTS = ["Reet Lunkad", "Lineysha Bamane", "Mrunal Kale", "Krishna Panjwani",
             "Tanmai Divekar", "Aarav Shah", "Isha Patil", "Rohan Mehta"]


def current_token(session_id, refresh_s=20):
    bucket = int(time.time() // refresh_s)
    return {"token": f"MOCK-{session_id}-{bucket}",
            "expires_in": refresh_s - int(time.time() % refresh_s)}


def mark_result(token):
    """Pick the outcome from the end of the token so Reet can test every screen:
    ...-expired  ...-far  ...-dup  ...-device  ...-flag   (anything else = success)"""
    t = (token or "").lower()
    if t.endswith("-expired"):
        return {"status": "rejected", "reason": "QR expired – scan the latest code", "distance_m": 12.0}
    if t.endswith("-far"):
        return {"status": "rejected", "reason": "You are outside the classroom area", "distance_m": 480.0}
    if t.endswith("-dup"):
        return {"status": "rejected", "reason": "Attendance already marked", "distance_m": 8.0}
    if t.endswith("-device"):
        return {"status": "rejected", "reason": "Unregistered device", "distance_m": 10.0}
    if t.endswith("-flag"):
        return {"status": "flagged", "reason": "Borderline location – sent for faculty review", "distance_m": 96.0}
    return {"status": "present", "reason": "Attendance marked", "distance_m": 14.0}


def marked_list(session_id):
    """Grows by one name every ~4 seconds so the live list visibly updates."""
    n = min(len(_STUDENTS), int(time.time() // 4) % (len(_STUDENTS) + 1))
    return [{"student_id": 100 + i, "name": _STUDENTS[i], "status": "present",
             "distance_m": 10 + 3 * i, "marked_at": "10:0%d:1%d" % (i % 10, i % 10)} for i in range(n)]


def session_summary(session_id):
    return {"session_id": session_id, "subject": "DAA", "division": "SY-B", "room": "304",
            "total_students": 60, "present": 38, "flagged": 2, "rejected": 5}
