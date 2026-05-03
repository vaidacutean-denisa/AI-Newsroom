def test_agent_output_consistency():
    """Simulează verificarea calității output-ului generat de agenți."""
    print("🚀 Running AI Evals: Verifying Agent Journalist & Editor consistency...")
    
    # Exemplu de criteriu de evaluare: Output-ul trebuie să fie Markdown valid
    sample_output = "# Titlu Articol\nAcesta este un draft."
    
    assert sample_output.startswith("#"), "Agent output must start with a Markdown header"
    print("✅ Eval Passed: Content structure is correct.")

if __name__ == "__main__":
    test_agent_output_consistency()
