import sys
import requests

# Cele 3 inputuri predefinite pentru verificarea Editorului (drafturi jurnalist)
PREDEFINED_INPUTS = [
    "Azi e o zi frumoasa, soarele straluceste dar masinile sunt blocate in trafic ore intregi pe autostrada si oamenii sunt nervosi.",
    "Compania tech X a lansat un produs nou telefon mobil care face poze 3d si costa prea mult cred parerea mea.",
    "Guvernul anunta marirea taxelor de anul viitor pentru toti antreprenorii. Asta o sa scada numarul de firme mici. Nasol."
]

API_URL = "http://localhost:8000/editor/review"

def eval_markdown_and_structure(editor_output):
    """Verifica prezenta tag-urilor Markdown (#, ##) si structurii logice."""
    if "#" not in editor_output:
        return False, "Esec: Output-ul nu contine Markdown (# sau ##)."
    if not editor_output.strip().startswith("#"):
        return False, "Esec: Output-ul nu este structurat cu un titlu la inceput."
    return True, "Validare Markdown & Structura incheiata cu succes."

def run_evaluations():
    print("🚀 Incepere evaluare calitate pentru Agent Editor...\n")
    
    for idx, input_text in enumerate(PREDEFINED_INPUTS):
        print(f"--- Evaluare Input {idx+1} ---")
        try:
            response = requests.post(API_URL, json={"draft": input_text})
            response.raise_for_status()
            output = response.json()["response"]
            
            # Verificare: Markdown si Structura
            is_valid, msg = eval_markdown_and_structure(output)
            if not is_valid:
                print(f"❌ {msg}\n")
                sys.exit(1)
            print(f"✅ {msg}")
            
            # (Validarile logice vor fi adaugate in commit-ul urmator)
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API-ul nu raspunde (Asigura-te ca serverul FastAPI ruleaza): {e}")
            print("❌ Opreste rularea din cauza erorii de conexiune.")
            sys.exit(1)
            
    print("\n✅ Evaluare Editor: Toate textele au trecut cu succes!")

if __name__ == "__main__":
    run_evaluations()
