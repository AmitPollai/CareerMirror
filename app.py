from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

skills_database = [
    "java",
    "python",
    "c++",
    "sql",
    "mysql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "spring boot",
    "git",
    "github",
    "oop",
    "dsa",
    "mongodb",
    "flask",
    "django",
    "bootstrap",
    "docker",
    "aws",
    "azure",
    "kubernetes"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]
    job_description = request.form["job_description"]

    if not file:
        return "No File Uploaded"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    text = ""

    try:

        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

    except Exception as e:
        return f"Error Reading PDF: {str(e)}"

    text_lower = text.lower()
    jd_lower = job_description.lower()

    resume_skills = []
    jd_skills = []

    for skill in skills_database:

        if skill in text_lower:
            resume_skills.append(skill)

        if skill in jd_lower:
            jd_skills.append(skill)

    matched = []
    missing = []

    for skill in jd_skills:

        if skill in resume_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    if len(jd_skills) > 0:

        job_match_score = int(
            (len(matched) / len(jd_skills)) * 100
        )

    else:

        job_match_score = 0

    resume_score = min(
        len(resume_skills) * 10,
        100
    )

    suggestions = []

    if "github" not in text_lower:
        suggestions.append(
            "Add GitHub Profile"
        )

    if "linkedin" not in text_lower:
        suggestions.append(
            "Add LinkedIn Profile"
        )

    if "project" not in text_lower:
        suggestions.append(
            "Add More Projects"
        )

    if len(resume_skills) < 8:
        suggestions.append(
            "Add More Technical Skills"
        )

    if not suggestions:
        suggestions.append(
            "Resume Looks Strong"
        )

    ats_score = 0

    if "github" in text_lower:
        ats_score += 15

    if "linkedin" in text_lower:
        ats_score += 15

    if "project" in text_lower:
        ats_score += 20

    if "experience" in text_lower:
        ats_score += 20

    if "education" in text_lower:
        ats_score += 10

    ats_score += min(
        len(resume_skills) * 2,
        20
    )

    ats_score = min(
        ats_score,
        100
    )

    recommended_roles = []

    if "java" in resume_skills:
        recommended_roles.append(
            "Java Developer"
        )

    if "python" in resume_skills:
        recommended_roles.append(
            "Python Developer"
        )

    if "html" in resume_skills and "css" in resume_skills:
        recommended_roles.append(
            "Frontend Developer"
        )

    if "javascript" in resume_skills:
        recommended_roles.append(
            "Web Developer"
        )

    if "sql" in resume_skills:
        recommended_roles.append(
            "Database Developer"
        )

    if "react" in resume_skills:
        recommended_roles.append(
            "React Developer"
        )

    if "node.js" in resume_skills:
        recommended_roles.append(
            "Backend Developer"
        )

    if "java" in resume_skills and "sql" in resume_skills:
        recommended_roles.append(
            "Full Stack Developer"
        )

    if len(recommended_roles) == 0:
        recommended_roles.append(
            "Software Engineer"
        )

    interview_questions = []

    roadmap = []

    for skill in missing:

        if skill == "react":

            interview_questions.append(
                "What are React Components and Props?"
            )

            roadmap.append(
                "Learn React Fundamentals → Components → Hooks → Projects"
            )

        elif skill == "mongodb":

            interview_questions.append(
                "How is MongoDB different from MySQL?"
            )

            roadmap.append(
                "Learn MongoDB CRUD Operations → Aggregation → Projects"
            )

        elif skill == "spring boot":

            interview_questions.append(
                "Explain Spring Boot Architecture."
            )

            roadmap.append(
                "Learn Spring Core → Spring Boot → REST APIs"
            )

        elif skill == "node.js":

            interview_questions.append(
                "What is Event Loop in Node.js?"
            )

            roadmap.append(
                "Learn Node.js Basics → Express.js → APIs"
            )

        elif skill == "docker":

            interview_questions.append(
                "What is Docker and why is it used?"
            )

            roadmap.append(
                "Learn Containers → Docker Images → Deployment"
            )

        elif skill == "aws":

            interview_questions.append(
                "What are AWS EC2 and S3?"
            )

            roadmap.append(
                "Learn AWS Basics → EC2 → S3 → Deployment"
            )

    return render_template(
        "result.html",
        text=text,
        resume_skills=resume_skills,
        jd_skills=jd_skills,
        matched=matched,
        missing=missing,
        resume_score=resume_score,
        job_match_score=job_match_score,
        ats_score=ats_score,
        suggestions=suggestions,
        recommended_roles=recommended_roles,
        interview_questions=interview_questions,
        roadmap=roadmap,
        matched_count=len(matched),
        missing_count=len(missing)
    )


if __name__ == "__main__":
    app.run(debug=True)