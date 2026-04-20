def calculate_progress(data):
    total_fields = 0
    filled_fields = 0

    for key, value in data.items():
        total_fields += 1

        if isinstance(value, bool):
            if value:
                filled_fields += 1
        else:
            if value not in ["", None]:
                filled_fields += 1

    return int((filled_fields / total_fields) * 100)