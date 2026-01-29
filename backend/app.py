from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

from utils import extract_text_from_pdf, build_groq_prompt

# --------------------------------------------------
# App & Config
# --------------------------------------------------
load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# --------------------------------------------------
# Load Models (once)
# --------------------------------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=GROQ_API_KEY)

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Resume Analyzer API is running"})


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """
    Accepts:
    - resume (PDF)
    - job_description (text)

    Returns:
    - match percentage
    - AI suggestions
    """

    if "resume" not in request.files:
        return jsonify({"error": "Resume file is required"}), 400

    resume_file = request.files["resume"]
    job_description = request.form.get("job_description")

    if not job_description:
        return jsonify({"error": "Job description is required"}), 400

    # --------------------------------------------------
    # NLP: Text Extraction
    # --------------------------------------------------
    resume_text = extract_text_from_pdf(resume_file)

    # --------------------------------------------------
    # NLP: Embeddings & Similarity
    # --------------------------------------------------
    resume_embedding = embedding_model.encode([resume_text])
    jd_embedding = embedding_model.encode([job_description])

    similarity_score = cosine_similarity(
        resume_embedding, jd_embedding
    )[0][0]

    match_percentage = round(float(similarity_score) * 100, 2)



    # --------------------------------------------------
    # LLM: Groq Suggestions
    # --------------------------------------------------
    prompt = build_groq_prompt(resume_text, job_description)

    groq_response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    ai_suggestions = groq_response.choices[0].message.content

    # --------------------------------------------------
    # Response
    # --------------------------------------------------
    return jsonify({
        "match_percentage": match_percentage,
        "ai_suggestions": ai_suggestions
    })


# --------------------------------------------------
# Run App
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
