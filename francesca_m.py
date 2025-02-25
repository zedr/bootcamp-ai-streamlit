import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data  # Memorizza i dati per migliorare le prestazioni
# Funzione per caricare i dati
def load_data():
    return pd.read_csv('target_vaccinati_sic_Isem2021.csv')

def load_data_sleep():
    file_path = "sleep_cycle_productivity.csv"
    data = pd.read_csv(file_path)
    data['Sleep Start Time'] = pd.to_numeric(data['Sleep Start Time'], errors='coerce')
    data['Sleep End Time'] = pd.to_numeric(data['Sleep End Time'], errors='coerce')
    return data

def load_data_smoke():
    return pd.read_csv('smoking_health_data_final.csv')


st.sidebar.header("Benvenuto!👋 Qui puoi esplorare i miei progetti")

project = st.sidebar.selectbox("Scegli il progetto", ["Progetto Vaccinazioni", "Progetto Sonno e Produttività", "Progetto Smoke"])


# Carica il progetto selezionato
if project == "Progetto Vaccinazioni":
    st.markdown("### 📊 Analisi delle Vaccinazioni in Sicilia (Primo Semestre 2021)")

    # Descrizione introduttiva
    st.markdown("""
        Questa sezione esplora i dati relativi alle vaccinazioni del primo semestre 2021 in Sicilia. 🏥  
        Puoi selezionare diverse opzioni per esplorare i dati, visualizzare statistiche e grafici interattivi. 📈  
        L'obiettivo è capire come le vaccinazioni sono state distribuite tra le province, i comuni e le diverse fasce d'età.
        """)

    # Mostra i dati
    df = load_data()
    st.write("📝 **Dati delle vaccinazioni**: Qui puoi visualizzare il dataset con tutte le informazioni relative alle vaccinazioni.")
    st.write(df)

    # Statistiche sui vaccinati
    st.markdown("### 📊 Statistiche sui Vaccinati")
    st.markdown(""" 
        Questa sezione mostra il totale e la media dei vaccinati in Sicilia.  
        - **Totale vaccinati**: Il numero complessivo di persone vaccinate in Sicilia.  
        - **Media vaccinati per comune**: La media delle persone vaccinate in ciascun comune.  
        Questi dati ti aiutano a capire l'impatto complessivo della campagna vaccinale.
        """)
    totale_vaccinati = df['Vaccinati'].sum()
    media_vaccinati = df['Vaccinati'].mean()
    st.write(f"🧑‍🤝‍🧑 **Totale vaccinati in Sicilia:** {totale_vaccinati}")
    st.write(f"📊 **Media vaccinati per comune:** {media_vaccinati:.2f}")


    # Filtro per provincia
    st.markdown("### 🔍 Filtro per Provincia")
    st.markdown("""
        Puoi selezionare una provincia per visualizzare i dati relativi alle vaccinazioni specifiche per quella provincia.  
        Questo ti permette di confrontare le diverse province e vedere come la campagna vaccinale è stata implementata in ciascuna area.
        """)
    provincia = st.selectbox("Seleziona la Provincia", df['provincia'].unique())
    df_filtered = df[df['provincia'] == provincia]
    st.write("🔍 **Dati filtrati per provincia selezionata**: Questi sono i dati delle vaccinazioni per la provincia scelta.")
    st.write(df_filtered)

    # Grafico numero vaccinati per classe di età e provincia
    st.markdown("### 📊 Numero di Vaccinati per Classe di Età e Provincia")

    st.markdown(""" 
        Questo grafico mostra come il numero di vaccinati varia in base alla classe di età e alla provincia.  
        Puoi vedere quali fasce d'età sono state più vaccinate e come le diverse province si confrontano.
        """)
    vaccinati_per_classe_età = df.groupby(['provincia', 'classeEta'])['Vaccinati'].sum().unstack()
    fig, ax = plt.subplots(figsize=(10, 6))
    vaccinati_per_classe_età.plot(kind='bar', ax=ax)
    ax.set_ylabel('Numero di Vaccinati')
    ax.set_xlabel('Provincia')
    ax.set_title('Numero di Vaccinati per Classe di Età e Provincia')
    st.pyplot(fig)

    # Vaccinazioni per comune
    st.markdown("### 🌍 Vaccinazioni per Comune")
    st.markdown(""" 
        Questa sezione ti permette di esplorare i dati di vaccinazione per ciascun comune della Sicilia.  
        Puoi filtrare i comuni in base a un numero minimo di vaccinati per vedere quali aree hanno avuto una maggiore copertura vaccinale.
        """)
    vaccinazioni_comune = df.groupby('Comune')['Vaccinati'].sum()
    soglia = st.slider('📏 Seleziona la soglia di vaccinazioni', 0, int(vaccinazioni_comune.max()), 1000)
    comuni_filtrati = vaccinazioni_comune[vaccinazioni_comune > soglia]
    st.write(f"🗺️ **Comuni con più di {soglia} vaccinati**: Questi sono i comuni con un numero di vaccinati superiore alla soglia selezionata.")
    st.write(comuni_filtrati)

    # Grafico per comuni con più vaccinati
    if not comuni_filtrati.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        comuni_filtrati.plot(kind='bar', ax=ax)
        ax.set_ylabel('Numero di Vaccinati')
        ax.set_xlabel('Comune')
        ax.set_title(f'Comuni con più di {soglia} Vaccinati')
        st.pyplot(fig)
    else:
        st.warning(f"⚠️ Non ci sono comuni con più di {soglia} vaccinati.")

    # Analisi delle vaccinazioni per classe di età
    st.markdown("### 👶 Vaccinazioni per Classe di Età")
    st.markdown(""" 
        Questo grafico mostra il totale delle vaccinazioni suddivise per classe di età.  
        Puoi vedere quali fasce d'età hanno avuto una maggiore copertura vaccinale e quali meno.
        """)
    classe_eta = df.groupby('classeEta')['Vaccinati'].sum().reset_index()
    st.bar_chart(classe_eta.set_index('classeEta'))

    # Analisi delle vaccinazioni per provincia
    st.markdown("### 🏙️ Vaccinazioni per Provincia")
    st.markdown("""
        Questo grafico mostra il totale delle vaccinazioni per ciascuna provincia della Sicilia.  
        Puoi confrontare le diverse province e vedere quali hanno avuto una maggiore copertura vaccinale.
        """)
    provincia = df.groupby('provincia')['Vaccinati'].sum().reset_index()
    st.bar_chart(provincia.set_index('provincia'))

    # Analisi dell'efficacia delle vaccinazioni
    st.markdown("### 💉 Analisi dell'efficacia delle Vaccinazioni")
    st.markdown("""
        Questo grafico mostra la percentuale di vaccinati per ciascuna classe di età.  
        Puoi vedere quali fasce d'età hanno avuto una maggiore adesione alla campagna vaccinale.
        """)
    efficacia = df.groupby('classeEta')['Vaccinati'].sum().reset_index()
    efficacia['percentuale_vaccinati'] = (efficacia['Vaccinati'] / df['Vaccinati'].sum()) * 100
    st.line_chart(efficacia.set_index('classeEta')['percentuale_vaccinati'])

    # Selezione dell'intervallo di tempo
    st.markdown("### 🗓️ Analisi per Intervallo di Tempo")
    st.markdown(""" 
        Puoi selezionare un intervallo di tempo per analizzare i dati delle vaccinazioni in un periodo specifico.  
        Questo ti permette di vedere come la campagna vaccinale è progredita nel tempo.
        """)
    inizio = st.date_input("Seleziona la data di inizio:", pd.to_datetime(df['inizioIntervallo']).min())
    fine = st.date_input("Seleziona la data di fine:", pd.to_datetime(df['fineIntervallo']).max())

    # colonne di data  in formato datetime
    df['inizioIntervallo'] = pd.to_datetime(df['inizioIntervallo'])
    df['fineIntervallo'] = pd.to_datetime(df['fineIntervallo'])

    # Converte le date selezionate in datetime
    inizio = pd.to_datetime(inizio)
    fine = pd.to_datetime(fine)

    # Filtro per intervallo di tempo
    df_filtered = df[(df['inizioIntervallo'] >= inizio) & (df['fineIntervallo'] <= fine)]
    st.write(df_filtered)

    # Top 10 province con più vaccinati
    st.markdown("### 🏆 Top 10 Province con Più Vaccinazioni")
    st.markdown("""
        Questo grafico mostra le 10 province con il maggior numero di vaccinazioni.  
        Puoi vedere quali province hanno avuto una maggiore adesione alla campagna vaccinale.
        """)
    vaccinazioni_per_provincia = df.groupby('provincia')['Vaccinati'].sum()
    top_province = vaccinazioni_per_provincia.nlargest(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_province.plot(kind='bar', ax=ax)
    ax.set_ylabel('Numero di Vaccinati')
    ax.set_xlabel('Provincia')
    ax.set_title('Top 10 Province con Più Vaccinazioni')
    st.pyplot(fig)


    # Grafico a barre impilate per classe di età
    st.markdown("### 📊 Vaccinazioni per Classe di Età (Stacked)")
    st.markdown(""" 
        Questo grafico a barre impilate mostra la distribuzione delle vaccinazioni per classe di età.  
        Puoi vedere come le diverse fasce d'età contribuiscono al totale delle vaccinazioni.
        """)
    fig, ax = plt.subplots(figsize=(10, 6))
    vaccinati_per_classe_età.plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel('Numero di Vaccinati')
    ax.set_xlabel('Classe di Età')
    ax.set_title('Vaccinazioni per Classe di Età (Distribuzione Stacked)')
    st.pyplot(fig)

    # Esportazione dei dati
    st.markdown("### 📥 Esporta Dati Filtrati")
    st.markdown("""
        Puoi esportare i dati filtrati in un file CSV per analisi future.  
        Questo ti permette di lavorare con i dati al di fuori dell'app.
        """)
    if st.button("🚀 Esporta Dati Filtrati"):
        df_filtered.to_csv("dati_filtrati.csv", index=False)
        st.success("✅ File esportato come 'dati_filtrati.csv'")



elif project == "Progetto Sonno e Produttività":

    data = load_data_sleep()

    # Titolo e descrizione dell'app
    st.title("🌙 Analisi delle Abitudini del Sonno e Benessere 💤")
    st.markdown("""
    Questa applicazione analizza le abitudini del sonno e il loro impatto su produttività, umore e livelli di stress. Esplora i dati per individuare correlazioni tra fattori dello stile di vita e qualità del sonno.
    """)

    # Esplorazione del dataset
    st.header("🔍 Esplorazione del Dataset")
    st.markdown(""" 
    In questa sezione puoi visualizzare i primi record del dataset o esplorare le statistiche descrittive per avere un'idea generale dei dati analizzati.  
    - **Primi 5 record**: Mostra una piccola anteprima del dataset.  
    - **Statistiche descrittive**: Fornisce una panoramica delle caratteristiche principali dei dati, come media, deviazione standard, minimo, massimo e quartili.
    """)
    if st.checkbox("📄 Mostra i primi 5 record"):
        st.write(data.head())

    if st.checkbox("📊 Mostra statistiche descrittive"):
        st.markdown("""
        **Cosa sono le statistiche descrittive?**  
        Le statistiche descrittive includono:

        - **count**: Il numero di valori non nulli (quanti partecipanti hanno fornito dati per questa colonna).
        - **mean**: La media dei valori (il valore medio).
        - **std**: La deviazione standard (quanto i dati sono dispersi rispetto alla media).
        - **min**: Il valore minimo osservato.
        - **25%**: Il primo quartile (25% dei dati è inferiore a questo valore).
        - **50%**: La mediana (il valore centrale, 50% dei dati è inferiore a questo valore).
        - **75%**: Il terzo quartile (75% dei dati è inferiore a questo valore).
        - **max**: Il valore massimo osservato.

        Queste statistiche ti aiutano a capire la distribuzione e la variabilità dei dati.
        """)
        st.write(data.describe())

    # Filtri per esplorazione
    st.header("🎯 Filtri Personalizzati")
    st.markdown("""
    **Perché usare i filtri?**  
    Puoi selezionare un genere e un intervallo di età per analizzare un sottoinsieme specifico del dataset.  
    Questo ti permette di esplorare come le abitudini del sonno variano in base a genere ed età.
    """)

    genere = st.selectbox("👤 Seleziona il Genere", options=data['Gender'].unique())
    età = st.slider("📅 Seleziona un intervallo di Età", int(data['Age'].min()), int(data['Age'].max()), (20, 40))

    filtered_data = data[(data['Gender'] == genere) & (data['Age'].between(età[0], età[1]))]
    st.write(filtered_data)

    # Suggerimenti per migliorare la qualità del sonno
    st.header("💡 Suggerimenti per Migliorare la Qualità del Sonno")
    st.markdown("""
    **Perché è importante migliorare la qualità del sonno?**  
    Un sonno di qualità è essenziale per la salute fisica e mentale. Ecco alcuni suggerimenti pratici:

    - **Esercizio fisico**: Un'attività fisica regolare può migliorare la qualità del sonno.
    - **Limitare la caffeina**: Ridurre l'assunzione di caffeina, soprattutto nelle ore serali, può favorire un sonno migliore.
    - **Tempo davanti allo schermo**: Cerca di limitare il tempo trascorso davanti allo schermo prima di andare a letto per migliorare la qualità del sonno.
    """)

    # Visualizzazioni interattive
    st.header("📈 Visualizzazioni Interattive")
    st.markdown("""
    In questa sezione puoi esplorare graficamente le relazioni tra diversi fattori legati al sonno, come la qualità, la durata e altri elementi dello stile di vita.  
    Scegli uno dei grafici per visualizzare meglio i dati e le correlazioni.
    """)

    # Distribuzione della qualità del sonno
    if st.checkbox("🌟 Distribuzione della Qualità del Sonno"):
        st.markdown(""" 
        Questo istogramma mostra come la qualità del sonno è distribuita tra gli utenti, valutata su una scala da 1 (scarsa) a 10 (eccellente).  
        La linea di densità aiuta a vedere se la qualità del sonno è generalmente alta o bassa.
        """)
        fig, ax = plt.subplots()
        sns.histplot(data['Sleep Quality'], kde=True, bins=10, ax=ax)
        ax.set_title("Distribuzione della Qualità del Sonno")
        st.pyplot(fig)

    # Correlazioni generali
    if st.checkbox("🔗 Mappa di Correlazione"):
        st.markdown(""" 
        La mappa di correlazione evidenzia le relazioni tra tutte le variabili numeriche presenti nel dataset.  
        I valori vanno da -1 a 1:  
        - **1**: Correlazione positiva perfetta (se una variabile aumenta, l'altra aumenta).  
        - **-1**: Correlazione negativa perfetta (se una variabile aumenta, l'altra diminuisce).  
        - **0**: Nessuna correlazione.  

        Le celle più scure indicano una correlazione più forte.
        """)
        fig, ax = plt.subplots(figsize=(10, 8))
        correlation = data.select_dtypes(include=['float64', 'int64']).corr()
        sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Mappa di Correlazione")
        st.pyplot(fig)

    # Analisi delle ore di lavoro sul sonno
    if st.checkbox("💼 Impatto delle Ore di Lavoro sul Sonno"):
        st.markdown(""" 
        Questo grafico esplora come le ore di lavoro giornaliere possano influire sulla durata e qualità del sonno.  
        Un aumento delle ore di lavoro potrebbe ridurre la durata del sonno.
        """)
        fig, ax = plt.subplots()
        sns.scatterplot(x=data['Work Hours (hrs/day)'], y=data['Total Sleep Hours'], ax=ax)
        ax.set_title("Ore di Lavoro vs Ore di Sonno")
        st.pyplot(fig)

    # Ore di sonno media per fascia di età
    if st.checkbox("⏰ Ore di Sonno Media per Fascia di Età", key="ore_media_fascia_eta"):
        st.markdown(""" 
        Questo grafico a barre mostra la media delle ore di sonno per fascia d'età.  
        Puoi vedere se ci sono differenze significative nella durata del sonno tra diverse fasce d'età.
        """)
        fig, ax = plt.subplots(figsize=(8, 6))
        sleep_by_age = data.groupby('Age')['Total Sleep Hours'].mean()
        sleep_by_age.plot(kind='bar', ax=ax, color='salmon')
        ax.set_title("Ore di Sonno Media per Fascia di Età")
        ax.set_xlabel('Fascia d\'Età')
        ax.set_ylabel('Ore di Sonno Media')
        st.pyplot(fig)

    # Correlazione tra qualità del sonno e produttività
    if st.checkbox("📈 Correlazione tra Qualità del Sonno e Produttività", key="correlazione_produttivita"):
        st.markdown("""  
        Questo boxplot mostra come varia la produttività in base alla qualità del sonno.  
        Puoi vedere se una migliore qualità del sonno è associata a una maggiore produttività.
        """)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x=data['Sleep Quality'], y=data['Productivity Score'], ax=ax, color='lightgreen')
        ax.set_title("Produttività vs Qualità del Sonno")
        ax.set_xlabel('Qualità del Sonno')
        ax.set_ylabel('Punteggio di Produttività')
        st.pyplot(fig)

    # Distribuzione dell'umore in base alla qualità del sonno
    if st.checkbox("🌈 Distribuzione dell'Umore in base alla Qualità del Sonno", key="distribuzione_umore"):
        st.markdown("""
        Questo grafico a scatola (boxplot) mostra come l'umore varia in base alla qualità del sonno.  
        Puoi vedere se una migliore qualità del sonno è associata a un umore più positivo.
        """)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x=data['Sleep Quality'], y=data['Mood Score'], ax=ax, color='lightblue')
        ax.set_title("Distribuzione dell'Umore in base alla Qualità del Sonno")
        ax.set_xlabel('Qualità del Sonno')
        ax.set_ylabel('Punteggio dell\'Umore')
        st.pyplot(fig)

    # Media delle ore di sonno in base al genere
    if st.checkbox("👤 Ore di Sonno Media per Genere", key="ore_media_genere"):
        st.markdown("""
        Questo grafico a barre mostra le ore di sonno medie per genere.  
        Puoi vedere se ci sono differenze significative nella durata del sonno tra uomini e donne.
        """)
        fig, ax = plt.subplots(figsize=(8, 6))
        sleep_by_gender = data.groupby('Gender')['Total Sleep Hours'].mean()
        sleep_by_gender.plot(kind='bar', ax=ax, color='orange')
        ax.set_title("Ore di Sonno Media per Genere")
        ax.set_xlabel('Genere')
        ax.set_ylabel('Ore di Sonno Media')
        st.pyplot(fig)

    # Messaggio finale
    st.markdown("""
    **🎉 Complimenti!**  
    Hai esplorato come le abitudini del sonno possano influire sulla produttività, l'umore e lo stress.  
    Usa i filtri e le visualizzazioni per scoprire di più sui tuoi dati.  
    Grazie per aver utilizzato questa app! ❤️  
    """)

