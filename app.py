import json
import os
import secrets
from functools import wraps

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, ValidationError, generate_csrf, validate_csrf
from sqlalchemy.exc import OperationalError
from werkzeug.utils import secure_filename

from config import Config
from models import (
    Achievement,
    Certification,
    Education,
    Experience,
    Project,
    Skill,
    User,
    bcrypt,
    db,
)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)

csrf = CSRFProtect(app)
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)

app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "resume_data.json")
PUBLIC_SPA_ROUTES = {
    "/",
    "/about",
    "/education",
    "/skills",
    "/experience",
    "/projects",
    "/certifications",
    "/contact",
}


@app.template_filter("fromjson")
def from_json_filter(json_string):
    if json_string:
        try:
            return json.loads(json_string)
        except (json.JSONDecodeError, TypeError):
            return None
    return None


def load_resume_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file_obj:
            return json.load(file_obj)
    return {}


def database_is_available():
    try:
        db.session.execute(db.select(User.id).limit(1))
        return True
    except OperationalError:
        db.session.rollback()
        return False


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def require_json(req):
    try:
        return req.get_json(force=True)
    except Exception:
        return None


def admin_session_required(json_response=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "admin_logged_in" not in session:
                if json_response:
                    return jsonify({"success": False, "message": "Unauthorized"}), 401
                flash("Please log in to access the admin dashboard.", "warning")
                return redirect(url_for("admin_login"))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def admin_csrf_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-CSRFToken") or request.form.get("csrf_token")
        try:
            validate_csrf(token)
        except ValidationError:
            return jsonify({"success": False, "message": "Invalid or missing CSRF token"}), 400
        return func(*args, **kwargs)

    return wrapper


def normalize_contact(data):
    return {
        "name": data.get("name", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "linkedin": data.get("linkedin", ""),
        "location": data.get("location", ""),
    }


def normalize_education(item):
    if isinstance(item, dict):
        return {
            "degree": item.get("degree", ""),
            "institute": item.get("institute", ""),
            "cgpa": item.get("cgpa", ""),
            "passing_year": item.get("passing_year", ""),
        }

    return {
        "degree": item.degree,
        "institute": item.institute,
        "cgpa": item.cgpa,
        "passing_year": item.passing_year,
    }


def normalize_experience(item):
    if isinstance(item, dict):
        responsibilities = item.get("responsibilities", [])
        if isinstance(responsibilities, str):
            responsibilities = from_json_filter(responsibilities) or []

        return {
            "company": item.get("company", ""),
            "location": item.get("location", ""),
            "role": item.get("role", ""),
            "duration": item.get("duration", ""),
            "responsibilities": responsibilities,
        }

    return {
        "company": item.company,
        "location": getattr(item, "location", ""),
        "role": item.role,
        "duration": item.duration,
        "responsibilities": from_json_filter(item.responsibilities) or [],
    }


def normalize_project(item):
    if isinstance(item, dict):
        description = item.get("description", "")
        link = item.get("link", "")
    else:
        description = item.description or ""
        link = item.link or ""

    highlights = [line.strip() for line in description.splitlines() if line.strip()]
    return {
        "title": item.get("title", "") if isinstance(item, dict) else item.title,
        "description": description,
        "highlights": highlights,
        "link": link,
    }


def normalize_certification(item):
    if isinstance(item, str):
        parts = [part.strip() for part in item.split(",")]
        title = parts[0] if parts else ""
        organization = parts[1] if len(parts) > 1 else ""
        year = parts[2] if len(parts) > 2 else ""
        return {
            "title": title,
            "organization": organization,
            "year": year,
            "image_url": None,
        }

    if isinstance(item, dict):
        return {
            "title": item.get("title", ""),
            "organization": item.get("organization", ""),
            "year": item.get("year", ""),
            "image_url": item.get("image_url"),
        }

    image_url = None
    if item.image_file:
        image_url = url_for(
            "static",
            filename=f"uploads/certs/{item.image_file}",
        )

    return {
        "title": item.title,
        "organization": item.organization,
        "year": item.year,
        "image_url": image_url,
    }


def normalize_skills(skills):
    normalized = {}
    for category, skill_list in skills.items():
        normalized[category] = [
            skill.name if hasattr(skill, "name") else skill for skill in skill_list
        ]
    return normalized


def get_public_content():
    data = load_resume_data()
    database_available = database_is_available()

    sections = {
        "educations": [],
        "experiences": [],
        "projects": [],
        "certifications": [],
        "skills": {},
        "achievements": data.get("achievements", []),
    }
    source = {"database": database_available, "fallback": not database_available}

    if database_available:
        sections["educations"] = [
            normalize_education(item) for item in Education.query.all()
        ]
        sections["experiences"] = [
            normalize_experience(item) for item in Experience.query.all()
        ]
        sections["projects"] = [normalize_project(item) for item in Project.query.all()]
        sections["certifications"] = [
            normalize_certification(item) for item in Certification.query.all()
        ]
        sections["skills"] = normalize_skills(Skill.get_skills_by_category())
        achievements = Achievement.query.all()
        if achievements:
            sections["achievements"] = [item.text for item in achievements]

    if not sections["educations"]:
        sections["educations"] = [
            normalize_education(item) for item in data.get("education", [])
        ]
    if not sections["experiences"]:
        sections["experiences"] = [
            normalize_experience(item)
            for item in data.get("professional_experience", [])
        ]
    if not sections["projects"]:
        sections["projects"] = [normalize_project(item) for item in data.get("projects", [])]
    if not sections["certifications"]:
        sections["certifications"] = [
            normalize_certification(item) for item in data.get("certifications", [])
        ]
    if not sections["skills"]:
        sections["skills"] = normalize_skills(data.get("technical_skills", {}))

    return {
        "profile": data.get("summary", ""),
        "contact": normalize_contact(data),
        "sections": sections,
        "meta": {
            "resume_url": url_for("download_resume"),
            "admin_url": url_for("admin_login"),
            "source": source,
        },
    }


def render_public_shell():
    return render_template(
        "public_shell.html",
        csrf_token=generate_csrf(),
    )


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


@app.route("/api/site-data")
def api_site_data():
    return jsonify(get_public_content())


@app.route("/")
@app.route("/about")
@app.route("/education")
@app.route("/skills")
@app.route("/experience")
@app.route("/projects")
@app.route("/certifications")
@app.route("/contact")
def public_shell():
    if request.path not in PUBLIC_SPA_ROUTES:
        abort(404)
    return render_public_shell()


@app.route("/download_resume")
def download_resume():
    resume_dir = app.config["RESUME_FOLDER"]
    resume_path = os.path.join(resume_dir, "resume.pdf")
    if os.path.exists(resume_path):
        return send_from_directory(resume_dir, "resume.pdf", as_attachment=True)
    flash("Resume not found.", "warning")
    return redirect(request.referrer or url_for("public_shell"))


@app.route("/admin/add_experience", methods=["POST"])
@csrf.exempt
@admin_session_required(json_response=True)
@admin_csrf_required
def add_experience():
    data = require_json(request)
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    company = data.get("company")
    role = data.get("role")
    if not company or not role:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    exp = Experience(
        company=company,
        role=role,
        duration=data.get("duration", ""),
        responsibilities=json.dumps(data.get("responsibilities", [])),
    )
    db.session.add(exp)
    db.session.commit()
    return jsonify({"success": True, "message": "Experience added", "id": exp.id})


@app.route("/admin/add_project", methods=["POST"])
@csrf.exempt
@admin_session_required(json_response=True)
@admin_csrf_required
def add_project():
    data = require_json(request)
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    title = data.get("title")
    if not title:
        return jsonify({"success": False, "message": "Missing title"}), 400

    proj = Project(
        title=title,
        description=data.get("description", ""),
        link=data.get("link", ""),
    )
    db.session.add(proj)
    db.session.commit()
    return jsonify({"success": True, "message": "Project added", "id": proj.id})


@app.route("/admin/add_certification", methods=["POST"])
@csrf.exempt
@admin_session_required(json_response=True)
@admin_csrf_required
def add_certification():
    title = request.form.get("title")
    organization = request.form.get("organization")
    year = request.form.get("year")

    if not all([title, organization, year]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    image_filename = None
    if "image" in request.files:
        file = request.files["image"]
        if file and file.filename != "" and allowed_file(file.filename):
            random_hex = secrets.token_hex(8)
            _, file_ext = os.path.splitext(secure_filename(file.filename))
            image_filename = random_hex + file_ext.lower()
            cert_dir = os.path.join(app.config["UPLOAD_FOLDER"], "certs")
            os.makedirs(cert_dir, exist_ok=True)
            file.save(os.path.join(cert_dir, image_filename))

    new_cert = Certification(
        title=title,
        organization=organization,
        year=year,
        image_file=image_filename,
    )
    db.session.add(new_cert)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "Certification added successfully!",
            "id": new_cert.id,
        }
    )


@app.route("/admin/upload_resume", methods=["POST"])
@csrf.exempt
@admin_session_required(json_response=True)
@admin_csrf_required
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"success": False, "message": "No file part in request."}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected."}), 400

    if file and file.filename.rsplit(".", 1)[1].lower() == "pdf":
        resume_dir = app.config["RESUME_FOLDER"]
        os.makedirs(resume_dir, exist_ok=True)
        file.save(os.path.join(resume_dir, "resume.pdf"))
        return jsonify({"success": True, "message": "Resume uploaded successfully!"})

    return (
        jsonify(
            {
                "success": False,
                "message": "Invalid file type. Please upload a PDF.",
            }
        ),
        400,
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if "admin_logged_in" in session:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["admin_logged_in"] = True
            session.permanent = True
            flash("Login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials", "danger")

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
@admin_session_required()
def admin_dashboard():
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "certs"), exist_ok=True)
    os.makedirs(app.config["RESUME_FOLDER"], exist_ok=True)
    database_available = database_is_available()
    storage_note = (
        "Uploads are stored on local disk in this phase. They may not survive instance replacement "
        "until deployment storage is upgraded."
    )
    return render_template(
        "admin_dashboard.html",
        database_available=database_available,
        storage_note=storage_note,
    )


@app.route("/admin/logout")
@admin_session_required()
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["APP_PORT"], debug=True)
