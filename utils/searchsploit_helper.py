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

    dirs = sorted(d for d in os.listdir(SCANS_DIR) if os.path.isdir(os.path.join(SCANS_DIR, d)))
    if not dirs:
        print("[red]❌ Nessuna scansione trovata.[/red]")
        return

    latest = os.path.join(SCANS_DIR, dirs[-1])
    # searchsploit --nmap richiede l'output XML (-oX) di Nmap, non il testo (-oN)
    nmap_file = os.path.join(latest, "nmap_scan.xml")

    if not os.path.isfile(nmap_file):
        print(f"[red]❌ File Nmap XML (nmap_scan.xml) non trovato in {latest}[/red]")
        print("[yellow]💡 searchsploit richiede l'output XML di Nmap; esegui una nuova scansione.[/yellow]")
        return

    print(f"\n[cyan]📦 Esecuzione searchsploit su:[/cyan] {nmap_file}\n")

    try:
        result = subprocess.run([
            "searchsploit", "--nmap", nmap_file
        ], capture_output=True, text=True, timeout=60)

        output = result.stdout

        if output.strip():
            print(Panel.fit(output, title="Risultati searchsploit"))

            path = os.path.join(latest, "searchsploit.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"\n💾 Risultati salvati in: {path}")
        else:
            print("[yellow]⚠️ Nessun risultato trovato da searchsploit. Probabilmente mancano versioni nei servizi o non ci sono match noti.[/yellow]\n")

    except FileNotFoundError:
        print("[red]❌ searchsploit non trovato. Installa exploitdb per usare questa funzione.[/red]")
    except Exception as e:
        print(f"[red]❌ Errore searchsploit:[/red] {e}")
