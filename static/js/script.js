const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("pdfFile");
const sendBtn = document.getElementById("sendBtn");
const questionInput = document.getElementById("question");
const chatBox = document.getElementById("chat-box");
const pdfViewer = document.getElementById("pdfViewer");

const summaryBtn = document.getElementById("summaryBtn");
const riskBtn = document.getElementById("riskBtn");
const clausesBtn = document.getElementById("clausesBtn");
const datesBtn = document.getElementById("datesBtn");

const suggestions = document.getElementById("suggestions");


// =====================================
// Upload PDF
// =====================================


   uploadBtn.addEventListener("click", async () => {

    if (fileInput.files.length === 0) {
        alert("Please choose a PDF.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {

        console.log("Uploading PDF...");

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        console.log("Status:", response.status);

        const text = await response.text();

        console.log("Server Response:", text);

        let data;

        try {
            data = JSON.parse(text);
        } catch (e) {
            alert("Server returned invalid response.\n\n" + text);
            return;
        }

        if (!response.ok) {
            alert(data.error || "Upload failed");
            return;
        }

        pdfViewer.src = data.pdf_url;

        suggestions.style.display = "block";

        chatBox.innerHTML += `
    <div class="bot-message">
        <strong>✅ Document Uploaded Successfully</strong>
        <br><br>
        <b>File:</b> ${data.filename}<br>
        <b>Size:</b> ${data.size} bytes
    </div>
`;

    } catch (err) {

        console.error(err);

        alert("Network Error:\n\n" + err);

    }

});


// =====================================
// Ask Question
// =====================================

async function askQuestion() {

    const question = questionInput.value.trim();

    if (question === "") return;

    chatBox.innerHTML += `
        <div class="user-message">
            ${question}
        </div>
    `;

    questionInput.value = "";

    chatBox.innerHTML += `
        <div class="bot-message loading" id="loadingMessage">
            🤖 AI is analyzing your document...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        const loading = document.getElementById("loadingMessage");

        if (loading) {
            loading.remove();
        }

        chatBox.innerHTML += `
            <div class="bot-message">

                ${marked.parse(data.answer)}

                <hr>

                <div class="sources">

                    <strong>📄 Sources Used</strong>

                    <ul>

                        ${data.sources
                            .map(source => `<li>${source}</li>`)
                            .join("")}

                    </ul>

                </div>

            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

    }

    catch (error) {

        console.error(error);

        const loading = document.getElementById("loadingMessage");

        if (loading) {
            loading.remove();
        }

        chatBox.innerHTML += `
            <div class="bot-message">
                ❌ Unable to get a response from the AI.
            </div>
        `;

    }

}


// =====================================
// Send Button
// =====================================

sendBtn.addEventListener("click", askQuestion);


// =====================================
// Press Enter
// =====================================

questionInput.addEventListener("keypress", function (e) {

    if (e.key === "Enter") {

        askQuestion();

    }

});


// =====================================
// Preset Questions
// =====================================

function askPreset(question) {

    questionInput.value = question;

    askQuestion();

}


// =====================================
// Sidebar Buttons
// =====================================

summaryBtn.addEventListener("click", () => {

    askPreset("Give a detailed summary of this legal document.");

});

riskBtn.addEventListener("click", () => {

    askPreset("Identify all legal risks in this document.");

});

clausesBtn.addEventListener("click", () => {

    askPreset("List all important clauses in this legal document.");

});

datesBtn.addEventListener("click", () => {

    askPreset("Extract every important date mentioned in this document.");

});


// =====================================
// Suggested Questions
// =====================================

const suggestionButtons = document.querySelectorAll(".suggestion-btn");

suggestionButtons.forEach(button => {

    button.addEventListener("click", () => {

        questionInput.value = button.textContent.trim();

        askQuestion();

    });

});