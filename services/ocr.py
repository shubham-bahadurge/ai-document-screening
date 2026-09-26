import easyocr

_reader = None


def get_reader():
    global _reader

    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=False)

    return _reader


def extract_text(image_path):
    reader = get_reader()

    results = reader.readtext(image_path)

    detected_text = []
    confidences = []

    for result in results:
        text = result[1]
        confidence = float(result[2])

        detected_text.append(text)
        confidences.append(confidence)

    if confidences:
        average_confidence = (
            sum(confidences) / len(confidences)
        ) * 100
    else:
        average_confidence = 0

    return {
        "text": detected_text,
        "confidence": round(average_confidence, 2),
        "count": len(detected_text)
    }