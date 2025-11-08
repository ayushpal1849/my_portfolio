# scripts/parse_resume.py
# Parse assets/resume.pdf into data/resume_data.json (heuristic)
import os, json, re
from PyPDF2 import PdfReader

base = os.path.dirname(os.path.dirname(__file__))
pdf_path = os.path.join(base, 'assets', 'resume.pdf')
out_dir = os.path.join(base, 'data')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'resume_data.json')

def extract_text(path):
    reader = PdfReader(path)
    text = ''
    for p in reader.pages:
        t = p.extract_text()
        if t:
            text += t + '\n'
    return text

def find_block(text, heading):
    m = re.search(rf"{heading}[\s\S]*?(?=\n[A-Z ]{{2,}}\n|\Z)", text, re.IGNORECASE)
    if m:
        return m.group(0)
    return ''

text = extract_text(pdf_path)
data = {}
# Name + contact
lines = [l.strip() for l in text.splitlines() if l.strip()]
data['name'] = lines[0] if lines else ''
# quick heuristics
if 'SUMMARY' in text:
    m = re.split(r'SUMMARY', text, flags=re.IGNORECASE)
    data['summary'] = m[1].split('\n\n')[0].strip() if len(m)>1 else ''
# Technical skills block
skills = {}
if 'TECHNICAL SKILLS' in text:
    block = find_block(text, 'TECHNICAL SKILLS')
    # find lines like '❖ Programming Languages : Python, C, PHP'
    for line in block.splitlines():
        if ':' in line:
            k,v = line.split(':',1)
            k = re.sub(r'[^A-Za-z ]','',k).strip().lower().replace(' ','_')
            vals = [x.strip() for x in v.split(',') if x.strip()]
            skills[k] = vals
data['technical_skills'] = skills
# Education
if 'EDUCATION' in text:
    block = find_block(text, 'EDUCATION')
    # simple parse
    ed_lines = [l.strip() for l in block.splitlines() if l.strip() and not l.strip().upper().startswith('EDUCATION')]
    educations = []
    if ed_lines:
        educations.append({
            'degree': ed_lines[0],
            'institute': ed_lines[1] if len(ed_lines)>1 else '',
            'cgpa': re.search(r'CGPA\s*[-:]?\s*([0-9\.]+)', block) and re.search(r'CGPA\s*[-:]?\s*([0-9\.]+)', block).group(1) or '',
            'passing_year': re.search(r'\b(20\d{2})\b', block) and int(re.search(r'\b(20\d{2})\b', block).group(1)) or ''
        })
    data['education'] = educations
# Professional Experience
if 'PROFESSIONAL EXPERIENCE' in text:
    block = find_block(text, 'PROFESSIONAL EXPERIENCE')
    # crude split by company lines (lines with uppercase and location)
    lines = [l for l in block.splitlines() if l.strip()]
    experiences = []
    # heuristic: first non-heading lines describe company
    cur = {}
    for l in lines:
        if l.isupper() and len(l.split())>1:
            if cur:
                experiences.append(cur); cur = {}
            cur['company'] = l
        else:
            if 'role' not in cur:
                cur['role'] = l
            else:
                cur.setdefault('details','').join('\n'+l)
    if cur:
        experiences.append(cur)
    data['professional_experience'] = experiences

# Certifications (simple extract)
certs = []
cert_block = find_block(text, 'CERTIFICATION')
for line in cert_block.splitlines():
    if '•' in line or '-' in line or ',' in line:
        l = line.replace('•','').strip()
        if l:
            certs.append(l)
data['certifications'] = certs

# Achievements
ach_block = find_block(text, 'ACHIEVEMENTS')
achievements = []
for line in ach_block.splitlines():
    if '•' in line:
        achievements.append(line.replace('•','').strip())
data['achievements'] = achievements

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print('Wrote', out_path)
