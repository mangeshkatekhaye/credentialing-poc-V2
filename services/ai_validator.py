# services/ai_validator.py

from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# -------------------------------
# LOAD ENV FILE
# -------------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# -------------------------------
# INITIALIZE CLIENT
# -------------------------------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    client = None
else:
    client = OpenAI(api_key=api_key)


# -------------------------------
# AI VALIDATION FUNCTION
# -------------------------------
def ai_validate(text, doc_type, mandatory_missing, high_risk_missing):

    # SAFETY CHECK
    if client is None:
        return "⚠️ AI insights unavailable (API key not configured)"

    # NON-CLINICAL FLOW
    if doc_type != "Clinical Document":
        return """
**Profile Type:** Non-Clinical

**Summary:**  
This profile represents a non-clinical professional. Provider credentialing checks such as NPI, DEA, and licensing are not applicable.

**Suggested Improvements:**
- Add measurable achievements (KPIs, impact metrics)
- Enhance role descriptions for clarity
- Include certifications and tools where relevant
"""

    # PREPARE INPUT
    mandatory_str = ", ".join(mandatory_missing) if mandatory_missing else "None"
    high_risk_str = ", ".join(high_risk_missing) if high_risk_missing else "None"

    # FINAL PROMPT
    prompt = f"""
You are a credentialing expert reviewing a healthcare provider profile.

The system has already identified the following:

Mandatory Issues: {mandatory_str}
High-Risk Gaps: {high_risk_str}

IMPORTANT:

# -------------------------------
# STRICT ALIGNMENT (CRITICAL)
# -------------------------------
- DO NOT reclassify issues
- DO NOT introduce new issues
- ONLY explain the issues exactly as provided
- Treat issue labels as the source of truth

- DO NOT use "expired" unless explicitly present in issue label

# -------------------------------
# LABEL → LANGUAGE MAPPING
# -------------------------------
- "Invalid/Missing" → "missing or not in a valid format"
- "Needs Full Date" → "present but not in a complete format"

# -------------------------------
# MANDATORY RULES (VERY STRICT)
# -------------------------------
- If Mandatory Issues = None → "None identified"
- If NOT empty:
  • ONLY describe them as "missing"
  • DO NOT use "invalid"
  • Summarize in ONE sentence
  • Example: "NPI, Board Certification, and Specialty information are missing."

# -------------------------------
# HIGH-RISK RULES
# -------------------------------
- If empty → "None identified"
- If NOT empty:
  • Summarize in ONE sentence
  • DO NOT repeat per field
  • Use grouped phrasing like:
    "Expiry information for license, DEA, board certification, and malpractice insurance..."

# -------------------------------
# TERMINOLOGY CONTROL
# -------------------------------
- Missing → no value
- Invalid → wrong format
- Partial → not complete

- DO NOT combine "missing" and "invalid" unless label explicitly says "Invalid/Missing"
- DO NOT say "invalid" for mandatory issues

# -------------------------------
# LANGUAGE QUALITY
# -------------------------------
- Be concise and professional
- Avoid repetition
- Use grouped sentences (NOT line-by-line repetition)

# -------------------------------
# OPTIONAL IMPROVEMENTS
# -------------------------------
- MUST exist if High-Risk exists
- MUST NOT include mandatory issues
- MUST align only with High-Risk gaps
- Keep actionable and concise

# -------------------------------
# OUTPUT FORMAT
# -------------------------------

❗ Mandatory Issues:
<summary or None identified>

⚠️ High-Risk Gaps:
<single grouped explanation>

ℹ️ Optional Improvements:
<aligned suggestions>
"""

    # OPENAI CALL
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content