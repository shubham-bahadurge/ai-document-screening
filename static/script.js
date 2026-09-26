const documentInput = document.getElementById("document");
const fileName = document.getElementById("fileName");

documentInput.addEventListener("change", function () {

    if (this.files.length > 0) {

        fileName.textContent =
            "Selected: " + this.files[0].name;

    } else {

        fileName.textContent =
            "No file selected";
    }

});


async function screenDocument() {

    const file = documentInput.files[0];
    const result = document.getElementById("result");

    if (!file) {

        result.innerHTML = `
            <div class="card">
                <h3>⚠️ No document selected</h3>
                <p>Please choose a document first.</p>
            </div>
        `;

        return;
    }


    result.innerHTML = `
        <div class="card">
            <h2>🔄 AI Analysis Running...</h2>
            <p>Analyzing image quality and extracting document text.</p>
        </div>
    `;


    const formData = new FormData();

    formData.append("document", file);


    try {

        const response = await fetch(
            "/screen",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {
            throw new Error(
                data.error || "Screening failed"
            );
        }


        // -----------------------------
        // OCR TEXT
        // -----------------------------

        let extractedText = "";

        if (
            data.ocr_text &&
            data.ocr_text.length > 0
        ) {

            extractedText = data.ocr_text
                .map(text => `<div>• ${text}</div>`)
                .join("");

        } else {

            extractedText =
                "<div>No readable text detected.</div>";
        }


        // -----------------------------
        // SCREENING REPORT
        // -----------------------------

        result.innerHTML = `

            <div class="card">

                <h2>🔍 Screening Report</h2>


                <p>
                    <strong>Document:</strong>
                    ${data.filename}
                </p>


                <p>
                    <strong>Image Quality:</strong>
                    ${data.image_quality}
                </p>


                <p>
                    <strong>Resolution:</strong>
                    ${data.width} × ${data.height}
                </p>


                <p>
                    <strong>Blur Score:</strong>
                    ${data.blur_score}
                </p>


                <hr>


                <h3>🧠 OCR Analysis</h3>


                <p>
                    <strong>Status:</strong>
                    ${data.ocr_status}
                </p>


                <p>
                    <strong>OCR Confidence:</strong>
                    ${data.ocr_confidence}%
                </p>


                <div class="ocr-box">

                    <strong>
                        Extracted Text
                    </strong>

                    <div class="ocr-text">
                        ${extractedText}
                    </div>

                </div>


                <hr>


                <h2>
                    Risk Score:
                    ${data.risk_score}/100
                </h2>


                <h3>
                    ${data.status}
                </h3>


                <p>
                    ${data.message}
                </p>

            </div>

        `;


    } catch (error) {

        result.innerHTML = `

            <div class="card">

                <h3>❌ Screening failed</h3>

                <p>
                    ${error.message}
                </p>

            </div>

        `;
    }
}