"""
Reset AIAS demo data.

This removes attendance sessions, QR tokens, attendance records,
scan attempts, and saved devices.

Users, subjects, classes and enrollments are not deleted.

Run:
    python reset_demo.py
"""

from models.db import execute


queries = [
    "DELETE FROM attempts",
    "DELETE FROM attendance",
    "DELETE FROM qr_tokens",
    "DELETE FROM devices",
    "DELETE FROM sessions",
]


def reset_demo():

    print("Starting AIAS demo reset...")

    for sql in queries:
        execute(sql)
        print("Executed:", sql)

    print()
    print("Demo reset completed successfully.")
    print("Users and classes have been preserved.")


if __name__ == "__main__":
    reset_demo()
