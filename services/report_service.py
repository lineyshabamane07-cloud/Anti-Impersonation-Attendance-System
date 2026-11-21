
from config import Config
from models.db import query
from services import mock_data


def list_marked(session_id):
    """Return attendance records for a session."""
    if Config.USE_MOCK:
        return mock_data.marked_list(session_id)

    rows = query(
        "SELECT a.student_id, u.name, a.status, "
        "a.distance_m, a.marked_at "
        "FROM attendance a "
        "JOIN users u ON u.id = a.student_id "
        "WHERE a.session_id = %s "
        "ORDER BY a.marked_at",
        (session_id,)
    )

    for row in rows:
        if row["marked_at"] is not None:
            row["marked_at"] = row["marked_at"].strftime("%H:%M:%S")

    return rows


def session_summary(session_id):
    """Return attendance statistics for a session."""
    if Config.USE_MOCK:
        return mock_data.session_summary(session_id)

    info = query(
        "SELECT s.id AS session_id, sub.name AS subject, "
        "c.division, c.room, "
        "(SELECT COUNT(*) FROM enrollments e "
        "WHERE e.class_id = c.id) AS total_students "
        "FROM sessions s "
        "JOIN classes c ON c.id = s.class_id "
        "JOIN subjects sub ON sub.id = c.subject_id "
        "WHERE s.id = %s",
        (session_id,),
        one=True
    )

    if info is None:
        return None

    counts = {"present": 0, "flagged": 0}

    rows = query(
        "SELECT status, COUNT(*) AS n "
        "FROM attendance "
        "WHERE session_id = %s "
        "GROUP BY status",
        (session_id,)
    )

    for row in rows:
        counts[row["status"]] = row["n"]

    rejected = query(
        "SELECT COUNT(*) AS n FROM attempts "
        "WHERE session_id = %s AND outcome = 'rejected'",
        (session_id,),
        one=True
    )

    info.update(
        present=counts["present"],
        flagged=counts["flagged"],
        rejected=rejected["n"]
    )

    return info


def list_attempts(only_problems=True):
    """Return attendance verification attempts."""
    if Config.USE_MOCK:
        return [{
            "created_at": "10:03:02",
            "student": "Demo Student",
            "outcome": "rejected",
            "reason": "QR expired - scan the latest code",
            "distance_m": 12.0
        }]

    sql = (
        "SELECT t.created_at, "
        "COALESCE(u.name, 'Unknown') AS student, "
        "t.outcome, t.reason, t.distance_m "
        "FROM attempts t "
        "LEFT JOIN users u ON u.id = t.student_id"
    )

    if only_problems:
        sql += " WHERE t.outcome IN ('rejected', 'flagged')"

    sql += " ORDER BY t.id DESC LIMIT 100"

    rows = query(sql)

    for row in rows:
        if row["created_at"] is not None:
            row["created_at"] = row["created_at"].strftime("%H:%M:%S")

    return rows
