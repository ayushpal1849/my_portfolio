# scripts/populate_db.py
# Populate DB from data/resume_data.json
import os
import json
import sys

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from models import db, Education, Experience, Certification, Skill, Achievement, Project
from sqlalchemy.exc import IntegrityError

base = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(base, 'data', 'resume_data.json')
if not os.path.exists(data_path):
    print('resume_data.json not found. Run parse_resume.py first.')
    raise SystemExit(1)

with app.app_context():
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Education
    for ed in data.get('education', []):
        e = Education(degree=ed.get('degree'), institute=ed.get('institute'), cgpa=ed.get('cgpa',''), passing_year=ed.get('passing_year') or None)
        db.session.add(e)
    # Experience
    for ex in data.get('professional_experience', []):
        exp = Experience(company=ex.get('company'), role=ex.get('role'), duration=ex.get('duration',''), responsibilities=json.dumps(ex.get('responsibilities',[])))
        db.session.add(exp)
    # Certifications
    for c in data.get('certifications', []):
        db.session.add(Certification(title=c, organization='', year=''))
    # Achievements
    for a in data.get('achievements', []):
        db.session.add(Achievement(text=a))
    # Skills (technical_skills is dict)
    for cat, items in data.get('technical_skills', {}).items():
        for it in items:
            db.session.add(Skill(category=cat, name=it))
    try:
        db.session.commit()
        print('Database populated successfully.')
    except IntegrityError as e:
        db.session.rollback()
        print('Integrity Error:', e)