elif project == "Progetto Smoke":
    df = load_data_smoke()

    # Titolo e introduzione
    st.title("🚭 Analisi Fumo & Salute 🧠")
    st.markdown("""
    Benvenuto nell'app che esplora come il fumo influenzi la nostra salute! 🌱
    Iniziamo un viaggio nei dati per scoprire come il fumo impatti parametri come la frequenza cardiaca ❤️, la pressione sanguigna 💪 e i livelli di colesterolo 🧃.
    """)

    # Visualizzazione dei dati grezzi
    st.subheader("🔍 Esploriamo i Dati!")
    st.markdown("""
    **Cosa stai vedendo?**  
    Qui vengono visualizzati i primi 10 record di un dataset. Questo ti permette di avere un'anteprima dei dati con cui stiamo lavorando.  
    Ogni riga rappresenta un partecipante, e le colonne contengono informazioni come età, frequenza cardiaca, pressione sanguigna e stato di fumatore.
    """)
    st.write("Ecco i primi dati raccolti:", df.head(10))

    # Statistiche descrittive
    st.subheader("📊 Statistiche Descrittive")
    st.markdown("""
    **Cosa sono le statistiche descrittive?**  
    Le statistiche descrittive forniscono una panoramica veloce delle caratteristiche principali dei dati. Ecco cosa significano i valori:

    - **count**: Il numero di valori non nulli (quanti partecipanti hanno fornito dati per questa colonna).
    - **mean**: La media dei valori (il valore medio).
    - **std**: La deviazione standard (quanto i dati sono dispersi rispetto alla media).
    - **min**: Il valore minimo osservato.
    - **25%**: Il primo quartile (25% dei dati è inferiore a questo valore).
    - **50%**: La mediana (il valore centrale, 50% dei dati è inferiore a questo valore).
    - **75%**: Il terzo quartile (75% dei dati è inferiore a questo valore).
    - **max**: Il valore massimo osservato.

    Queste statistiche ti aiutano a capire la distribuzione e la variabilità dei dati.
    """)
    st.write(df.describe())

    # Filtro per età e fumatore/non fumatore
    st.subheader("🔍 Filtra i Dati")
    st.markdown("""
    **Perché filtrare i dati?**  
    Puoi selezionare un'età specifica e lo stato di fumatore (fumatore, non fumatore o tutti) per visualizzare solo i dati rilevanti.  
    Questo ti permette di esplorare come il fumo influisce su specifici gruppi di età.
    """)
    col1, col2 = st.columns(2)
    with col1:
        age_filter = st.slider("Seleziona l'età di un partecipante:", int(df['age'].min()), int(df['age'].max()))
    with col2:
        smoker_filter = st.selectbox("Seleziona lo stato di fumatore:", ["Tutti", "Fumatore", "Non Fumatore"])

    # Applica i filtri
    filtered_data = df[df['age'] == age_filter]
    if smoker_filter == "Fumatore":
        filtered_data = filtered_data[filtered_data['current_smoker'] == 'yes']
    elif smoker_filter == "Non Fumatore":
        filtered_data = filtered_data[filtered_data['current_smoker'] == 'no']

    # Visualizzazione dei dati filtrati
    st.write(f"🔍 Risultati per l'età {age_filter} anni e stato di fumatore: {smoker_filter}")
    st.write(filtered_data)

    # Download dei dati filtrati
    st.markdown("""
    **Scarica i dati filtrati**  
    Puoi scaricare i dati filtrati in formato CSV per ulteriori analisi o per conservarli.
    """)
    st.download_button(
        label="Scarica i dati filtrati (CSV)",
        data=filtered_data.to_csv(index=False).encode('utf-8'),
        file_name='dati_filtrati.csv',
        mime='text/csv'
    )

    # Analisi Fumatori vs Non Fumatori
    st.subheader("Fumatori vs Non Fumatori 🔥❌")
    st.markdown("""
    **Cosa stai vedendo?**  
    In questa sezione, confrontiamo i fumatori e i non fumatori in termini di frequenza cardiaca media e distribuzione dell'età.  
    Questo ti aiuta a capire se ci sono differenze significative tra i due gruppi.
    """)

    smokers = df[df['current_smoker'] == 'yes']
    non_smokers = df[df['current_smoker'] == 'no']

    # Grafico a torta per fumatori vs non fumatori
    st.write("📊 Proporzione di Fumatori e Non Fumatori")
    st.markdown("""
    **Cosa mostra questo grafico?**  
    Il grafico a torta mostra la proporzione di fumatori e non fumatori nel dataset.  
    Questo ti aiuta a capire quanto è comune il fumo tra i partecipanti.
    """)
    fig, ax = plt.subplots()
    ax.pie([smokers.shape[0], non_smokers.shape[0]], labels=["Fumatori", "Non Fumatori"], autopct='%1.1f%%',
           colors=['#ff9999', '#66b3ff'])
    st.pyplot(fig)

    # Confronto delle medie dei parametri di salute
    st.write("💓 Frequenza Cardiaca Media:")
    st.markdown("""
    **Cosa significa?**  
    La frequenza cardiaca media è un indicatore importante della salute cardiovascolare.  
    Qui confrontiamo la frequenza cardiaca media tra fumatori e non fumatori per vedere se ci sono differenze significative.
    """)
    st.write(f"Fumatori: {smokers['heart_rate'].mean():.2f} bpm")
    st.write(f"Non Fumatori: {non_smokers['heart_rate'].mean():.2f} bpm")

    # Grafico della distribuzione dell'età
    st.subheader("📅 Distribuzione dell'Età")
    st.markdown("""
    **Cosa mostra questo grafico?**  
    Il grafico mostra la distribuzione dell'età dei partecipanti.  
    Puoi vedere quante persone ci sono in ogni fascia d'età e se ci sono picchi o tendenze particolari.
    """)
    st.write("Scopri la distribuzione dell'età dei partecipanti")
    fig, ax = plt.subplots()
    sns.histplot(df['age'], kde=True, ax=ax)
    st.pyplot(fig)

    # Analisi della pressione sanguigna
    st.subheader("💉 Pressione Sanguigna (Sistolica vs Diastolica)")
    st.markdown("""
    **Cosa stai vedendo?**  
    Questo grafico mostra la relazione tra la pressione sistolica (massima) e diastolica (minima).  
    Ogni punto rappresenta un partecipante. Puoi vedere se c'è una correlazione tra le due misure.
    """)
    st.write("Ecco come si distribuiscono la pressione sistolica e diastolica nei partecipanti")
    df['sistolica'], df['diastolica'] = zip(
        *df['blood_pressure'].str.split('/').apply(lambda x: (float(x[0]), float(x[1]))))
    fig, ax = plt.subplots()
    sns.scatterplot(x='sistolica', y='diastolica', data=df, ax=ax)
    st.pyplot(fig)

    # Distribuzione del colesterolo
    st.subheader("🧃 Distribuzione del Colesterolo")
    st.markdown("""
    **Cosa mostra questo grafico?**  
    Il grafico mostra la distribuzione dei livelli di colesterolo nei partecipanti.  
    Puoi vedere se ci sono valori anomali (outlier) o se la maggior parte delle persone ha livelli di colesterolo nella norma.
    """)
    st.write("Ecco come si distribuisce il colesterolo nei partecipanti")
    fig, ax = plt.subplots()
    sns.histplot(df['chol'], kde=True, ax=ax, color='green')
    st.pyplot(fig)

    # Heatmap delle correlazioni
    st.subheader("📈 Correlazione tra Variabili")
    st.markdown("""
    **Cosa stai vedendo?**  
    La heatmap mostra le correlazioni tra le variabili numeriche del dataset.  
    I valori vanno da -1 a 1:  
    - **1**: Correlazione positiva perfetta (se una variabile aumenta, l'altra aumenta).  
    - **-1**: Correlazione negativa perfetta (se una variabile aumenta, l'altra diminuisce).  
    - **0**: Nessuna correlazione.  

    Questo ti aiuta a identificare relazioni interessanti tra le variabili.
    """)
    st.write("Ecco la correlazione tra le variabili numeriche del dataset")
    corr = df.corr(numeric_only=True)
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Confronto statistiche descrittive per fumatori vs non fumatori
    st.subheader("📊 Confronto Statistiche Fumatori vs Non Fumatori")
    st.markdown("""
    **Cosa stai vedendo?**  
    Qui confrontiamo le statistiche descrittive (media, deviazione standard, minimo, massimo, ecc.) tra fumatori e non fumatori.  
    Questo ti aiuta a capire se ci sono differenze significative tra i due gruppi in termini di età, frequenza cardiaca, pressione sanguigna e colesterolo.
    """)
    st.write("Confronto delle statistiche descrittive tra fumatori e non fumatori")
    st.write("**Fumatori:**")
    st.write(smokers.describe())
    st.write("**Non Fumatori:**")
    st.write(non_smokers.describe())

    # Messaggio finale
    st.markdown("""
    🎉 Complimenti! Hai esplorato come il fumo possa influire sulla salute.  
    Usa i filtri per esplorare dati specifici e scoprire di più!  😊
    """)




st.markdown("\n❤️ App sviluppata usando Streamlit! 🚀")
