import re
import docx
import spacy
from pdfminer.high_level import extract_text

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "python", "java", "c++", "sql", "html", "css", "javascript",
    "flask", "machine learning", "django", "react", "node", "mongodb",
    "tensorflow", "keras", "pandas", "numpy", "git", "docker", "aws"
]

# -------- PDF TEXT --------
def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        print("PDF TEXT LENGTH:", len(text) if text else 0)
        return text or ""
    except Exception as e:
        print("PDF ERROR:", e)
        return ""

# -------- DOCX TEXT --------
def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print("DOCX ERROR:", e)
        return ""

# -------- EMAIL --------
def extract_email(text):
    return re.findall(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)

# -------- PHONE --------
def extract_phone(text):
    # FIX: also match +91-XXXXXXXXXX and (XXX) XXX-XXXX patterns
    patterns = [
        r"\b\d{10}\b",
        r"\+?\d[\d\s\-]{8,13}\d",
    ]
    found = []
    for pat in patterns:
        found.extend(re.findall(pat, text))
    # deduplicate and clean
    return list(set(p.strip() for p in found))

# -------- NAME --------
def extract_name(text):
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return "Not Found"

    first_line = lines[0]

    # Heuristic: first line is short, no email, no skill keyword → likely a name
    if len(first_line.split()) <= 4 and "@" not in first_line:
        if not any(skill in first_line.lower() for skill in SKILLS_DB):
            return first_line

    # Fallback: spaCy NER
    doc = nlp(text[:1000])  # only scan the top of the resume for speed
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Not Found"

# -------- SKILLS --------
def extract_skills_ai(text):
    text_lower = text.lower()
    # FIX: multi-word skills need exact phrase matching
    found = []
    for skill in SKILLS_DB:
        # use word boundary for single-word, plain search for multi-word
        if " " in skill:
            if skill in text_lower:
                found.append(skill.title())
        else:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found.append(skill.title())
    return list(set(found))

# -------- SCORE --------
def calculate_score(resume_skills, job_skills):
    resume_set = set(s.lower() for s in resume_skills)
    # job_skills already cleaned in app.py, but be safe here too
    job_set = set(s.strip().lower() for s in job_skills if s.strip())

    if not job_set:
        return 0.0

    matched = resume_set.intersection(job_set)
    print(f"Matched skills: {matched} | Job wants: {job_set}")
    return round((len(matched) / len(job_set)) * 100, 2)