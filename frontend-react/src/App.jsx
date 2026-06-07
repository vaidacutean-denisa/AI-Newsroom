import { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [logs, setLogs] = useState([]);
  const [result, setResult] = useState(null);
  const [currentMarkdown, setCurrentMarkdown] = useState("");

  const [openSections, setOpenSections] = useState({
    draft: true,
    feedback: true,
    final: true,
  });

  const [logsOpen, setLogsOpen] = useState(true);

  const addLog = (status, msg) => {
    const time = new Date().toLocaleTimeString();
    setLogs((prev) => [...prev, `[${time}] [${status}] ${msg}`]);
  };

  const capitalizeFirst = (text = "") =>
    text.charAt(0).toUpperCase() + text.slice(1);

  const safeText = (t) => (t ? String(t) : "");

  const parseEditor = (text = "") => {
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
  };

  const formatText = (text = "") =>
    safeText(text)
      .replace(/---+/g, "")
      .replace(/\n{2,}/g, "\n\n");

  const toggleSection = (key) => {
    setOpenSections((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const copyArticle = () => {
    navigator.clipboard.writeText(currentMarkdown || "");
  };

  const exportPDF = () => {
    const win = window.open("", "_blank");
    win.document.write(`
      <html>
        <body>
          <pre style="font-family: Georgia; white-space: pre-wrap;">
${currentMarkdown || ""}
          </pre>
        </body>
      </html>
    `);
    win.document.close();
    win.print();
  };

  const askAI = async () => {
    if (!prompt.trim()) {
      setError("Please enter a topic.");
      return;
    }

    setError("");
    setLoading(true);
    setLogs([]);
    setResult(null);

    addLog("RUNNING", "Jurnalist...");
    addLog("RUNNING", "Editor...");
    addLog("RUNNING", "Request...");

    try {
      const startTime = Date.now();
    
      const res = await fetch("http://localhost:8000/article/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
    
      if (!res.ok) throw new Error(await res.text());
    
      const data = await res.json();
    
      const draft = data?.draft ?? "";
      const finalRaw = data?.final_article ?? "";
    
      const { feedback, final } = parseEditor(finalRaw);
    
      setCurrentMarkdown(finalRaw);
    
      setResult({
        title: capitalizeFirst(prompt),
        prompt,
        draft,
        feedback,
        final,
      });
    
      const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    
      addLog(
        "DONE",
        `Articol generat în ${duration} secunde`
      );
    
    } catch (e) {
      addLog("ERROR", "Backend/Ollama fail");
      setResult({
        title: "Error",
        prompt: "",
        draft: "",
        feedback: "",
        final: "Backend/Ollama nu răspunde.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>AI Newsroom</h1>
      </header>

      <div className="input-card">
        <div className="prompt-line">
          Generate article about{" "}
          <input value={prompt} onChange={(e) => setPrompt(e.target.value)} />
        </div>

        <button onClick={askAI} disabled={loading}>
          {loading ? "Generating..." : "Generate"}
        </button>

        {error && <div className="error">{error}</div>}
      </div>

      <div className="container">
        {result && (
          <div className="article-box">
            <h2 className="title">{result.title}</h2>

            {/* DRAFT */}
            <div className="block">
              <div
                className="block-title"
                onClick={() => toggleSection("draft")}
              >
                <span>📰 Draft (Jurnalist)</span>
                <span>{openSections.draft ? "▼" : "▶"}</span>
              </div>

              {openSections.draft && (
                <div className="block-content newspaper-content">
                  {formatText(result.draft)}
                </div>
              )}
            </div>

            {/* FEEDBACK */}
            <div className="block">
              <div
                className="block-title"
                onClick={() => toggleSection("feedback")}
              >
                <span>✏️ Feedback (Editor)</span>
                <span>{openSections.feedback ? "▼" : "▶"}</span>
              </div>

              {openSections.feedback && (
                <div className="block-content newspaper-content">
                  {formatText(result.feedback)}
                </div>
              )}
            </div>

            {/* FINAL */}
            <div className="block">
              <div
                className="block-title"
                onClick={() => toggleSection("final")}
              >
                <span>📄 Articol Final</span>
                <span>{openSections.final ? "▼" : "▶"}</span>
              </div>

              {openSections.final && (
                <div className="block-content newspaper-content">
                  {formatText(result.final)}
                </div>
              )}
            </div>

            <div className="actions">
              <button onClick={copyArticle}>Copy</button>
              <button onClick={exportPDF}>PDF</button>
            </div>
          </div>
        )}
      </div>

      {/* LOGS */}
      <div className={`log-panel ${logsOpen ? "open" : "closed"}`}>
        <div className="log-toggle" onClick={() => setLogsOpen(!logsOpen)}>
          {logsOpen ? "▼ Logs" : "▲"}
        </div>

        {logsOpen && (
          <div id="logContainer">
            {logs.map((l, i) => (
              <div key={i} className="log-item">
                {l}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;