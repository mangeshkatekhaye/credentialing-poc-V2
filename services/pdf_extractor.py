# services/pdf_extractor.py

import fitz  # PyMuPDF
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import httpx


# -------------------------------
# LOAD ENV
# -------------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")


# -------------------------------
# INITIALIZE OPENAI CLIENT (WITH TIMEOUT)
# -------------------------------
if not api_key:
    client = None
else:
    client = OpenAI(
        api_key=api_key,
        timeout=httpx.Timeout(20.0)  # 🔥 prevents infinite hang
    )


# -------------------------------
# EXTRACT TEXT FROM PDF
# -------------------------------
def extract_text_from_pdf(uploaded_file):
    try:
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        text = ""
        for page in pdf:
            text += page.get_text()

        return text

    except Exception as e:
        print("PDF Extraction Error:", e)
        return ""


# -------------------------------
# EXTRACT STRUCTURED DATA USING AI
# -------------------------------
def extract_structured_data(text):

    if client is None:
        return {}

    try:
        prompt = f"""
Extract structured credentialing information from the document.

Return ONLY valid JSON with these fields:

- first_name
- last_name
- full_name
- dob
- gender
- phone
- email
- address
- npi
- specialty
- license_number
- license_expiry
- dea_number
- dea_expiry
- board_certified (true/false)
- board_expiry
- practice_name
- tin
- medicaid_id
- malpractice_insurance (true/false)
- malpractice_expiry

Rules:
- If a value is missing, return "" or false
- Do NOT guess or hallucinate
- Use only information present in the document
- Use the word "missing" only implicitly (do not add explanation)
- Return STRICT JSON (no explanation, no markdown)

Document:
{text[:6000]}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        # -------------------------------
        # CLEAN RESPONSE (HANDLE ```json```)
        # -------------------------------
        if result.startswith("```"):
            result = result.replace("```json", "").replace("```", "").strip()

        # -------------------------------
        # SAFE JSON PARSE
        # -------------------------------
        try:
            return json.loads(result)
        except Exception as parse_error:
            print("JSON Parse Error:", parse_error)
            print("Raw Response:", result)
            return {}

    except Exception as e:
        print("OpenAI Extraction Error:", e)
        return {}