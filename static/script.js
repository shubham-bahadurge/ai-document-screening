async function screenDocument() {

    const file =
        document.getElementById("document").files[0];

    const result =
        document.getElementById("result");

    if (!file) {
        result.innerHTML =
            "<div class='card'><h3>⚠️ Please select a document.</h3></div>";
        return;
    }

    result.innerHTML =
        "<div class='card'><h2>🔄 Analyzing document...</h2><p>Please wait.</p></div>";

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
            throw new Error(data.error);
        }

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

                <h2>
                    Risk Score: ${data.risk_score}/100
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
                <p>${error.message}</p>
            </div>
        `;
    }
}