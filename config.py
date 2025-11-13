import os
from dotenv import load_dotenv
from pathlib import Path
import urllib.parse

# secrets
SECRET_KEY = os.getenv("SECRET_KEY", os.getenv("FLASK_SECRET_KEY", "dev-secret"))

# Prefer DATABASE_URL (Railway). If not present, fallback to local MySQL (XAMPP).
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # accepted forms: postgresql://... or postgresql+psycopg2://...
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    # local dev MySQL fallback (XAMPP)
    LOCAL_DB_USER = os.getenv("LOCAL_DB_USER", "root")
    LOCAL_DB_PASS = os.getenv("LOCAL_DB_PASS", "")
    LOCAL_DB_HOST = os.getenv("LOCAL_DB_HOST", "127.0.0.1")
    LOCAL_DB_NAME = os.getenv("LOCAL_DB_NAME", "portfolio_db")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{LOCAL_DB_USER}:{urllib.parse.quote_plus(LOCAL_DB_PASS)}"
        f"@{LOCAL_DB_HOST}:3306/{LOCAL_DB_NAME}"
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False

# load .env from project root
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    # attempt parent folder
    load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
