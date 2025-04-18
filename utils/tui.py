from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text
import socket
import time

console = Console()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def render_layout(env_status=None):
    lhost = get_local_ip()

    header = Panel(
        Text(f"🧠 scAnnI v0.1.2025\nby Kita69 | LHOST: {lhost}", justify="center", style="bold cyan"),
        expand=False
    )

    banner = Text(r"""
             _                ___ 
 ___  ___   / \   _ __  _ __ |_ _|
/ __|/ __| / _ \ | '_ \| '_ \ | | 
\__ \ (__ / ___ \| | | | | | || | 
|___/\___/_/   \_\_| |_|_| |_|___|

scAnnI v0.1.2025 - AI Powered Pentest Toolkit
""", justify="center")

    msf_status = "🟢" if env_status and env_status.get("msfconsole") else "🔴"
    ai_status = "🟢" if env_status and env_status.get("ollama") else "🔴"

    menu_text = Text.from_markup(
        "\n".join([
            f"{msf_status} 1. Pentest automatico",
            f"{msf_status} 2. Scansione manuale passo passo",
            f"{msf_status} 3. Esegui exploit generati (.rc)",
            f"{ai_status} 4. Assistente AI",
            "🟢 5. Suggerimenti da ExploitDB (searchsploit)",
            f"{msf_status} 6. Genera report PDF ultima sessione",
            f"{msf_status} 7. Genera file exploit_list.txt",
            "🛠️ 8. Tool esterni",
            "🚪 0. Esci"
        ])
    )

    menu_panel = Panel(menu_text, title="Menu principale", expand=True)

    return Group(header, banner, menu_panel)

def main_menu(ultimate=False, env_status=None):
    console.clear()

    with Live(render_layout(env_status), refresh_per_second=0.5, console=console):
        time.sleep(0.5)

    return Prompt.ask(
        "\n[green]Seleziona un'opzione[/green]",
        choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    )
