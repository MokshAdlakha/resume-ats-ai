# 📄 Resume ATS AI

An AI-powered resume screening tool that parses multiple PDF/DOCX resumes, extracts candidate information, and ranks applicants based on job description match — built with Flask and spaCy.

---

## 🚀 Live Demo
> Coming soon — deploying on Render

---

## ✨ Features

- 📤 Upload multiple resumes at once (PDF & DOCX)
- 🔍 Extracts **Name, Email, Phone, Skills** automatically
- 🧠 NLP-powered name detection using **spaCy**
- 📊 Scores and **ranks candidates** by job description match
- 💾 Stores all results in a local SQLite database
- 📋 Dashboard to view all past candidates

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| NLP | spaCy (`en_core_web_sm`) |
| PDF Parsing | pdfminer.six |
| DOCX Parsing | python-docx |
| Database | SQLite |
| Frontend | HTML, CSS (Jinja2 templates) |
| Deployment | Render + Gunicorn |

---

## 📁 Project Structure

```
resume_ats_ai/
│
├── templates/
│   ├── index.html        # Upload page
│   ├── result.html       # Results table
│   └── dashboard.html    # All candidates
│
├── uploads/              # Uploaded resumes (temp)
├── app.py                # Flask routes
├── extractor.py          # Resume parsing logic
├── database.py           # SQLite operations
├── requirements.txt      # Dependencies
└── resumes.db            # SQLite database
```

---

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/MokshAdlakha/resume-ats-ai.git
cd resume-ats-ai
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

**4. Run the app**
```bash
python app.py
```

**5. Open in browser**
```
http://127.0.0.1:5000
```

---

## 📌 How It Works

1. User uploads one or more resumes (PDF/DOCX)
2. User enters required skills as a comma-separated job description
3. App extracts **name, email, phone, skills** from each resume
4. Each resume is **scored** based on how many job skills it matches
5. Results are displayed ranked from highest to lowest score
6. All candidates are saved to the database for later review

---

## 📸 Screenshots

> _Add screenshots of your app here_

---

## 🙋‍♂️ Author

**Moksh Adlakha**  
[GitHub](https://github.com/MokshAdlakha)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
