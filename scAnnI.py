import os
import socket
from rich.console import Console
from utils.tui import main_menu
from utils.pentest_auto import run_pentest_auto
from utils.manual_scan import run_manual_scan
from utils.exploit_runner import exploit_menu
from utils.ai_assistant import ai_assistant
from utils.searchsploit_helper import run_searchsploit
from utils.reporting import generate_session_report
from utils.tools import tools_menu
from utils.startup_check import startup_check

console = Console()
SCANS_DIR = "scans"
os.makedirs(SCANS_DIR, exist_ok=True)

session_memory = {
    "targets": [],
    "suggested_modules": [],
    "executed_exploits": []
}

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LHOST = get_local_ip()

def main():
    env_status = startup_check()
    console.clear()

    while True:
        choice = main_menu(env_status=env_status)

        if choice == "1":
            eseguito = run_pentest_auto(session_memory)
            if eseguito:
                console.input("\n[green]Premi Invio per tornare al menu...[/green]")
        elif choice == "2":
            run_manual_scan(session_memory)
        elif choice == "3":
            exploit_menu(session_memory)
        elif choice == "4":
            ai_assistant(session_memory)
        elif choice == "5":
            run_searchsploit()
            console.input("\n[green]Premi Invio per tornare al menu...[/green]")
        elif choice == "6":
            console.print("[cyan]📝 Generazione del report PDF in corso...[/cyan]")
            try:
                generate_session_report()
            except Exception as e:
                console.print(f"[red]❌ Errore generazione report PDF:[/red] {e}")
            console.input("\n[green]Premi Invio per tornare al menu...[/green]")
        elif choice == "7":
            console.print("[cyan]📄 Generazione del file exploit_list.txt in corso...[/cyan]")
            from utils.exploit_utils import generate_exploit_list
            generate_exploit_list()
            console.input("\n[green]Premi Invio per tornare al menu...[/green]")
        elif choice == "8":
            tools_menu()
        elif choice == "0":
            console.print("\n[cyan]👋 Uscita... Alla prossima![/cyan]")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[cyan]👋 Interrotto dall'utente. Uscita...[/cyan]")
