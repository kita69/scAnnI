import subprocess
import shutil
import requests
from rich import print
from utils import config_ai

ollama_available = False
msfconsole_available = False


def check_command_exists(command):
    return shutil.which(command) is not None

def is_ollama_api_active():
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    except:
        return False

def check_msfconsole():
    global msfconsole_available
    if check_command_exists("msfconsole"):
        print("[green]✅ msfconsole trovato. Generazione database exploit...[/green]")
        try:
            from utils.exploit_utils import parse_exploit_names
            output = subprocess.getoutput('msfconsole -q -x "show exploits; exit"')
            names = parse_exploit_names(output)
            with open("exploit_list.txt", "w") as f:
                f.write("\n".join(names))
            msfconsole_available = True
        except Exception as e:
            print(f"[red]❌ Errore durante l'aggiornamento del database exploit: {e}[/red]")
    else:
        print("[yellow]⚠️ msfconsole non trovato. L'esecuzione degli exploit automatici e manuali sarà disabilitata.[/yellow]")


def check_ollama():
    global ollama_available
    if is_ollama_api_active():
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            models = [line.split()[0] for line in result.stdout.strip().splitlines() if line and not line.startswith("NAME")]
            if not models:
                raise ValueError("Nessun modello AI trovato")

            print("[green]✅ Ollama trovato. Modelli disponibili:[/green]")
            for i, model in enumerate(models, 1):
                print(f"{i}. {model}")

            if len(models) == 1:
                config_ai.AI_MODEL_DEFAULT = models[0]
                config_ai.AI_MODEL_CODE = models[0]
                print(f"[cyan]✔️ Modello impostato: {models[0]} (default e exploit)[/cyan]")
            else:
                def choose_model(message):
                    while True:
                        raw = input(message).strip()
                        if raw.isdigit() and 1 <= int(raw) <= len(models):
                            return models[int(raw) - 1]
                        print(f"[yellow]⚠️ Inserisci un numero tra 1 e {len(models)}.[/yellow]")

                config_ai.AI_MODEL_DEFAULT = choose_model("🔹 Seleziona il modello AI generale (numero): ")
                config_ai.AI_MODEL_CODE = choose_model("🔸 Seleziona il modello per exploit (numero): ")
                print("[cyan]✔️ Modelli configurati correttamente.[/cyan]")

            ollama_available = True

        except Exception as e:
            print(f"[red]❌ Errore nel caricamento dei modelli AI: {e}[/red]")
            print("[yellow]⚠️ L'assistenza AI sarà disattivata. Proseguo senza suggerimenti automatici.[/yellow]")
    else:
        print("[yellow]❌ Ollama non trovato o API non attiva. L'assistenza AI sarà disattivata. Premi Invio per continuare...[/yellow]")
        input()


def startup_check():
    print("[bold magenta]\n🔎 Controllo strumenti in corso...[/bold magenta]")
    check_msfconsole()
    check_ollama()
    print("[bold magenta]\n✅ Controllo completato. Avvio di scAnnI...[/bold magenta]\n")

    return {
        "ollama": ollama_available,
        "msfconsole": msfconsole_available
    }
