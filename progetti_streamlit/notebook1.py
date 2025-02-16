import streamlit as st
import pandas as pd
import plotly.express as px


# Funzione per caricare i dati con il percorso assoluto
@st.cache_data
def load_data():
    file_path = r"C:\Users\giuli\PycharmProjects\bootcamp-ai-streamlit\progetti_streamlit\HollywoodMovies.csv"
    return pd.read_csv(file_path)


def main():
    st.title("Analisi dei film di Hollywood 🎬")

    df = load_data()

    # Visualizzazione delle prime righe
    st.subheader("Prime righe del dataset")
    st.dataframe(df.head())

    # Numero di film per anno
    st.subheader("Numero di film per anno")
    movies_per_year = df["Year"].value_counts().sort_index()
    fig1 = px.bar(x=movies_per_year.index, y=movies_per_year.values,
                  labels={"x": "Anno", "y": "Numero di film"},
                  title="Numero di film per anno")
    st.plotly_chart(fig1)

    # Commento analitico
    st.markdown("""
    ### Analisi del numero di film usciti per anno 🎬 
    📌 **Grafico utilizzato**: Bar chart.

    Osserviamo una variazione nella quantità di film prodotti annualmente. Si nota un incremento nella produzione cinematografica in determinati periodi (2013, 2012, 2008), probabilmente dovuto a tendenze di mercato o cambiamenti nelle strategie delle case di produzione. Alcuni anni mostrano un calo significativo (2007), che potrebbe essere correlato a crisi economiche o scioperi nell’industria cinematografica. Sarebbe interessante correlare questi dati con eventi storici nel settore del cinema o con fattori economici, tecnologici o culturali.
    """)

    # Distribuzione dei generi cinematografici
    st.subheader("Distribuzione dei generi cinematografici")
    genre_distribution = df["Genre"].value_counts()
    fig2 = px.pie(names=genre_distribution.index, values=genre_distribution.values,
                  title="Distribuzione dei generi")
    st.plotly_chart(fig2)

    # Commento analitico
    st.markdown("""
    ### Distribuzione dei generi cinematografici 🎭
    📌 **Grafico utilizzato**: Torta con legenda esterna.

    Alcuni generi, come **Action**, **Drama** e **Comedy**, sono molto diffusi e dominano la produzione,  
    mentre altri come **Documentary** o **Musical** hanno una presenza minore.  
    Questa distribuzione riflette probabilmente le preferenze e la domanda del pubblico e  
    le strategie commerciali delle case di produzione.
    """)

    # Relazione tra budget e incassi mondiali
    st.subheader("Relazione tra Budget e Incassi")
    st.write("Seleziona il genere di film per filtrare i dati:")
    genres = st.multiselect("Seleziona i generi", df["Genre"].unique(),
                            default=df["Genre"].unique())
    filtered_df = df[df["Genre"].isin(genres)]
    fig3 = px.scatter(filtered_df, x="Budget", y="WorldGross", color="Genre",
                      log_x=True, log_y=True, title="Budget vs Incassi Mondiali")
    st.plotly_chart(fig3)

    # Commento analitico
    st.markdown("""
    ### Relazione tra Budget e Incassi 💵
    📌 **Grafico utilizzato**: Scatter plot.

    La maggior parte dei film segue una correlazione positiva: un budget elevato tende a portare a incassi più alti.
    Tuttavia, ci sono alcune eccezioni, ovvero film con budget basso ma incassi elevati (effetto sorpresa) o film ad alto budget che hanno floppato.
    """)


if __name__ == "__main__":
    main()
