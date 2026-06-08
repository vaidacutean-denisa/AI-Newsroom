"""
Report generator script for AI-Newsroom.
Runs the evaluations and compiles a formatted Markdown report docs/eval_report.md
containing scores and justifications.
"""

import os
import sys
import json
import subprocess
from datetime import datetime

def run_evaluations_subprocess():
    """Runs scripts/ai_evals.py to populate docs/eval_results.json"""
    print("⏳ Running evaluation pipeline (ai_evals.py)...")
    ai_evals_path = os.path.join(os.path.dirname(__file__), "ai_evals.py")
    
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    try:
        result = subprocess.run(
            [sys.executable, ai_evals_path],
            capture_output=True,
            text=True,
            env=env,
            encoding="utf-8"
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Evaluation pipeline failed:\n{result.stderr}")
            sys.exit(result.returncode)
    except Exception as e:
        print(f"❌ Failed to run evaluation script: {e}")
        sys.exit(1)

def generate_report():
    # Run evaluation first to gather fresh results
    run_evaluations_subprocess()
    
    results_path = os.path.join(os.path.dirname(__file__), "../docs/eval_results.json")
    report_path = os.path.join(os.path.dirname(__file__), "../docs/eval_report.md")
    
    if not os.path.exists(results_path):
        print(f"❌ Results file {results_path} was not found.")
        sys.exit(1)
        
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    if not results:
        print("❌ No evaluation results found in file.")
        sys.exit(1)
        
    # Calculate statistics
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["status"] == "PASSED")
    avg_coherence = sum(r["coherence_score"] for r in results) / total_tests
    avg_relevance = sum(r["relevance_score"] for r in results) / total_tests
    
    is_ci = os.environ.get("CI", "").lower() == "true"
    env_name = "GitHub Actions (CI)" if is_ci else "Local Workspace"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build Markdown report
    md = []
    md.append("# 📊 AI Evaluation Report (G-Eval / LLM-as-a-Judge)\n")
    md.append(f"This report was automatically generated on **{timestamp}** in **{env_name}** environment.\n")
    
    md.append("## 📈 Executive Summary\n")
    md.append("| Metric | Value | Status |")
    md.append("| :--- | :--- | :--- |")
    md.append(f"| Scenarios Tested | **{total_tests}** | - |")
    md.append(f"| Pass Rate | **{passed_tests / total_tests * 100:.1f}%** | {'✅ Success' if passed_tests == total_tests else '❌ Failure'} |")
    md.append(f"| Average Coherence | **{avg_coherence:.2f} / 5.0** | {'💚 Excellent' if avg_coherence >= 4.0 else '💛 Satisfactory'} |")
    md.append(f"| Average Relevance | **{avg_relevance:.2f} / 5.0** | {'💚 Excellent' if avg_relevance >= 4.0 else '💛 Satisfactory'} |\n")
    
    md.append("---\n")
    md.append("## 🔍 Scenario Breakdown\n")
    
    for r in results:
        input_id = r["input_id"]
        input_text = r["input_text"]
        coherence = r["coherence_score"]
        relevance = r["relevance_score"]
        reasoning = r["reasoning"]
        
        md.append(f"### Scenario {input_id}: \"*{input_text}*\"\n")
        md.append(f"* **Coherence Score**: `{coherence} / 5`")
        md.append(f"* **Relevance Score**: `{relevance} / 5`")
        md.append(f"* **Status**: `{'✅ PASSED' if coherence >= 3 and relevance >= 3 else '❌ FAILED'}`")
        md.append("* **Judge Reasoning**:")
        md.append(f"  > {reasoning}\n")
        
        editor_output = r["editor_output"]
        split_index = editor_output.find("Secțiunea 2")
        final_article = editor_output[split_index:] if split_index != -1 else editor_output
        
        snippet = final_article.replace("\n", "\n  ").strip()
        md.append("  <details>")
        md.append("  <summary>Show generated final article</summary>")
        md.append(f"\n  {snippet}\n")
        md.append("  </details>\n")
        md.append("--- \n")
        
    md.append("\n*Report generated via `scripts/generate_eval_report.py` based on methodology in `docs/EVALUATION.md`.*")
    
    # Write Markdown file
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
        
    print("🎉 Markdown report successfully generated at: docs/eval_report.md")

if __name__ == "__main__":
    generate_report()
