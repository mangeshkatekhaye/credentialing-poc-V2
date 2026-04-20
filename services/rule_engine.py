# services/rule_engine.py

from datetime import datetime


# -------------------------------
# UTIL FUNCTIONS
# -------------------------------

EVALUATION_DATE = datetime(2025, 1, 1)

def is_empty(value):
    """
    Checks if a value is empty (None, "", whitespace)
    """
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def parse_date(value):
    """
    Tries to parse a date from multiple formats
    Returns datetime object or None
    """
    if is_empty(value):
        return None

    value = value.strip()

    formats = [
        "%Y-%m-%d",   # 2025-06-30
        "%m/%d/%Y",   # 06/30/2025
        "%B %Y",      # June 2025
        "%b %Y"       # Jun 2025
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except:
            continue

    return None


def is_valid_date(value):
    """
    Checks if date is parsable in any supported format
    """
    return parse_date(value) is not None


def is_precise_date(value):
    """
    Checks if date is in full precision format (YYYY-MM-DD or MM/DD/YYYY)
    """
    if is_empty(value):
        return False

    value = value.strip()

    precise_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y"
    ]

    for fmt in precise_formats:
        try:
            datetime.strptime(value, fmt)
            return True
        except:
            continue

    return False


def is_expired(value):
    """
    Checks if parsed date is in the past
    """
    date_value = parse_date(value)
    if not date_value:
        return False

    return date_value < EVALUATION_DATE


# -------------------------------
# MAIN RULE ENGINE
# -------------------------------
def evaluate_rules(data):
    """
    Input: structured form data (dictionary)
    Output:
        mandatory_missing (list)
        high_risk_missing (list)
    """

    mandatory_missing = []
    high_risk_missing = []

    # -------------------------------
    # MANDATORY RULES
    # -------------------------------

    if is_empty(data.get("npi")):
        mandatory_missing.append("NPI")

    if is_empty(data.get("license_number")):
        mandatory_missing.append("Medical License")

    if not data.get("board_certified"):
        mandatory_missing.append("Board Certification")

    if is_empty(data.get("specialty")):
        mandatory_missing.append("Specialty")

    # -------------------------------
    # HIGH-RISK RULES
    # -------------------------------

    # License
    if not is_empty(data.get("license_number")):
        expiry = data.get("license_expiry")

        if not is_valid_date(expiry):
            high_risk_missing.append("License Expiry (Invalid/Missing)")
        elif not is_precise_date(expiry):
            high_risk_missing.append("License Expiry (Needs Full Date)")
        elif is_expired(expiry):
            high_risk_missing.append("License Expiry (Expired)")

    # DEA
    if not is_empty(data.get("dea_number")):
        expiry = data.get("dea_expiry")

        if not is_valid_date(expiry):
            high_risk_missing.append("DEA Expiry (Invalid/Missing)")
        elif not is_precise_date(expiry):
            high_risk_missing.append("DEA Expiry (Needs Full Date)")
        elif is_expired(expiry):
            high_risk_missing.append("DEA Expiry (Expired)")

    # Board Certification
    if data.get("board_certified"):
        expiry = data.get("board_expiry")

        if not is_valid_date(expiry):
            high_risk_missing.append("Board Certification Expiry (Invalid/Missing)")
        elif not is_precise_date(expiry):
            high_risk_missing.append("Board Certification Expiry (Needs Full Date)")
        elif is_expired(expiry):
            high_risk_missing.append("Board Certification Expiry (Expired)")

    # Malpractice Insurance
    if data.get("malpractice_insurance"):
        expiry = data.get("malpractice_expiry")

        if not is_valid_date(expiry):
            high_risk_missing.append("Malpractice Insurance Expiry (Invalid/Missing)")
        elif not is_precise_date(expiry):
            high_risk_missing.append("Malpractice Insurance Expiry (Needs Full Date)")
        elif is_expired(expiry):
            high_risk_missing.append("Malpractice Insurance Expiry (Expired)")

    return mandatory_missing, high_risk_missing


# -------------------------------
# READINESS CALCULATION
# -------------------------------
def calculate_readiness(mandatory_missing, high_risk_missing):
    """
    Determines submission readiness score
    """

    if mandatory_missing:
        return 0
    elif high_risk_missing:
        return 80
    else:
        return 100


# -------------------------------
# TEST BLOCK
# -------------------------------
if __name__ == "__main__":
    sample_data = {
        "full_name": "Dr. Elena Ramirez",
        "npi": "1234567890",
        "specialty": "Internal Medicine",
        "license_number": "TX12345",
        "license_expiry": "June 2025",  # partial date
        "dea_number": "DEA123",
        "dea_expiry": "06/30/2026",  # valid precise
        "board_certified": True,
        "board_expiry": "2023-06-01",  # expired
        "malpractice_insurance": True,
        "malpractice_expiry": "2026-12-01"
    }

    mandatory, high_risk = evaluate_rules(sample_data)
    readiness = calculate_readiness(mandatory, high_risk)

    print("Mandatory Issues:", mandatory)
    print("High Risk Issues:", high_risk)
    print("Readiness:", readiness)