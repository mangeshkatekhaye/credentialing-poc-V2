def validate_data(data):
    issues = []

    if not data.get("Full Name"):
        issues.append("❌ Full Name is missing")

    if not data.get("Email"):
        issues.append("❌ Email is missing")

    if not data.get("Phone Number"):
        issues.append("❌ Phone Number is missing")

    if not data.get("Skills"):
        issues.append("⚠️ Skills not found")

    # 🔥 Improved Experience Check
    experience = (
        data.get("Total Experience (years)") or
        data.get("Total Experience") or
        data.get("Experience")
    )

    if not experience:
        issues.append("⚠️ Total Experience not identified")

    return issues