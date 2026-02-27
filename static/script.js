// ==========================
// FLOATING CARDS (Optimized)
// ==========================

document.addEventListener("mousemove", e => {
  document.querySelectorAll(".float-card").forEach(card => {
    const x = (window.innerWidth / 2 - e.clientX) / 40;
    const y = (window.innerHeight / 2 - e.clientY) / 40;
    card.style.transform = `translate(${x}px, ${y}px)`;
  });
});


// ==========================
// SMOOTH SCROLL
// ==========================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", e => {
    e.preventDefault();
    const target = document.querySelector(anchor.getAttribute("href"));
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  });
});


// ==========================
// LINE NUMBER FUNCTIONS
// ==========================

function addLineNumbers(code) {
    const lines = code.split("\n");
    return lines
        .map((line, index) => `${index + 1} | ${line}`)
        .join("\n");
}

function removeLineNumbers(code) {
    return code
        .split("\n")
        .map(line => line.replace(/^\d+\s\|\s/, ""))
        .join("\n");
}


// ==========================
// GENERATE CODE
// ==========================

async function generateCode() {
    try {
        const prompt = document.getElementById("promptInput").value;
        const language = document.getElementById("languageSelect").value;

        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt, language })
        });

        const data = await response.json();

        if (data.code) {
            const numberedCode = addLineNumbers(data.code);
            document.getElementById("codeBox").value = numberedCode;
        } else {
            alert("No code returned from backend.");
        }

    } catch (error) {
        console.error("Generate Error:", error);
        alert("Error generating code.");
    }
}


// ==========================
// RUN BUILD
// ==========================

async function runBuild() {
    try {
        const rawCode = document.getElementById("codeBox").value;
        const code = removeLineNumbers(rawCode);
        const language = document.getElementById("languageSelect").value;
        const logBox = document.getElementById("buildLogs");

        const response = await fetch("/build", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, language })
        });

        const data = await response.json();

        if (data.status === "success") {
            logBox.innerHTML = "Build successful ✅";
            updateAccuracy(true);
        } else {
            logBox.innerHTML = "Build failed ❌<br>" + (data.message || "");
            updateAccuracy(false);
        }

    } catch (error) {
        console.error("Build Error:", error);
        alert("Build error occurred.");
    }
}


// ==========================
// AI SUGGESTIONS
// ==========================

async function getSuggestions() {
    try {
        const rawCode = document.getElementById("codeBox").value;
        const code = removeLineNumbers(rawCode);
        const language = document.getElementById("languageSelect").value;
        const errorMessage = document.getElementById("buildLogs").innerText;
        const suggestionBox = document.getElementById("aiSuggestion");

        const response = await fetch("/suggest", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                code: code,
                language: language,
                prompt: errorMessage
            })
        });

        const data = await response.json();

        if (data.suggestion && data.suggestion.replacement_line) {
            suggestionBox.innerHTML = `
                <div style="color:#00ffe0;font-weight:bold;">
                    🔧 Line ${data.suggestion.line_number}
                </div>
                <br>
                <div style="color:#ff6b6b;">
                    ❌ ${data.suggestion.original_line}
                </div>
                <br>
                <div style="color:#00ff9c;font-weight:bold;">
                    ✅ ${data.suggestion.replacement_line}
                </div>
            `;
        } else {
            suggestionBox.innerHTML = "No precise replacement available.";
        }

    } catch (error) {
        console.error("Suggestion Error:", error);
        alert("Suggestion error occurred.");
    }
}


// ==========================
// ACCURACY ANIMATION
// ==========================

function updateAccuracy(success) {

    const accuracyValue = document.getElementById("accuracyValue");
    const canvas = document.getElementById("accuracyGraph");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    // Ensure canvas scales correctly
    canvas.width = canvas.offsetWidth;
    canvas.height = 160;

    let target = success
        ? Math.floor(Math.random() * 6) + 95
        : Math.floor(Math.random() * 20) + 60;

    let current = 0;

    const interval = setInterval(() => {

        current += 1;
        accuracyValue.innerText = current + "%";

        drawWave(ctx, canvas, current, success);

        if (current >= target) {
            clearInterval(interval);
        }

    }, 20);
}

function drawWave(ctx, canvas, accuracy, success) {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const points = [];
    const segments = 25;

    for (let i = 0; i <= segments; i++) {

        let variance = success
            ? Math.random() * 8
            : Math.random() * 25;

        const y =
            canvas.height -
            (accuracy - variance) *
            (canvas.height / 120);

        const x = (canvas.width / segments) * i;

        points.push({ x, y });
    }

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);

    for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
    }

    ctx.strokeStyle = success ? "#00ffe0" : "#ff4d4d";
    ctx.lineWidth = 3;
    ctx.shadowColor = success ? "#00ffe0" : "#ff4d4d";
    ctx.shadowBlur = 15;

    ctx.stroke();
}


// ==========================
// COPY CODE
// ==========================

function copyCode() {
    const codeBox = document.getElementById("codeBox");

    if (!codeBox.value.trim()) {
        alert("No code to copy!");
        return;
    }

    navigator.clipboard.writeText(codeBox.value)
        .then(() => {
            const btn = document.getElementById("copyBtn");
            btn.innerText = "Copied ✓";
            setTimeout(() => {
                btn.innerText = "Copy";
            }, 2000);
        })
        .catch(err => {
            console.error("Copy failed:", err);
        });
}


// ==========================
// CODE EXPLANATION
// ==========================

async function explainCode() {
    try {
        const rawCode = document.getElementById("codeBox").value;
        const language = document.getElementById("languageSelect").value;

        if (!rawCode.trim()) {
            alert("No code to explain!");
            return;
        }

        const response = await fetch("/explain", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                code: rawCode,
                language: language
            })
        });

        const data = await response.json();

        if (data.explanation) {
            document.getElementById("codeExplanation").innerHTML =
                `<div style="white-space: pre-wrap;">${data.explanation}</div>`;
        } else {
            document.getElementById("codeExplanation").innerHTML =
                "No explanation returned.";
        }

    } catch (error) {
        console.error("Explain Error:", error);
        alert("Explain error occurred.");
    }
}


// ==========================
// DOWNLOAD PROJECT
// ==========================

async function downloadProject() {
    try {
        const rawCode = document.getElementById("codeBox").value;
        const language = document.getElementById("languageSelect").value;

        if (!rawCode.trim()) {
            alert("No code to download!");
            return;
        }

        const response = await fetch("/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                code: rawCode,
                language: language
            })
        });

        if (!response.ok) {
            alert("Download failed");
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "project.zip";
        document.body.appendChild(a);
        a.click();
        a.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error("Download Error:", error);
        alert("Download error occurred.");
    }
}