import pdfplumber
import re

def extract_text_from_pdf(file):
    """
    Extracts raw text from uploaded PDF resume
    """
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return clean_text(text)


def clean_text(text):
    """
    Basic NLP preprocessing:
    - lowercase
    - remove special characters
    - remove extra spaces
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_groq_prompt(resume_text, job_description):
    """
    Prompt engineering for Groq LLM
    """
    prompt = f"""
You are an AI resume reviewer.

Resume:
{resume_text}

Job Description:
{job_description}

Perform the following:
1. List missing technical and soft skills
2. Suggest 3 specific resume improvements
3. Suggest 2 keywords to add for ATS optimization

Return the answer in clear bullet points.
"""
    return prompt
