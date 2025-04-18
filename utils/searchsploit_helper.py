import os
import subprocess
from rich import print
from rich.console import Console
from rich.panel import Panel

SCANS_DIR = "scans"
console = Console()

def run_searchsploit():
    if not os.path.exists(SCANS_DIR):
        print("[red]❌ Nessuna directory scans presente.[/red]")
        return

    dirs = sorted(os.listdir(SCANS_DIR))
    if not dirs:
        print("[red]❌ Nessuna scansione trovata.[/red]")
        return

    latest = os.path.join(SCANS_DIR, dirs[-1])
    nmap_file = os.path.join(latest, "nmap_scan.txt")

    if not os.path.isfile(nmap_file):
        print(f"[red]❌ File Nmap non trovato in {latest}[/red]")
        return

    print(f"\n[cyan]📦 Esecuzione searchsploit su:[/cyan] {nmap_file}\n")

    try:
        result = subprocess.run([
            "searchsploit", "--nmap", nmap_file
        ], capture_output=True, text=True, timeout=60)

        output = result.stdout
        
        if output.strip():
            print("[grey]DEBUG output searchsploit:[/grey]\n" + output)
            print(Panel.fit(output, title="Risultati searchsploit"))
        
            path = os.path.join(latest, "searchsploit.txt")
            with open(path, "w") as f:
                f.write(output)
            print(f"\n💾 Risultati salvati in: {path}")
        else:
            print("[yellow]⚠️ Nessun risultato trovato da searchsploit. Probabilmente mancano versioni nei servizi o non ci sono match noti.[/yellow]\n")



    except Exception as e:
        print(f"[red]❌ Errore searchsploit:[/red] {e}")
