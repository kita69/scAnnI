import os
import subprocess
from rich.console import Console

console = Console()

FLUXION_PATH = "./fluxion/fluxion.sh"

def tools_menu():
    while True:
        console.print("""
[bold cyan]\n╭────────────── Tools ──────────────╮
│ [1] Avvia Fluxion                  │
│ [0] Torna al menu principale       │
╰────────────────────────────────────╯
""")
        choice = input("Scelta: ").strip()

        if choice == "1":
            if not os.path.isfile(FLUXION_PATH):
                console.print(f"[red]❌ File Fluxion non trovato. Assicurati che sia in {FLUXION_PATH}[/red]")
                continue
            console.print("[yellow]🚀 Avvio di Fluxion...[/yellow]")
            try:
                subprocess.run(["sudo", "bash", FLUXION_PATH])
            except FileNotFoundError:
                console.print("[red]❌ Comando 'sudo' o 'bash' non disponibile nel sistema.[/red]")
        elif choice == "0":
            break
        else:
            console.print("[red]❌ Scelta non valida.[/red]")
