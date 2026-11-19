# OWNER: Lineysha Bamane   (callers: Reet's POST /student/mark)
from config import Config
from services import mock_data


def mark_attendance(token, student_id, lat, lng, device_id):
    """Run all checks (token valid+unexpired -> enrolled -> not already marked ->
    device matches/binds -> inside geofence), write attendance + attempts rows.
    Returns: {"status": "present"|"rejected"|"flagged", "reason": str, "distance_m": float}"""
    if Config.USE_MOCK:
        return mock_data.mark_result(token)
    raise NotImplementedError("Lineysha: implement verification chain")
