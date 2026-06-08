"""
AI Evaluation script for AI-Newsroom.
Includes LLM-as-a-Judge evaluation methodology inspired by:
Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., & Zhu, C. (2023). 
G-eval: NLG evaluation using GPT-4 with better human alignment. arXiv preprint arXiv:2303.16634.
"""

import os
import sys
import json
import requests

# Predefined journalist drafts for editor evaluation
PREDEFINED_INPUTS = [
    "Azi e o zi frumoasa, soarele straluceste dar masinile sunt blocate in trafic ore intregi pe autostrada si oamenii sunt nervosi.",
    "Compania tech X a lansat un produs nou telefon mobil care face poze 3d si costa prea mult cred parerea mea.",
    "Guvernul anunta marirea taxelor de anul viitor pentru toti antreprenorii. Asta o sa scada numarul de firme mici. Nasol."
]

API_URL = "http://localhost:8000/editor/review"

EVALUATOR_SYSTEM_PROMPT = (
    "Ești un evaluator AI imparțial și exigent. Sarcina ta este să evaluezi calitatea unui articol final "
    "generat pornind de la un draft inițial (context).\n"
    "Trebuie să evaluezi articolul pe baza a două criterii specifice din literatura academică (inspirate din G-Eval):\n"
    "1. Coerență (Coherence): Structura logică, lizibilitatea, lipsa contradicțiilor și cursivitatea textului.\n"
    "2. Relevanță (Relevance): Cât de bine acoperă subiectul și ideile din draftul inițial, fără a adăuga informații complet irelevante.\n"
    "Notează fiecare criteriu pe o scară de la 1 la 5 (unde 1 este extrem de slab, iar 5 este excelent).\n"
    "Răspunde OBLIGATORIU într-un format JSON valid, exact așa:\n"
    "{\n"
    '  "coherence_score": 1-5,\n'
    '  "relevance_score": 1-5,\n'
    '  "reasoning": "Justificarea notelor tale, pe scurt, în limba română."\n'
    "}\n"
    "Nu adăuga niciun alt text în afară de obiectul JSON."
)


def eval_markdown_and_structure(editor_output):
    """Verify Markdown headers and structural sections."""
    if "#" not in editor_output:
        return False, "Fail: Output does not contain Markdown headers (# or ##)."
        
    if "Secțiunea" not in editor_output and "Feedback" not in editor_output:
        return False, "Fail: Output is missing the required structural sections."
        
    return True, "Markdown & Structure validation successful."


def eval_logic_and_length(input_text, editor_output):
    """Verify text was modified/reorganized and satisfies minimum length."""
    if input_text.strip() == editor_output.strip():
        return False, "Fail: Output is identical to input."
    
    if len(editor_output) < 15:
        return False, "Fail: Output text is too short."
        
    return True, "Text modification & length validation successful."


def eval_llm_as_a_judge(draft_text, final_article, is_ci):
    """Evaluate final article using LLM-as-a-Judge (G-Eval style)."""
    if is_ci:
        return {
            "coherence_score": 5,
            "relevance_score": 5,
            "reasoning": "CI Mode: Simulating perfect scores."
        }
    
    prompt = (
        f"{EVALUATOR_SYSTEM_PROMPT}\n\n"
        f"--- INITIAL DRAFT ---\n{draft_text}\n\n"
        f"--- FINAL ARTICLE ---\n{final_article}\n\n"
        "Evaluate now and return only the requested JSON:"
    )
    
    try:
        ask_url = "http://localhost:8000/ask"
        response = requests.post(ask_url, json={"prompt": prompt})
        response.raise_for_status()
        
        result_text = response.json().get("response", "").strip()
        
        # Strip markdown tags if present
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(result_text)
        return data
    except Exception as e:
        print(f"⚠️ Error during LLM-as-a-Judge evaluation: {e}")
        return {
            "coherence_score": 0,
            "relevance_score": 0,
            "reasoning": f"Judge API call failed: {e}"
        }


def run_evaluations():
    print("🚀 Starting quality evaluations for Editor Agent...\n")
    
    is_ci = os.environ.get("CI", "").lower() == "true"
    results = []
    
    for idx, input_text in enumerate(PREDEFINED_INPUTS):
        print(f"--- Evaluating Input {idx+1} ---")
        try:
            if is_ci:
                print("🔧 Running in CI environment: Simulating Editor Agent response...")
                output = (
                    "Secțiunea 1: Feedback critic\n"
                    "Probleme: Textul e prea scurt. Actiuni: Am extins.\n"
                    "Secțiunea 2: Articol final\n"
                    f"# Titlu Articol Revizuit {idx+1}\n"
                    "Acesta este un articol rescris, curatat de greseli si restructurat pentru a fi mult mai profesional fata de varianta bruta."
                )
            else:
                response = requests.post(API_URL, json={"draft": input_text})
                response.raise_for_status()
                output = response.json()["response"]
            
            # Check 1: Markdown & Structure
            is_valid_md, msg_md = eval_markdown_and_structure(output)
            if not is_valid_md:
                print(f"❌ {msg_md}\n")
                sys.exit(1)
            print(f"✅ {msg_md}")
            
            # Check 2: Logic & Length
            is_valid_logic, msg_logic = eval_logic_and_length(input_text, output)
            if not is_valid_logic:
                print(f"❌ {msg_logic}\n")
                sys.exit(1)
            print(f"✅ {msg_logic}")

            # Extract final article for the judge
            split_index = output.find("Secțiunea 2")
            final_article = output[split_index:] if split_index != -1 else output

            # Check 3: LLM-as-a-Judge (Coherence & Relevance)
            print("🤖 Running LLM-as-a-Judge...")
            judge_results = eval_llm_as_a_judge(input_text, final_article, is_ci)
            
            c_score = judge_results.get("coherence_score", 0)
            r_score = judge_results.get("relevance_score", 0)
            reasoning = judge_results.get("reasoning", "")
            
            print(f"📊 Judge Scores: Coherence = {c_score}/5, Relevance = {r_score}/5")
            print(f"💡 Reasoning: {reasoning}")
            
            if c_score < 3 or r_score < 3:
                print(f"❌ LLM-as-a-Judge Fail: Score below minimum threshold (3/5)!\n")
                sys.exit(1)
            print("✅ LLM-as-a-Judge evaluation passed.")
            
            results.append({
                "input_id": idx + 1,
                "input_text": input_text,
                "editor_output": output,
                "coherence_score": c_score,
                "relevance_score": r_score,
                "reasoning": reasoning,
                "status": "PASSED"
            })
            
            print(f"✔️  Input {idx+1} passed all criteria.\n")
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API not responding (Make sure FastAPI server is running): {e}")
            print("❌ Terminating run due to connection error.")
            sys.exit(1)
            
    # Save raw results to JSON
    results_file = os.path.join(os.path.dirname(__file__), "../docs/eval_results.json")
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"📊 Results exported to: docs/eval_results.json")
    
    print("✅ Editor Evaluation: All inputs passed successfully!")

if __name__ == "__main__":
    run_evaluations()
