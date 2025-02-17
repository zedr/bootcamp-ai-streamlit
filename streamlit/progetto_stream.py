import streamlit as st
import os

# Ottieni il percorso della cartella corrente
base_path = os.path.dirname(__file__)

# Percorso relativo al file notebook1.py dentro la cartella "streamlit"
file_path = os.path.join(base_path, "streamlit", "notebook1.py")

# Leggi il contenuto del file in sicurezza
try:
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    st.code(code, language="python")
except FileNotFoundError:
    st.error(f"Errore: il file non è stato trovato nel percorso {file_path}")

