import re
from pypdf import PdfReader


# Skills that the analyzer can recognize
SKILL_LIST = [
    "Python",
    "C",
    "C++",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "Git",
    "GitHub",
    "Flask",
    "Django",
    "Embedded C",
    "Microcontrollers",
    "Arduino",
    "IoT",
    "MATLAB",
    "Digital Electronics",
    "Analog Electronics",
    "Communication Systems",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Structures",
    "Problem Solving",
    "Communication",
    "Teamwork",
]


def extract_text_from_pdf(file_path):
    """Extract text from uploaded PDF."""
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def normalize_text(text):
    """Convert text into a standard format."""
    text = text.lower()
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    return text


def skill_found(skill, text):
    """Check whether a skill exists in the text."""
    text = normalize_text(text)
    skill = normalize_text(skill)

    # Special handling for C and C++
    if skill == "c":
        return bool(re.search(r"\bc\b", text))

    if skill == "c++":
        return "c++" in text

    return skill in text


def extract_skills(text):
    """Find recognized skills in text."""
    found_skills = []

    for skill in SKILL_LIST:
        if skill_found(skill, text):
            found_skills.append(skill)

    return found_skills


def analyze_resume(resume_text, job_description):
    """
    Compare resume skills with skills mentioned
    in the job description.
    """

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = []
    missing_skills = []

    for skill in job_skills:

        if skill in resume_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    # Calculate score
    if len(job_skills) > 0:
        score = round((len(matched_skills) / len(job_skills)) * 100)
    else:
        score = 0

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }