# scripts/create_admin.py
# Creates an admin user in the database. Reads username/password from .env if present, else prompts.
import os
import sys

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from getpass import getpass
from app import app
from models import db, User

def main():
    username = os.getenv('ADMIN_USER') or input('Admin username: ')
    password = os.getenv('ADMIN_PASSWORD') or getpass('Admin password: ')
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            print('User already exists, updating password.')
            user.set_password(password)
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
        db.session.commit()
        print('Admin user created/updated for', username)

if __name__ == '__main__':
    main()
