import os
import re
from fpdf import FPDF
from datetime import datetime
import requests
import matplotlib
matplotlib.use("Agg")  # usa il backend non-GUI
import matplotlib.pyplot as plt
from rich import print

SCANS_DIR = "scans"
MODEL = "openhermes"

class PDFReport(FPDF):
    def __init__(self, target_ip=""):
        super().__init__()
        self.target_ip = target_ip

    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"scAnnI - Report del PenTest ({self.target_ip})", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()} | Target: {self.target_ip}", 0, 0, "C")

def generate_port_graph(nmap_data, output_path):
    ports = []
    services = []
    for line in nmap_data.splitlines():
        if re.search(r"^[0-9]+/tcp\s+open", line):
            parts = line.split()
            port = parts[0].split("/")[0]
            service = parts[2] if len(parts) > 2 else "?"
            ports.append(port)
            services.append(service)

    if not ports:
        return False

    plt.figure(figsize=(8, 4))
    plt.bar(ports, [1]*len(ports), tick_label=services)
    plt.title("Porte Aperte Rilevate")
    plt.xlabel("Servizi")
    plt.ylabel("Stato")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return True

def generate_session_report():
    folders = sorted([f for f in os.listdir(SCANS_DIR) if os.path.isdir(os.path.join(SCANS_DIR, f))], reverse=True)
    if not folders:
        print("[red]❌ Nessuna scansione trovata per generare il report.[/red]")
        return

    latest = os.path.join(SCANS_DIR, folders[0])
    target_ip = folders[0].split("_")[0] if "_" in folders[0] else folders[0]
    pdf = PDFReport(target_ip=target_ip)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Sommario
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Sommario:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, "1. Informazioni di base\n2. Output Nmap\n3. Moduli suggeriti dalla AI\n4. Analisi tecnica finale")
    pdf.ln(5)

    # Sezione 1 - Info base
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Informazioni di base", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Cartella: {folders[0]}", ln=True)
    pdf.ln(5)

    # Sezione 2 - Output Nmap
    nmap_file = os.path.join(latest, "nmap_scan.txt")
    if os.path.exists(nmap_file):
        with open(nmap_file, "r") as f:
            nmap_data = f.read()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "2. Output Nmap", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, nmap_data)
        pdf.ln(3)

        # Generazione e inserimento grafico
        graph_path = os.path.join(latest, "port_graph.png")
        if generate_port_graph(nmap_data, graph_path):
            pdf.image(graph_path, w=180)
            pdf.ln(5)

    # Sezione 3 - Risposta IA
    ai_file = os.path.join(latest, "ollama_response.txt")
    if os.path.exists(ai_file):
        with open(ai_file, "r") as f:
            ai_data = f.read()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "3. Moduli suggeriti dalla IA", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, ai_data)
        pdf.ln(5)

    # Sezione 4 - Analisi AI finale (extra)
    if os.path.exists(nmap_file):
        try:
            with open(nmap_file, "r") as f:
                raw_nmap = f.read()
            prompt = (
    "Analizza il seguente output Nmap in modo dettagliato e professionale. "
    "La tua risposta deve essere in italiano tecnico, formale e completo. "
    "Non usare inglese. Scrivi come se fosse un report professionale per un team di cybersecurity italiano.\n\n"
    f"{raw_nmap}"
)

            res = requests.post("http://localhost:11434/api/generate", json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            })
            summary = res.json().get("response", "[Nessuna risposta dalla AI]")
        except Exception as e:
            summary = f"[Errore durante l'analisi AI]: {e}"

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "4. Analisi AI del target", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, summary)

    # Salva il file
    report_path = os.path.join(latest, "report.pdf")
    pdf.output(report_path)
    print(f"[green]✅ Report PDF generato in:[/green] {report_path}")
