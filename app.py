from flask import Flask, render_template, request, jsonify
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/screen", methods=["POST"])
def screen_document():

    if "document" not in request.files:
        return jsonify({"error": "No document uploaded"}), 400

    file = request.files["document"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    image = cv2.imread(filepath)

    if image is None:
        return jsonify({"error": "Invalid image file"}), 400

    height, width = image.shape[:2]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    quality = "Good"
    risk = 10

    if width < 500 or height < 300:
        quality = "Low"
        risk += 25

    if blur_score < 100:
        quality = "Blurry"
        risk += 30

    if risk < 30:
        status = "Low Risk"
    elif risk < 60:
        status = "Medium Risk"
    else:
        status = "High Risk"

    return jsonify({
        "filename": file.filename,
        "width": width,
        "height": height,
        "image_quality": quality,
        "blur_score": round(blur_score, 2),
        "risk_score": min(risk, 100),
        "status": status,
        "message": "Automated screening only. Final identity verification requires authoritative verification."
    })


if __name__ == "__main__":
    app.run(debug=True)