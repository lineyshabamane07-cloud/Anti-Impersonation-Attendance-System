
import os

# Use the real MySQL database for this test
os.environ["USE_MOCK"] = "false"

from models.db import query
from services import qr_service, verify_service, report_service

LAT = 18.5204
LNG = 73.8567

# Find the demo class instead of assuming its ID is 1
demo_class = query(
    "SELECT id FROM classes WHERE division = %s "
    "ORDER BY id DESC LIMIT 1",
    ("SY-B",),
    one=True
)

if demo_class is None:
    raise RuntimeError("No demo class found. Check seed.py.")

class_id = demo_class["id"]

# Find the demo students
students = query(
    "SELECT id, user_code FROM users "
    "WHERE user_code IN (%s, %s, %s)",
    ("S001", "S002", "S003")
)

student_ids = {
    student["user_code"]: student["id"]
    for student in students
}

if len(student_ids) != 3:
    raise RuntimeError("Demo students are missing.")

# Create a new attendance session
session_id = qr_service.create_session(
    class_id,
    LAT,
    LNG,
    radius_m=100
)

# Generate QR token
token_data = qr_service.get_current_token(session_id)
token = token_data["token"]

if not token:
    raise RuntimeError("Could not generate a QR token.")

print("Session ID:", session_id)
print("QR token generated successfully!")

# Test 1: Valid attendance
print(
    "1. Valid:",
    verify_service.mark_attendance(
        token, student_ids["S001"],
        LAT, LNG, "phone-A"
    )
)

# Test 2: Duplicate attendance
print(
    "2. Duplicate:",
    verify_service.mark_attendance(
        token, student_ids["S001"],
        LAT, LNG, "phone-A"
    )
)

# Test 3: Student outside geofence
print(
    "3. Far away:",
    verify_service.mark_attendance(
        token, student_ids["S002"],
        LAT + 0.01, LNG, "phone-B"
    )
)

# Test 4: Invalid QR token
print(
    "4. Invalid token:",
    verify_service.mark_attendance(
        "invalid-token",
        student_ids["S003"],
        LAT, LNG, "phone-C"
    )
)

# Display results
print("Attendance:", report_service.list_marked(session_id))
print("Summary:", report_service.session_summary(session_id))

