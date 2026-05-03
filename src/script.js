document.addEventListener("DOMContentLoaded", () => {
    let triedSubmit = false;
  
    const input = document.getElementById("prompt");
    const errorDiv = document.getElementById("error");
    const responseDiv = document.getElementById("response");
    const logContainer = document.getElementById("logContainer");
    const loadingDiv = document.getElementById("loading");
    const logPanel = document.getElementById("logPanel");
  
    function capitalizeFirst(text) {
      return text.charAt(0).toUpperCase() + text.slice(1);
    }
  
    // ================= LOG SYSTEM =================
    function addLog(status, msg) {
      const time = new Date().toLocaleTimeString();
  
      const div = document.createElement("div");
      div.className = "log-item";
      div.textContent = `[${time}] [${status}] ${msg}`;
  
      logContainer.appendChild(div);
      logContainer.scrollTop = logContainer.scrollHeight;
    }
  
    // ================= TOGGLE LOGS =================
    function toggleLogs() {
      const arrow = document.getElementById("arrow");
  
      logPanel.classList.toggle("closed");
      arrow.innerText = logPanel.classList.contains("closed") ? "▶" : "▼";
    }
  
    window.toggleLogs = toggleLogs;
  
    // ================= INPUT EVENTS =================
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") askAI();
    });
  
    input.addEventListener("input", () => {
      if (triedSubmit) {
        errorDiv.style.display = "none";
      }
    });
  
    function wait(ms) {
      return new Promise(r => setTimeout(r, ms));
    }
  
    // ================= MAIN FUNCTION =================
    async function askAI() {
      triedSubmit = true;
  
      const prompt = input.value.trim();
  
      if (!prompt) {
        errorDiv.style.display = "block";
        errorDiv.innerText = "Please enter a topic.";
        return;
      }
  
      errorDiv.style.display = "none";
  
      // reset UI
      logContainer.innerHTML = "";
      responseDiv.innerHTML = "";
      responseDiv.style.display = "none";
      loadingDiv.style.display = "flex";
  
      try {
  
        addLog("RUNNING", "Jurnalistul scrie...");
        await wait(700);
  
        addLog("RUNNING", "Editorul analizează...");
        await wait(700);
  
        // ================= REAL REQUEST =================
        const res = await fetch("http://localhost:8000/article/generate", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ prompt })
        });
  
        if (!res.ok) throw new Error("Backend error");
  
        const data = await res.json();
  
        const draft = data.draft || "";
        const final = data.final_article || "";
  
        loadingDiv.style.display = "none";
        responseDiv.style.display = "block";
  
        responseDiv.innerHTML = `
          <h2>${capitalizeFirst(prompt)}</h2>
  
          <div class="section">
            <h3>Agent 1 - Draft</h3>
            <p>${draft.replace(/\n/g, "<br>")}</p>
          </div>
  
          <div class="section">
            <h3>Agent 2 - Final Article</h3>
            <p>${final.replace(/\n/g, "<br>")}</p>
          </div>
        `;
  
        addLog("DONE", "Articol generat cu succes");
  
      } catch (err) {
        loadingDiv.style.display = "none";
        responseDiv.style.display = "block";
        responseDiv.innerHTML = "Error connecting to backend.";
  
        addLog("ERROR", "Pipeline failed");
      }
    }
  
    window.askAI = askAI;
  });