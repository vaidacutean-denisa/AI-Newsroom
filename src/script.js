document.addEventListener("DOMContentLoaded", () => {

  let triedSubmit = false;

  const input = document.getElementById("prompt");
  const errorDiv = document.getElementById("error");
  const responseDiv = document.getElementById("response");
  const logContainer = document.getElementById("logContainer");
  const loadingDiv = document.getElementById("loading");
  const logPanel = document.getElementById("logPanel");

  /* 🔥 BUTTON reference */
  const generateBtn = document.querySelector("button");

  let currentMarkdown = "";

  function capitalizeFirst(text) {
    return text.charAt(0).toUpperCase() + text.slice(1);
  }

  /* ================= LOG ================= */
  function addLog(status, msg) {
    const time = new Date().toLocaleTimeString();

    const div = document.createElement("div");
    div.className = "log-item";
    div.textContent = `[${time}] [${status}] ${msg}`;

    logContainer.appendChild(div);
  }

  /* ================= PARSE EDITOR ================= */
  function parseEditor(text) {
    let feedback = "";
    let final = "";

    const splitIndex = text.indexOf("Secțiunea 2");

    if (splitIndex !== -1) {
      feedback = text.substring(0, splitIndex);
      final = text.substring(splitIndex);
    } else {
      final = text;
    }

    return { feedback, final };
  }

  /* ================= FORMAT ================= */
  function formatText(text) {
    return text
      .replace(/---+/g, "")
      .replace(/^# (.*)$/gm, '<h2 style="font-weight: normal;">$1</h2>')
      .replace(/^## (.*)$/gm, '<h3>$1</h3>')
      .replace(/\n{2,}/g, "<br><br>")
      .replace(/\n/g, "<br>");
  }

  /* ================= SECTION ================= */
  function createSection(title, content) {
    const id = "sec-" + Math.random().toString(36).slice(2);

    return `
      <div class="block">
        <div class="block-title" onclick="toggleSection('${id}')">
          ${title} <span id="arrow-${id}">▼</span>
        </div>

        <div id="${id}" class="block-content">
          ${formatText(content)}
        </div>
      </div>
    `;
  }

  function toggleSection(id) {
    const el = document.getElementById(id);
    const arrow = document.getElementById("arrow-" + id);

    if (el.style.display === "none") {
      el.style.display = "block";
      arrow.innerText = "▼";
    } else {
      el.style.display = "none";
      arrow.innerText = "▶";
    }
  }

  window.toggleSection = toggleSection;

  /* ================= LOG TOGGLE ================= */
  function toggleLogs() {
    const arrow = document.getElementById("arrow");

    logPanel.classList.toggle("closed");
    arrow.innerText = logPanel.classList.contains("closed") ? "▶" : "▼";
  }

  window.toggleLogs = toggleLogs;

  /* ================= COPY ================= */
  function copyArticle() {
    navigator.clipboard.writeText(currentMarkdown);
    alert("Copied to clipboard!");
  }

  window.copyArticle = copyArticle;

  /* ================= PDF ================= */
  function exportPDF() {
    const win = window.open("", "_blank");

    win.document.write(`
      <html>
        <body>
          <pre style="font-family: Georgia; white-space: pre-wrap;">
${currentMarkdown}
          </pre>
        </body>
      </html>
    `);

    win.document.close();
    win.print();
  }

  window.exportPDF = exportPDF;

  /* ================= INPUT ================= */
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") askAI();
  });

  input.addEventListener("input", () => {
    if (triedSubmit) errorDiv.style.display = "none";
  });

  /* ================= MAIN ================= */
  async function askAI() {
    triedSubmit = true;

    const prompt = input.value.trim();

    if (!prompt) {
      errorDiv.style.display = "block";
      return;
    }

    errorDiv.style.display = "none";

    /* 🔥 DISABLE BUTTON */
    generateBtn.disabled = true;
    generateBtn.innerText = "Generating...";

    logContainer.innerHTML = "";
    responseDiv.innerHTML = "";
    responseDiv.style.display = "none";
    loadingDiv.style.display = "flex";

    addLog("RUNNING", "Jurnalistul scrie...");
    await new Promise(r => setTimeout(r, 400));

    addLog("RUNNING", "Editorul analizează...");
    await new Promise(r => setTimeout(r, 400));

    const startTime = Date.now();
    addLog("RUNNING", "Trimite request...");

    try {
      const res = await fetch("http://localhost:8000/article/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });

      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();

      const draft = data.draft || "";
      const finalRaw = data.final_article || "";

      const { feedback, final } = parseEditor(finalRaw);

      currentMarkdown = finalRaw;

      const endTime = Date.now();
      const duration = ((endTime - startTime) / 1000).toFixed(1);

      loadingDiv.style.display = "none";
      responseDiv.style.display = "block";

      responseDiv.innerHTML =
        `<h2>${capitalizeFirst(prompt)}</h2>` +
        createSection("Input utilizator", prompt) +
        createSection("Draft (Jurnalist)", draft) +
        createSection("Feedback (Editor)", feedback) +
        createSection("Articol final", final) +
        `
        <div style="display:flex; gap:10px; margin-top:15px;">
          <button onclick="copyArticle()">📋 Copy text</button>
          <button onclick="exportPDF()">📄 Export PDF</button>
        </div>
        `;

      addLog("DONE", `Articol generat în ${duration}s`);

    } catch (err) {
      loadingDiv.style.display = "none";
      responseDiv.style.display = "block";
      responseDiv.innerHTML = "Error connecting to backend.";

      addLog("ERROR", "Eroare");

    } finally {
      /* 🔥 RE-ENABLE BUTTON */
      generateBtn.disabled = false;
      generateBtn.innerText = "Generate";
    }
  }

  window.askAI = askAI;
});