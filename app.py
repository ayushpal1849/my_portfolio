from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash
from flask_migrate import Migrate
from config import Config
from flask import session, abort
from flask_wtf.csrf import CSRFProtect, generate_csrf
from sqlalchemy.exc import OperationalError
from models import db, User, Experience, Project, Education, Certification, Skill, Achievement
from werkzeug.utils import secure_filename
import secrets
import json, os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Custom Jinja filter to parse JSON strings from the database
@app.template_filter('fromjson')
def from_json_filter(json_string):
    """Parses a JSON string into a Python object."""
    if json_string:
        try:
            return json.loads(json_string)
        except (json.JSONDecodeError, TypeError):
            return None
    return None

# Utility to load fallback JSON data (generated from resume parsing)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'resume_data.json')

def load_resume_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@app.route('/')
def index():
    # attempt load from DB, fallback to JSON data
    educations = []
    data = load_resume_data()
    try:
        educations = Education.query.all()
    except OperationalError:
        flash("Database not connected. Displaying fallback data.", "warning")
    
    if not educations:
        educations = data.get('education')

    profile = data.get('summary','')
    contact = {'name': data.get('name'), 'email': data.get('email'), 'phone': data.get('phone'), 'linkedin': data.get('linkedin')}
    return render_template('index.html', profile=profile, contact=contact)

@app.route('/about')
def about():
    data = load_resume_data()
    return render_template('about.html', data=data)

@app.route('/educational-qualification')
def educational():
    educations = []
    try:
        educations = Education.query.all()
    except OperationalError:
        flash("Database not connected. Displaying fallback data.", "warning")
    
    if not educations:
        data = load_resume_data()
        educations = data.get('education', [])
    return render_template('educational.html', educations=educations)

@app.route('/professional-experience')
def professional():
    experiences = []
    try:
        experiences = Experience.query.all()
    except OperationalError:
        flash("Database not connected. Displaying fallback data.", "warning")

    if not experiences:
        data = load_resume_data()
        experiences = data.get('professional_experience', [])
    return render_template('professional_experience.html', experiences=experiences)

@app.route('/certifications')
def certifications():
    certs = []
    try:
        certs = Certification.query.all()
    except OperationalError:
        flash("Database not connected. Displaying fallback data.", "warning")

    if not certs:
        data = load_resume_data()
        certs = data.get('certifications', [])
    return render_template('certifications.html', certs=certs)

@app.route('/technical-skills')
def technical_skills():
    skills = {}
    try:
        skills = Skill.get_skills_by_category()
    except OperationalError:
        flash("Database not connected. Displaying fallback data.", "warning")
    
    if not skills:
        data = load_resume_data()
        skills = data.get('technical_skills', {})
    return render_template('technical_skills.html', skills=skills)

@app.route('/projects')
def projects():
    all_projects = []
    try:
        all_projects = Project.query.all()
    except OperationalError:
        flash("Database not connected. Displaying fallback data.", "warning")

    if not all_projects:
        data = load_resume_data()
        all_projects = data.get('projects', [])
    return render_template('projects.html', projects=all_projects)

@app.route('/download_resume')
def download_resume():
    resume_dir = os.path.join(app.root_path, 'static', 'resume')
    resume_path = os.path.join(resume_dir, 'resume.pdf')
    if os.path.exists(resume_path):
        return send_from_directory(resume_dir, 'resume.pdf', as_attachment=True)
    else:
        flash('Resume not found.', 'warning')
        return redirect(request.referrer or url_for('index'))

# Admin endpoints (AJAX)
def require_json(req):
    try:
        return req.get_json(force=True)
    except:
        return None

# --- Existing Admin Endpoints ---

@app.route('/admin/add_experience', methods=['POST'])
def add_experience():
    data = require_json(request)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    company = data.get('company')
    role = data.get('role')
    if not company or not role:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    import json as _json
    exp = Experience(company=company, role=role, duration=data.get('duration',''), responsibilities=_json.dumps(data.get('responsibilities',[])))
    db.session.add(exp)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Experience added', 'id': exp.id})

@app.route('/admin/add_project', methods=['POST'])
def add_project():
    data = require_json(request)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    title = data.get('title')
    if not title:
        return jsonify({'success': False, 'message': 'Missing title'}), 400
    proj = Project(title=title, description=data.get('description',''), link=data.get('link',''))
    db.session.add(proj)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Project added', 'id': proj.id})

# --- New Admin Endpoints ---

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/admin/add_certification', methods=['POST'])
def add_certification():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    title = request.form.get('title')
    organization = request.form.get('organization')
    year = request.form.get('year')

    if not all([title, organization, year]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            # Generate a secure, random filename
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            image_filename = random_hex + f_ext
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'certs', image_filename))

    new_cert = Certification(
        title=title,
        organization=organization,
        year=year,
        image_file=image_filename
    )
    db.session.add(new_cert)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Certification added successfully!', 'id': new_cert.id})

@app.route('/admin/upload_resume', methods=['POST'])
def upload_resume():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    if 'resume' not in request.files:
        return jsonify({'success': False, 'message': 'No file part in request.'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected.'}), 400

    if file and file.filename.rsplit('.', 1)[1].lower() == 'pdf':
        resume_dir = os.path.join(app.static_folder, 'resume')
        os.makedirs(resume_dir, exist_ok=True)
        # The file will always be named 'resume.pdf' to overwrite the old one
        file.save(os.path.join(resume_dir, 'resume.pdf'))
        return jsonify({'success': True, 'message': 'Resume uploaded successfully!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid file type. Please upload a PDF.'}), 400

# Simple admin login route for accessing admin dashboard (for demonstration)
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('admin_login.html', csrf_token=generate_csrf)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        flash('Please log in to access the admin dashboard.', 'warning')
        return redirect(url_for('admin_login'))
    
    # Create upload directories if they don't exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'certs'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'resume'), exist_ok=True)

    return render_template('admin_dashboard.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)