# utils/config_ai.py
import os

# Modelli AI predefiniti
AI_MODEL_DEFAULT = "openhermes"   # Per analisi, assistente AI, report
AI_MODEL_CODE = "codellama"       # Per generazione exploit e script

# Endpoint Ollama (centralizzati per coerenza tra i moduli)
OLLAMA_URL = "http://localhost:11434"
OLLAMA_GENERATE_URL = OLLAMA_URL + "/api/generate"
# (connect, read): evita hang infinito se il server accetta ma non risponde
OLLAMA_TIMEOUT = (5, 300)

# Root del progetto, per ancorare i path indipendentemente dalla CWD
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPLOIT_LIST_PATH = os.path.join(PROJECT_ROOT, "exploit_list.txt")
