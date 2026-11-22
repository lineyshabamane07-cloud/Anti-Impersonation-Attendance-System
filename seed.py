
import bcrypt
from models.db import execute, query

DEMO_PASSWORD = "demo123"


def hash_pw(plain):
    return bcrypt.hashpw(
        plain.encode(),
        bcrypt.gensalt()
    ).decode()


def add_user(code, name, role, division=None):
    return execute(
        "INSERT INTO users "
        "(user_code, name, email, password_hash, role, division) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (
            code,
            name,
            f"{code.lower()}@example.com",
            hash_pw(DEMO_PASSWORD),
            role,
            division
        )
    )


def run():
    # Prevent duplicate demo data
    existing = query(
        "SELECT id FROM users WHERE user_code = %s",
        ("F001",),
        one=True
    )

    if existing:
        print("Demo data already exists. Seeding skipped.")
        return

    # Add faculty and admin
    faculty_id = add_user(
        "F001", "Dr. Demo Faculty", "faculty"
    )

    add_user("A001", "Demo Admin", "admin")

    # Add 10 demo students
    student_names = [
        "Reet Lunkad",
        "Krishna Panjwani",
        "Mrunal Kale",
        "Lineysha Bamane",
        "Tanmai Divekar",
        "Aarav Shah",
        "Isha Patil",
        "Rohan Mehta",
        "Sneha Iyer",
        "Kabir Singh"
    ]

    student_ids = []

    for i, name in enumerate(student_names):
        student_id = add_user(
            f"S{i + 1:03d}",
            name,
            "student",
            "SY-B"
        )
        student_ids.append(student_id)

    # Add subject
    subject_id = execute(
        "INSERT INTO subjects (code, name) "
        "VALUES (%s, %s)",
        ("DAA", "Design and Analysis of Algorithms")
    )

    # Add class
    class_id = execute(
        "INSERT INTO classes "
        "(subject_id, faculty_id, division, room) "
        "VALUES (%s, %s, %s, %s)",
        (subject_id, faculty_id, "SY-B", "304")
    )

    # Enroll all students
    for student_id in student_ids:
        execute(
            "INSERT INTO enrollments "
            "(class_id, student_id) VALUES (%s, %s)",
            (class_id, student_id)
        )

    print("Demo data inserted successfully!")
    print("Faculty: 1")
    print("Admin: 1")
    print("Students:", len(student_ids))
    print("Subject: DAA")
    print("Division: SY-B")
    print("Class ID:", class_id)
    print("Demo password:", DEMO_PASSWORD)


if __name__ == "__main__":
    run()
