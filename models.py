from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()  # initialize in app with bcrypt.init_app(app) or by importing this module after app created

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        # stores bcrypt hash (bytes -> decode to str)
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(256))
    role = db.Column(db.String(256))
    duration = db.Column(db.String(128))
    responsibilities = db.Column(db.Text)  # JSON list stored as text

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    link = db.Column(db.String(512))

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(256))
    institute = db.Column(db.String(256))
    cgpa = db.Column(db.String(64))
    passing_year = db.Column(db.Integer)

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512))
    organization = db.Column(db.String(256))
    year = db.Column(db.String(32))
    image_file = db.Column(db.String(256), nullable=True)  # Stores the filename of the certificate image

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(128))
    name = db.Column(db.String(128))

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512))
