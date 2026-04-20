from flask import Flask, render_template, request
import os

from extractor import *
from database import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    # Hardcoded fake result to test if template works
    results = [{
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "9876543210",
        "skills": "Python, Flask",
        "score": 75.0
    }]
    return render_template("result.html", results=results)

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('resume')
    job_desc = request.form.get('job_desc', "")
    # FIX 1: strip whitespace and lowercase each job skill
    job_skills = [s.strip().lower() for s in job_desc.split(",") if s.strip()]

    results = []

    print("FILES COUNT:", len(files))

    for file in files:
        if file and file.filename != "":
            print("Processing:", file.filename)

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            filename = file.filename.lower()

            try:
                if filename.endswith(".pdf"):
                    text = extract_text_from_pdf(filepath)
                elif filename.endswith(".docx"):
                    text = extract_text_from_docx(filepath)
                else:
                    print("Unsupported file type:", file.filename)
                    continue

                if not text or text.strip() == "":
                    print("Empty text for:", file.filename)
                    continue

                name  = extract_name(text)
                email = extract_email(text)   # list
                phone = extract_phone(text)   # list
                skills = extract_skills_ai(text)  # list

                score = calculate_score(skills, job_skills)

                # FIX 2: safe join — handles empty lists without crashing
                insert_candidate(
                    name,
                    ", ".join(email) if email else "Not Found",
                    ", ".join(phone) if phone else "Not Found",
                    ", ".join(skills) if skills else "None",
                    score
                )

                results.append({
                    "name": name,
                    "email": ", ".join(email) if email else "Not Found",
                    "phone": ", ".join(phone) if phone else "Not Found",
                    "skills": ", ".join(skills) if skills else "None",
                    "score": score
                })

            except Exception as e:
                import traceback
                print("ERROR processing", file.filename, ":", e)
                traceback.print_exc()   # FIX 3: full traceback so you can debug

    results.sort(key=lambda x: x["score"], reverse=True)
    return render_template("result.html", results=results)

@app.route('/dashboard')
def dashboard():
    candidates = get_all_candidates()
    return render_template("dashboard.html", candidates=candidates)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, port=5001)