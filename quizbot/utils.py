def validate_question(text):
    if not text or len(text.strip()) < 5:
        return False, "❌ Savol juda qisqa! Kamida 5 ta belgi kiriting."
    if len(text) > 500:
        return False, "❌ Savol juda uzun! Maksimal 500 ta belgi."
    return True, ""

def validate_option(text, option_name):
    if not text or len(text.strip()) < 1:
        return False, f"❌ {option_name} varianti bo'sh bo'lishi mumkin emas!"
    if len(text) > 200:
        return False, f"❌ {option_name} varianti juda uzun! Maksimal 200 ta belgi."
    return True, ""