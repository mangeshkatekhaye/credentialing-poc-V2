def classify_document(text):
    text_lower = text.lower()

    # Clinical indicators
    clinical_keywords = [
        "mbbs", "md", "doctor", "npi", "license", "dea",
        "board certified", "medical council", "physician"
    ]

    # Non-clinical indicators
    non_clinical_keywords = [
        "engineer", "developer", "cloud", "platform",
        "azure", "databricks", "ai", "ml", "software"
    ]

    clinical_score = sum(word in text_lower for word in clinical_keywords)
    non_clinical_score = sum(word in text_lower for word in non_clinical_keywords)

    if clinical_score > non_clinical_score:
        return "Clinical Document"
    elif non_clinical_score > clinical_score:
        return "Non-Clinical Document"
    else:
        return "Unknown Document Type"