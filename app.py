from flask import Flask, render_template, request
import os

from analyzer import extract_text_from_pdf, analyze_resume


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    job_description = ""

    if request.method == "POST":

        # Get job description
        job_description = request.form.get("job_description", "").strip()

        # Get uploaded resume
        resume_file = request.files.get("resume")

        if not job_description:
            result = {
                "error": "Please enter a Job Description."
            }

            return render_template(
                "index.html",
                result=result,
                job_description=job_description
            )

        if not resume_file or resume_file.filename == "":
            result = {
                "error": "Please upload your resume PDF."
            }

            return render_template(
                "index.html",
                result=result,
                job_description=job_description
            )

        # Save resume
        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume_file.filename
        )

        resume_file.save(file_path)

        try:

            # Extract resume text
            resume_text = extract_text_from_pdf(file_path)

            # Analyze
            result = analyze_resume(
                resume_text,
                job_description
            )

            if not result["matched_skills"] and not result["missing_skills"]:
                result["error"] = (
                    "No recognized skills were found in the Job Description. "
                    "Please enter skills such as Python, C, Git, Arduino, IoT, etc."
                )

        except Exception as e:

            result = {
                "error": f"Error analyzing resume: {str(e)}"
            }

    return render_template(
        "index.html",
        result=result,
        job_description=job_description
    )


if __name__ == "__main__":
    app.run(debug=True)