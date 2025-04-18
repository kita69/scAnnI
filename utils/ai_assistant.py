import requests
from rich.console import Console
from utils.config_ai import AI_MODEL_DEFAULT

console = Console()

def ai_assistant(session_memory):
    console.print("\n[bold green]🤖 Modalità assistente AI attiva (scrivi 'exit' per uscire)[/bold green]")

    context = """Sei un assistente per un penetration tester. Rispondi in modo tecnico e professionale.
Ecco i dati raccolti finora:
"""
    if session_memory["targets"]:
        context += f"Target analizzati: {', '.join(session_memory['targets'])}\n"
    if session_memory["suggested_modules"]:
        context += f"Moduli suggeriti: {', '.join(session_memory['suggested_modules'])}\n"
    if session_memory["executed_exploits"]:
        context += f"Exploit eseguiti: {', '.join(session_memory['executed_exploits'])}\n"

    context += "\nPuoi fornire suggerimenti, raccomandazioni o strategie."

    while True:
        user_input = input("👤 Tu > ").strip()
        if user_input.lower() == "exit":
            break

        prompt = f"{context}\n\nDomanda: {user_input}\nRisposta in italiano tecnico:"

        try:
            res = requests.post("http://localhost:11434/api/generate", json={
                "model": AI_MODEL_DEFAULT,
                "prompt": prompt,
                "stream": False
            })
            reply = res.json().get("response", "[Nessuna risposta dalla AI]")
        except Exception as e:
            reply = f"❌ Errore: {e}"

        print(f"\n🤖 AI > {reply}\n")

def ask_ai(prompt, model=AI_MODEL_DEFAULT):
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        return res.json().get("response", "[Nessuna risposta dalla AI]")
    except Exception as e:
        return f"[Errore AI]: {e}"
