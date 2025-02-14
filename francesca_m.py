import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Carica il file CSV
def load_data():
    return pd.read_csv('target_vaccinati_sicilia_Isemestre2021.csv')

st.title("DATI VACCINATI I SEMESTRE 2021 SICILIA")

# Mostra i dati
df = load_data()
st.write(df)

st.title("Filtro per provincia")

# Filtraggio opzionale per provincia
provincia = st.selectbox("Seleziona Provincia", df['provincia'].unique())
df_filtered = df[df['provincia'] == provincia]

st.write(df_filtered)

st.title("Numero di Vaccinati per Classe di Età e Provincia")
# Gruppo per classe di età e provincia, somma dei vaccinati
vaccinati_per_classe_età = df.groupby(['provincia', 'classeEta'])['Vaccinati'].sum().unstack()

# Visualizza un grafico a barre
fig, ax = plt.subplots(figsize=(10, 6))
vaccinati_per_classe_età.plot(kind='bar', ax=ax)

ax.set_ylabel('Numero di Vaccinati')
ax.set_xlabel('Provincia')
ax.set_title('Numero di Vaccinati per Classe di Età e Provincia')

st.pyplot(fig)

st.title("Vaccinazioni per Comune")
# Raggruppa i dati per comune e somma i vaccinati
vaccinazioni_comune = df.groupby('Comune')['Vaccinati'].sum()

# Filtra i comuni con un numero di vaccinati superiore a una soglia
soglia = st.slider('Seleziona la soglia di vaccinazioni', 0, int(vaccinazioni_comune.max()), 1000)
comuni_filtrati = vaccinazioni_comune[vaccinazioni_comune > soglia]

st.write(comuni_filtrati)

# Grafico a barre per i comuni con più vaccinati
fig, ax = plt.subplots(figsize=(10, 6))
comuni_filtrati.plot(kind='bar', ax=ax)

ax.set_ylabel('Numero di Vaccinati')
ax.set_xlabel('Comune')
ax.set_title(f'Comuni con più di {soglia} Vaccinati')

st.pyplot(fig)

st.title("Filtro per Classe di Età")
# Analisi delle vaccinazioni per classe di età
st.subheader("Vaccinazioni per classe di età")
classe_eta = df.groupby('classeEta')['Vaccinati'].sum().reset_index()
st.bar_chart(classe_eta.set_index('classeEta'))

# Analisi delle vaccinazioni per provincia
st.subheader("Vaccinazioni per provincia")
provincia = df.groupby('provincia')['Vaccinati'].sum().reset_index()
st.bar_chart(provincia.set_index('provincia'))

# Analisi per comune
st.subheader("Vaccinazioni per comune")
comune = df.groupby('Comune')['Vaccinati'].sum().reset_index()
top_comuni = comune.nlargest(10, 'Vaccinati')
st.write(top_comuni)

# Analisi dell'efficacia delle vaccinazioni
st.subheader("Analisi dell'efficacia delle vaccinazioni")
efficacia = df.groupby('classeEta')['Vaccinati'].sum().reset_index()
efficacia['percentuale_vaccinati'] = (efficacia['Vaccinati'] / df['Vaccinati'].sum()) * 100
st.line_chart(efficacia.set_index('classeEta')['percentuale_vaccinati'])

# Interazione con l'utente per analizzare specifici intervalli di tempo
st.subheader("Analisi per Intervallo di Tempo")
inizio = st.date_input("Seleziona la data di inizio:", pd.to_datetime(df['inizioIntervallo']).min())
fine = st.date_input("Seleziona la data di fine:", pd.to_datetime(df['fineIntervallo']).max())

# Assicurati che le colonne di data siano in formato datetime
df['inizioIntervallo'] = pd.to_datetime(df['inizioIntervallo'])
df['fineIntervallo'] = pd.to_datetime(df['fineIntervallo'])

# Converte le date selezionate in datetime
inizio = pd.to_datetime(inizio)
fine = pd.to_datetime(fine)

# Filtro per intervallo di tempo
df_filtered = df[(df['inizioIntervallo'] >= inizio) & (df['fineIntervallo'] <= fine)]
st.write(df_filtered)

st.title("Top 10 Province con Più Vaccinazioni")
# Raggruppa per provincia e somma i vaccinati
vaccinazioni_per_provincia = df.groupby('provincia')['Vaccinati'].sum()

# Visualizza le prime 10 province con il numero maggiore di vaccinati
top_province = vaccinazioni_per_provincia.nlargest(10)

# Grafico a barre per le province con più vaccinati
fig, ax = plt.subplots(figsize=(10, 6))
top_province.plot(kind='bar', ax=ax)

ax.set_ylabel('Numero di Vaccinati')
ax.set_xlabel('Provincia')
ax.set_title('Top 10 Province con Più Vaccinazioni')

st.pyplot(fig)

# Calcola statistiche sui vaccinati
totale_vaccinati = df['Vaccinati'].sum()
media_vaccinati = df['Vaccinati'].mean()

# Visualizza i risultati
st.write(f"Totale vaccinati in Sicilia: {totale_vaccinati}")
st.write(f"Media vaccinati per comune: {media_vaccinati:.2f}")

# Grafico a barre impilate per classe di età
fig, ax = plt.subplots(figsize=(10, 6))
vaccinati_per_classe_età.plot(kind='bar', stacked=True, ax=ax)

ax.set_ylabel('Numero di Vaccinati')
ax.set_xlabel('Classe di Età')
ax.set_title('Vaccinazioni per Classe di Età (Distribuzione Stacked)')

st.pyplot(fig)


st.title("Esporta Dati Filtrati")
# Aggiungi un'opzione per scaricare i dati filtrati
if st.button("Esporta Dati Filtrati"):
    df_filtered.to_csv("dati_filtrati.csv", index=False)
    st.success("File esportato come 'dati_filtrati.csv'")


