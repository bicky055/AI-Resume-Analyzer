from flask import Blueprint, request, jsonify
from utils.parser import extract_text_from_pdf
from utils.text_cleaner import clean_text

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    if "job_description" not in request.form:
        return jsonify({"error": "No job description provided"}), 400

    file = request.files["resume"]
    job_description = request.form["job_description"]

    # Extract and clean resume text
    resume_text = extract_text_from_pdf(file)

    print("Raw Resume Length:", len(resume_text))
    print("Raw JD Length:", len(job_description))

    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)

    print("Clean Resume Length:", len(resume_clean))
    print("Clean JD Length:", len(jd_clean))
    #TF IDF Vectorization
    vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english')
    vectors = vectorizer.fit_transform([resume_clean, jd_clean])

    print("Common Features:", set(resume_clean.split()) & set(jd_clean.split()))
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    match_score = round(similarity * 100 + 50, 2)
    resume_words = set(resume_clean.split())
    jd_words = set(jd_clean.split())

    matched_keywords = list(resume_words & jd_words)
    missing_keywords = list(jd_words - resume_words)

    return jsonify({
    "message": "Resume processed successfully",
    "match_score": match_score,
    "matched_keywords": matched_keywords[:15],
    "missing_keywords": missing_keywords[:15]
        })