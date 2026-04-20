def get_empty_form():

    return {
        # -------------------------------
        # SECTION 1 — PERSONAL INFO
        # -------------------------------
        "first_name": "",
        "last_name": "",
        "full_name": "",
        "dob": "",
        "gender": "",
        "phone": "",
        "email": "",
        "address": "",

        "npi": "",
        "specialty": "",

        # -------------------------------
        # SECTION 2 — LICENSE
        # -------------------------------
        "license_number": "",
        "license_expiry": "",

        "dea_number": "",
        "dea_expiry": "",

        # -------------------------------
        # SECTION 4 — BOARD CERTIFICATION
        # -------------------------------
        "board_certified": False,
        "board_expiry": "",

        # -------------------------------
        # SECTION 6 — PRACTICE
        # -------------------------------
        "practice_name": "",
        "tin": "",
        "medicaid_id": "",

        # -------------------------------
        # SECTION 7 — MALPRACTICE
        # -------------------------------
        "malpractice_insurance": False,
        "malpractice_expiry": ""
    }