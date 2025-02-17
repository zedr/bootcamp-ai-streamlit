import streamlit as st

# Carica il tuo script Python del notebook
with open('notebook1.py') as f:
    code = f.read()

st.code(code, language='python')
