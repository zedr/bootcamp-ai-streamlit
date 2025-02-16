import streamlit as st
import notebook1  # Importa il primo notebook
import notebook2  # Importa il secondo notebook

# Titolo dell'app
st.title("Progetti Streamlit - Analisi di Dataset")

# Creazione di due tab per separare le analisi
tab1, tab2 = st.tabs(["Dataset Hollywood Movies", "Dataset Eventi culturali in Italia"])

# Prima scheda: Analisi del primo dataset - Hollywood Movies
with tab1:
    st.header("Analisi del primo dataset - Hollywood Movies")
    notebook1.main()

# Seconda scheda: Analisi del secondo dataset - Eventi culturali in Italia
with tab2:
    st.header("Analisi del secondo dataset - Eventi culturali in Italia")
    notebook2.main()
