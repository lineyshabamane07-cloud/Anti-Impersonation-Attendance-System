
# OWNER: Lineysha Bamane
# Caller: Reet's POST /student/mark

from datetime import datetime, timedelta

from config import Config
from models.db import query, execute
from services import mock_data
from services.geo_service import haversine_m

GRACE_SECONDS = 3
FLAG_MARGIN_M = 30


def mark_attendance(token, student_id, lat, lng, device_id):
    """
    Verify QR, enrollment, duplicate attendance,
    device binding and geofence.

    Returns:
    {
        "status": "present" | "flagged" | "rejected",
        "reason": str,
        "distance_m": float | None
    }
    """

    if Config.USE_MOCK:
        return mock_data.mark_result(token)

    session_id = None

    def finish(status, reason, distance=None):
        # Record attempts when a session is identifiable.
        if session_id is not None:
            execute(
                "INSERT INTO attempts "
                "(session_id, student_id, outcome, reason, "
                "distance_m, created_at) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    session_id,
                    student_id,
                    status,
                    reason,
                    distance,
                    datetime.now()
                )
            )

        return {
            "status": status,
            "reason": reason,
            "distance_m": distance
        }

    # 1. Validate location
    try:
        lat = float(lat)
        lng = float(lng)

        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            raise ValueError()

    except (TypeError, ValueError):
        return finish(
            "rejected",
            "Invalid or missing location"
        )

    # 2. Validate QR token
    token_row = query(
        "SELECT q.session_id, q.expires_at, "
        "s.class_id, s.lat, s.lng, s.radius_m, "
        "s.ends_at, s.status "
        "FROM qr_tokens q "
        "JOIN sessions s ON s.id = q.session_id "
        "WHERE q.token = %s",
        (token,),
        one=True
    )

    if token_row is None:
        return finish(
            "rejected",
            "Invalid QR token"
        )

    session_id = token_row["session_id"]
    now = datetime.now()

    if token_row["status"] != "active":
        return finish(
            "rejected",
            "Attendance session is not active"
        )

    if now > token_row["ends_at"]:
        return finish(
            "rejected",
            "Attendance session has ended"
        )

    if now > token_row["expires_at"] + timedelta(
        seconds=GRACE_SECONDS
    ):
        return finish(
            "rejected",
            "QR token expired"
        )

    # 3. Check enrollment
    enrolled = query(
        "SELECT student_id FROM enrollments "
        "WHERE class_id = %s AND student_id = %s",
        (token_row["class_id"], student_id),
        one=True
    )

    if enrolled is None:
        return finish(
            "rejected",
            "Student is not enrolled in this class"
        )

    # 4. Check duplicate attendance
    existing = query(
        "SELECT student_id FROM attendance "
        "WHERE session_id = %s AND student_id = %s",
        (session_id, student_id),
        one=True
    )

    if existing is not None:
        return finish(
            "rejected",
            "Attendance already marked"
        )

    # 5. Check device binding
    if not device_id:
        return finish(
            "rejected",
            "Missing device ID"
        )

    device = query(
        "SELECT student_id FROM devices "
        "WHERE device_id = %s",
        (device_id,),
        one=True
    )

    if device is not None:
        if device["student_id"] != student_id:
            return finish(
                "rejected",
                "Device belongs to another student"
            )
    else:
        student_device = query(
            "SELECT device_id FROM devices "
            "WHERE student_id = %s",
            (student_id,),
            one=True
        )

        if student_device is not None:
            return finish(
                "rejected",
                "Student is registered with another device"
            )

        execute(
    "INSERT INTO devices (student_id, device_id, bound_at) "
    "VALUES (%s, %s, %s)",
    (student_id, device_id, datetime.now())
)

    # 6. Calculate geofence distance
    distance = haversine_m(
        token_row["lat"],
        token_row["lng"],
        lat,
        lng
    )

    radius = token_row["radius_m"]

    if distance <= radius:
        status = "present"
        reason = "Attendance marked successfully"

    elif distance <= radius + FLAG_MARGIN_M:
        status = "flagged"
        reason = "Near geofence boundary; review required"

    else:
        return finish(
            "rejected",
            "Outside allowed geofence",
            distance
        )

    # 7. Save attendance
    execute(
        "INSERT INTO attendance "
        "(session_id, student_id, status, distance_m, marked_at) "
        "VALUES (%s, %s, %s, %s, %s)",
        (
            session_id,
            student_id,
            status,
            distance,
            datetime.now()
        )
    )

    return finish(status, reason, distance)
