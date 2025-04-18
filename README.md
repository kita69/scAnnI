# 🧠 scAnnI - AI Powered Pentest Toolkit

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/status-Beta-orange)

> 🔎 AI-assisted reconnaissance, vulnerability analysis, exploit generation and reporting — all from a terminal-based toolkit.

---

## 🚀 Descrizione

**scAnnI** (Scan + AI) è un toolkit per penetration testing **assistito da intelligenza artificiale**.  
Combina strumenti classici come **Nmap** e **Metasploit** con l'AI locale tramite **Ollama**, permettendoti di:

- Eseguire scansioni di rete
- Analizzare vulnerabilità con AI
- Generare file `.rc` per Metasploit
- Lanciare exploit
- Generare report PDF completi con sommario e grafico porte
- Interagire con un assistente AI in tempo reale

---

## 🧠 Funzionalità principali

- ✅ Scansione Nmap automatica o manuale
- ✅ Analisi AI tecnica (OpenHermes, CodeLlama, ecc.)
- ✅ Generazione di exploit `.rc`
- ✅ Esecuzione automatica exploit (con Metasploit)
- ✅ Assistente AI in tempo reale
- ✅ Integrazione con `searchsploit`
- ✅ Report PDF con:
  - Sommario
  - Output Nmap
  - Risposta AI
  - Grafico delle porte aperte

---

## 📂 Struttura progetto

scanni/
├── scAnnI.py
├── requirements.txt
├── setup.py
├── exploit_list.txt
├── scans/
│   └── [timestamp]/report.pdf
├── fluxion/ (facoltativo)
└── utils/
    ├── ai_assistant.py
    ├── config_ai.py
    ├── exploit_runner.py
    ├── exploit_utils.py
    ├── manual_scan.py
    ├── pentest_auto.py
    ├── reporting.py
    ├── searchsploit_helper.py
    ├── tools.py
    └── tui.py


## ⚙️ Requisiti

- Python 3.10+
- [Ollama](https://ollama.com) installato e funzionante su `localhost:11434`
- `nmap`, `msfconsole`, `hydra` installati nel sistema
- `fpdf`, `matplotlib`, `rich`, `requests` (puoi installarli con `pip`)

---

## 📦 Installazione

```bash
git clone https://github.com/tuonome/scAnnI.git
cd scAnnI
pip install -r requirements.txt
python3 scAnnI.py

# scAnnI
