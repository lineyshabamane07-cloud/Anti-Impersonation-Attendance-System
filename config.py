import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-this")

    DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"

    USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "aias")

    DEFAULT_GEOFENCE_METERS = int(
        os.getenv("DEFAULT_GEOFENCE_METERS", 100)
    )

    QR_REFRESH_SECONDS = int(
        os.getenv("QR_REFRESH_SECONDS", 20)
    )

    SESSION_DURATION_MINUTES = int(
        os.getenv("SESSION_DURATION_MINUTES", 10)
    )
