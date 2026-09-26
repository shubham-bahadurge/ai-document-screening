import re


def analyze_consistency(ocr_text):
    """
    Analyze OCR text for basic document consistency indicators.
    This is a screening aid, not proof of authenticity.
    """

    if not ocr_text:
        return {
            "status": "Insufficient Data",
            "score": 0,
            "indicators": [],
            "text_length": 0
        }

    # Combine OCR results
    text = " ".join(ocr_text)

    indicators = []
    score = 0

    # -----------------------------
    # TEXT LENGTH
    # -----------------------------

    if len(text) < 20:
        indicators.append("Very little readable text detected")
        score += 20

    elif len(text) < 50:
        indicators.append("Limited readable text detected")
        score += 10

    else:
        indicators.append("Sufficient readable text detected")

    # -----------------------------
    # SPECIAL CHARACTER CHECK
    # -----------------------------

    unusual_chars = re.findall(
        r"[^A-Za-z0-9\s.,:/()\-@]",
        text
    )

    if len(unusual_chars) > 10:
        indicators.append("High number of unusual characters")
        score += 15
    else:
        indicators.append("Character pattern appears normal")

    # -----------------------------
    # NUMBER CHECK
    # -----------------------------

    numbers = re.findall(r"\d+", text)

    if numbers:
        indicators.append(
            f"Numeric content detected ({len(numbers)} group(s))"
        )
    else:
        indicators.append("No numeric content detected")
        score += 5

    # -----------------------------
    # REPEATED TEXT CHECK
    # -----------------------------

    words = text.lower().split()

    repeated_words = set(
        word for word in words
        if words.count(word) > 2 and len(word) > 2
    )

    if repeated_words:
        indicators.append("Repeated text patterns detected")
        score += 10
    else:
        indicators.append("No excessive repeated text detected")

    # -----------------------------
    # FINAL STATUS
    # -----------------------------

    score = min(score, 100)

    if score < 20:
        status = "Consistent"

    elif score < 40:
        status = "Review Recommended"

    else:
        status = "Potential Inconsistency"

    return {
        "status": status,
        "score": score,
        "indicators": indicators,
        "text_length": len(text)
    }
