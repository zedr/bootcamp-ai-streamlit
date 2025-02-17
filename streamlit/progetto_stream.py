import streamlit as st
import notebook1  # Importa il primo notebook

# Titolo dell'app
st.title("Progetto Streamlit - Analisi di un dataset")

# Creazione di una tab
tab1= st.tabs(["Dataset Hollywood Movies"])

# Prima scheda: Analisi del primo dataset - Hollywood Movies
with tab1:
    st.header("Analisi del primo dataset - Hollywood Movies")
    notebook1.main()
