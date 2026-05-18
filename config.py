import os
import urllib.parse
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


def build_local_mysql_uri():
    local_db_user = os.getenv("LOCAL_DB_USER", "root")
    local_db_pass = os.getenv("LOCAL_DB_PASS", "")
    local_db_host = os.getenv("LOCAL_DB_HOST", "127.0.0.1")
    local_db_name = os.getenv("LOCAL_DB_NAME", "portfolio_db")

    return (
        f"mysql+pymysql://{local_db_user}:{urllib.parse.quote_plus(local_db_pass)}"
        f"@{local_db_host}:3306/{local_db_name}"
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.getenv("FLASK_SECRET_KEY", "dev-secret-key"))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or build_local_mysql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    APP_PORT = int(os.getenv("PORT", "8000"))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(STATIC_DIR / "uploads"))
    RESUME_FOLDER = os.getenv("RESUME_FOLDER", str(STATIC_DIR / "resume"))
