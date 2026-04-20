def calculate_clinical_score(text):
    text = text.lower()

    score = 0

    if "license" in text:
        score += 25
    if "board" in text:
        score += 20
    if "dea" in text:
        score += 15
    if "education" in text:
        score += 15
    if "experience" in text:
        score += 15
    if "patient" in text or "clinical" in text:
        score += 10

    penalty = 0

    if "npi" not in text:
        penalty += 10
    if "cme" not in text:
        penalty += 3
    if "malpractice" not in text:
        penalty += 3
    if "privileges" not in text:
        penalty += 2
    if "oig" not in text:
        penalty += 2

    final_score = max(0, score - penalty)

    return final_score, {
        "Base Score": score,
        "Penalty": -penalty
    }


def calculate_score(data):
    score = 0

    if data.get("Full Name"):
        score += 15
    if data.get("Email"):
        score += 15
    if data.get("Phone Number"):
        score += 10
    if data.get("Skills"):
        score += 15
    if data.get("Total Experience"):
        score += 15

    text_blob = str(data).lower()

    if "certification" in text_blob:
        score += 10
    if any(tool in text_blob for tool in ["jira", "excel", "power bi", "salesforce"]):
        score += 10
    if "healthcare" in text_blob:
        score += 10

    return min(score, 100), {"Profile Strength": score}


def generate_checklist(data, text, doc_type):

    if doc_type != "Clinical Document":
        return [
            ("Full Name", bool(data.get("Full Name"))),
            ("Email", bool(data.get("Email"))),
            ("Phone Number", bool(data.get("Phone Number"))),
            ("Experience Identified", bool(data.get("Total Experience"))),
            ("Skills Present", bool(data.get("Skills"))),
            ("Healthcare Domain Exposure", "healthcare" in text.lower()),
            ("HIPAA Awareness", "hipaa" in text.lower())
        ]

    text = text.lower()

    return [
        ("Full Name", True),
        ("Email", True),
        ("Phone Number", True),
        ("Medical License Present", "license" in text),
        ("License Expiry Available", "expire" in text),
        ("Board Certification", "board" in text),
        ("DEA Registration", "dea" in text),
        ("NPI Present", "npi" in text),
        ("CME Information", "cme" in text),
        ("Malpractice Info", "malpractice" in text),
        ("Hospital Privileges", "privileges" in text),
        ("OIG / Sanctions Check", "oig" in text),
    ]