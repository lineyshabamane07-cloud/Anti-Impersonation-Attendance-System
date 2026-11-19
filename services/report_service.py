# OWNER: Lineysha Bamane   (callers: Tanmai's live list + report, Mrunal's admin pages)
from config import Config
from services import mock_data


def list_marked(session_id):
    """Students marked so far in this session.
    Returns: [{"student_id", "name", "status", "distance_m", "marked_at"}]"""
    if Config.USE_MOCK:
        return mock_data.marked_list(session_id)
    raise NotImplementedError("Lineysha: JOIN attendance + users")


def session_summary(session_id):
    """Returns: {"session_id","subject","division","room","total_students","present","flagged","rejected"}"""
    if Config.USE_MOCK:
        return mock_data.session_summary(session_id)
    raise NotImplementedError("Lineysha: counts from attendance/attempts")


def list_attempts(only_problems=True):
    """Audit rows for the admin page. Returns: [{"created_at","student","outcome","reason","distance_m"}]"""
    if Config.USE_MOCK:
        return [{"created_at": "10:03:02", "student": "Demo Student", "outcome": "rejected",
                 "reason": "QR expired – scan the latest code", "distance_m": 12.0},
                {"created_at": "10:04:40", "student": "Demo Student 2", "outcome": "flagged",
                 "reason": "Borderline location", "distance_m": 96.0}]
    raise NotImplementedError("Lineysha: SELECT from attempts")
