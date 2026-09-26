import os
import ssl

import certifi
import easyocr


# Fix Python SSL certificate verification
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass


_reader = None


def get_reader():

    global _reader

    if _reader is None:

        _reader = easyocr.Reader(
            ["en"],
            gpu=False,
            verbose=True
        )

    return _reader


def extract_text(image_path):

    reader = get_reader()

    results = reader.readtext(
        image_path
    )

    detected_text = []
    confidences = []

    for result in results:

        text = result[1]
        confidence = float(result[2])

        detected_text.append(text)
        confidences.append(confidence)


    if confidences:

        average_confidence = (
            sum(confidences)
            / len(confidences)
        ) * 100

    else:

        average_confidence = 0


    return {
        "text": detected_text,
        "confidence": round(
            average_confidence,
            2
        ),
        "count": len(
            detected_text
        )
    }