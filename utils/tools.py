import subprocess
from rich.console import Console

console = Console()

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
            console.print("[yellow]🚀 Avvio di Fluxion...[/yellow]")
            try:
                subprocess.run(["sudo", "bash", "./fluxion/fluxion.sh"])
            except FileNotFoundError:
                console.print("[red]❌ File Fluxion non trovato. Assicurati che sia in ./fluxion/fluxion.sh[/red]")
        elif choice == "0":
            break
        else:
            console.print("[red]❌ Scelta non valida.[/red]")
