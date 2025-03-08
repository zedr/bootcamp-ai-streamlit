import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import altair as alt
import numpy as np
import streamlit as st
import tensorflow as tf
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from PIL import Image


# Funzioni per indovina un numero
def get_secret_number():
    return random.randint(1, 10)


def initial_state(is_new_run=True):
    # Quando la impostiamo a True, significa che è un nuovo run del gioco
    if is_new_run:
        st.session_state.attempts_in_current_game = 0  # Azzeriamo i tentativi perché è un nuovo run
    st.session_state.number = get_secret_number()  # Generiamo un nuovo numero segreto
    st.session_state.attempt = 0  # Numero di tentativi
    st.session_state.over = False  # Impostiamo il gioco come non finito


# Incremento per tenere traccia del numero di tentativi nella partita corrente
def restart_game():
    initial_state(is_new_run=False)  # Non è un nuovo run, quindi continuiamo con il run esistente
    st.session_state.attempts_in_current_game += 1  # Incrementiamo i tentativi nella stessa partita


# Inizializzare per chuck api (gioco1)
# Scarica il lessico VADER se non è già presente
nltk.download('vader_lexicon')

# Inizializza l'analizzatore di sentiment
sia = SentimentIntensityAnalyzer()


def fetch_jokes():
    api_url = "https://api.chucknorris.io/jokes/random"
    jokes = []
    for _ in range(10):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            joke = response.json().get('value')
            if joke:
                sentiment = sia.polarity_scores(joke)['compound']
                sentiment_label = (
                    "Positivo" if sentiment > 0.05 else
                    "Negativo" if sentiment < -0.05 else
                    "Neutro"
                )
                jokes.append({"text": joke, "sentiment": sentiment_label})
        except requests.exceptions.RequestException as e:
            st.error(f"Errore nel recupero della battuta: {e}")
    return jokes


# About me per sidebar
def about_me():
    with st.sidebar:
        # Immagine del profilo
        st.image(
            "https://avatars.githubusercontent.com/u/72889405?v=4",
            width=120,
            caption="Veronica Schembri",
            output_format="auto",
        )

        # Nome e descrizione
        st.write("## Veronica Schembri")
        st.write("Front End Developer | Data Science & AI Enthusiast")

        # Sezione Social Media
        st.write("### Social Media")
        st.markdown(
            """
            - [🌐 Sito](https://www.veronicaschembri.com)
            - [🐙 GitHub](https://github.com/Pandagan-85)
            - [🔗 LinkedIn](https://www.linkedin.com/in/veronicaschembri/)
            - [📸 Instagram](https://www.instagram.com/schembriveronica/)
            """
        )


# 📌 Sidebar per selezionare il gioco
# Mostro gli stati per debuggare Indovina il numero
st.sidebar.write("debug state:", st.session_state)
game_choice = st.sidebar.radio("🐼 Scegli cosa vuoi fare:", ["Dog Vision", "Chuck Norris Jokes", "Indovina il numero", "Analisi Film"],
                               index=0)
about_me()

if game_choice == "Indovina il numero":
    st.title("🎲 Indovina il Numero")

    if 'number' not in st.session_state:
        initial_state()

    st.button('Nuova partita', on_click=restart_game)

    placeholder, debug = st.empty(), st.empty()

    guess = placeholder.number_input(
        f'Inserisci un numero tra 1 - {10}',
        key=st.session_state.attempts_in_current_game,  # Usa il tentativo corrente come chiave
        min_value=0,
        max_value=10,
    )

    _, _, _, _, col2 = st.columns(5)

    with col2:
        if not guess:
            st.write(f"Tentativi rimanenti : 7")
        if guess:
            st.write(f"Tentativi rimanenti : {6 - st.session_state.attempt}")

    if guess:
        if st.session_state.attempt < 6:
            st.session_state.attempt += 1
            if guess < st.session_state.number:
                debug.warning(f'{guess} troppo basso!')
            elif guess > st.session_state.number:
                debug.warning(f'{guess} troppo alto!')
            else:
                debug.success(f'Wooooo! Hai indovinato')
                st.balloons()
                st.session_state.over = True
                placeholder.empty()
        else:
            debug.error(f'Mi dispiace hai perso! Il numero era {st.session_state.number}')
            st.session_state.over = True
            placeholder.empty()

# 📌 LOGICA: ANALISI FILM
elif game_choice == "Dog Vision":
    st.title("🐕 Classificatore di Razze Canine")
    st.image("assets_veronica_s/dog.gif", use_container_width=False)
    st.write("Carica una foto del tuo cane e scopri di che razza è!")

    # Istruzioni per caricare correttamente le immagini
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📸 Foto Chiare")
        st.write("Usa immagini ben illuminate per una migliore previsione.")

    with col2:
        st.subheader("🐶 Un Solo Cane")
        st.write(
            "Assicurati che nell'immagine ci sia un solo cane per risultati accurati.")

    with col3:
        st.subheader("🖼️ Buona Qualità")
        st.write("Evita immagini sfocate o parzialmente coperte.")


    # Funzione per preparare le immagini caricate

    def prepare_image(image, img_size=224):
        """
        Prepara un'immagine per il modello:
        1. Ridimensiona a img_size x img_size
        2. Normalizza
        """
        image = tf.image.resize(image, [img_size, img_size])
        return tf.cast(image, tf.float32) / 255.0


    # Funzione per ottenere l'etichetta dalla previsione

    def get_pred_label(prediction_probabilities, unique_breeds):
        """
        Converte le probabilità di previsione in un'etichetta.
        """
        return unique_breeds[np.argmax(prediction_probabilities)]


    # Funzione per creare il grafico a barre delle top N razze

    def plot_top_breeds(prediction_probabilities, unique_breeds, n=10):
        """
        Crea un grafico a barre delle top N razze più probabili utilizzando Altair per una resa estetica migliore.
        """
        # Ottieni gli indici delle top N probabilità
        top_idxs = np.argsort(prediction_probabilities)[-n:][::-1]

        # Ottieni le etichette e i valori corrispondenti
        top_breeds = [unique_breeds[i] for i in top_idxs]
        top_values = [prediction_probabilities[i] * 100 for i in top_idxs]

        # Crea un DataFrame per la visualizzazione
        df = pd.DataFrame({'Breed': top_breeds, 'Confidence': top_values})

        # Crea il grafico con Altair
        chart = (
            alt.Chart(df)
            .mark_bar(cornerRadiusEnd=5)
            .encode(
                x=alt.X("Confidence:Q", title="Confidence (%)"),
                y=alt.Y("Breed:N", sort="-x", title="Razza"),
                color=alt.condition(
                    alt.datum.Confidence == max(df["Confidence"]),
                    # Evidenzia la razza con il valore più alto
                    alt.value("green"),
                    alt.value("skyblue"),
                ),
                tooltip=["Breed", "Confidence"]
            )
            .properties(title="Top 10 Razze Più Probabili", width=600, height=400)
        )

        st.altair_chart(chart, use_container_width=True)


    # Caricamento del modello per la classificazione delle razze canine

    @st.cache_resource
    def load_dog_breed_model():
        """
        Carica il modello salvato con supporto per KerasLayer.
        """
        import tensorflow_hub as hub
        from tensorflow.keras.models import load_model

        # Definisci il custom object scope per KerasLayer
        custom_objects = {'KerasLayer': hub.KerasLayer}

        # Carica il modello con il custom object scope
        model = load_model('assets_veronica_s/modello_veronica_s.h5', custom_objects=custom_objects)
        return model


    # Caricamento del modello per il rilevamento dei cani

    @st.cache_resource
    def load_dog_detector_model():
        """
        Carica il modello per rilevare se un'immagine contiene un cane.
        Utilizziamo un modello MobileNetV2 pre-addestrato su ImageNet.
        """
        # Carica MobileNetV2 pre-addestrato
        base_model = tf.keras.applications.MobileNetV2(
            weights='imagenet', include_top=True)
        return base_model


    # Funzione per verificare se un'immagine contiene un cane

    def is_dog(image, model):
        """
        Verifica se l'immagine contiene un cane utilizzando un modello pre-addestrato.
        Utilizziamo le classi ImageNet dove le classi 151-268 sono razze di cani.

        Args:
            image: immagine in formato PIL
            model: modello pre-addestrato per la classificazione

        Returns:
            bool: True se è un cane, False altrimenti
            float: confidenza nella rilevazione del cane
        """
        # Converti l'immagine nel formato richiesto da MobileNetV2
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_resized = tf.image.resize(img_array, (224, 224))
        img_expanded = tf.expand_dims(img_resized, 0)

        # Preprocessa l'immagine per MobileNetV2
        img_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(
            img_expanded)

        # Ottieni le previsioni
        predictions = model.predict(img_preprocessed)

        # In ImageNet, le classi 151-268 (indici 150-267) sono razze di cani
        dog_class_indices = range(150, 268)

        # Somma le probabilità di tutte le classi di cani
        dog_probability = np.sum(predictions[0][dog_class_indices])

        # Se la probabilità è superiore a una soglia, diciamo che è un cane
        threshold = 0.5  # Puoi modificare questa soglia in base alle tue esigenze
        return dog_probability > threshold, dog_probability


    # Caricamento delle razze uniche

    @st.cache_data
    def load_unique_breeds():
        import json
        try:
            with open('assets_veronica_s/unique_breeds.json', 'r') as f:
                unique_breeds = json.load(f)
            return np.array(unique_breeds)
        except FileNotFoundError:
            st.error("File delle razze non trovato.")
            return None


    # Funzione per fare previsioni sulle immagini caricate

    def predict_breed(image, model, unique_breeds):
        """
        Fa una previsione su un'immagine.
        """
        # Converti l'immagine PIL in un tensore
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        # Prepara l'immagine
        img_processed = prepare_image(img_array)
        # Aggiungi la dimensione del batch
        img_batch = tf.expand_dims(img_processed, axis=0)
        # Fai la previsione
        prediction = model.predict(img_batch)
        # Ottieni l'etichetta
        breed = get_pred_label(prediction[0], unique_breeds)
        # Ottieni il punteggio di confidenza
        confidence = np.max(prediction[0]) * 100
        return breed, confidence, prediction[0], img_processed.numpy()


    # Carica i modelli e le razze
    try:
        dog_breed_model = load_dog_breed_model()
        dog_detector_model = load_dog_detector_model()
        unique_breeds = load_unique_breeds()

        if unique_breeds is None:
            st.warning(
                "Per favore carica il file unique_breeds.npy prima di continuare.")
            # Opzione per caricare il file unique_breeds
            uploaded_breeds = st.file_uploader(
                "Carica il file unique_breeds.npy", type="npy")
            if uploaded_breeds is not None:
                unique_breeds = np.load(uploaded_breeds, allow_pickle=True)
                st.success("Razze caricate con successo!")
    except Exception as e:
        st.error(f"Errore nel caricamento dei modelli o delle razze: {e}")
        st.stop()

    # Interfaccia per il caricamento delle immagini
    uploaded_files = st.file_uploader("Carica una o più immagini di cani in jpg", type=[
        "jpg"], accept_multiple_files=True)

    if uploaded_files:
        st.write(f"Hai caricato {len(uploaded_files)} immagini.")

        # Per ogni immagine caricata
        for i, uploaded_file in enumerate(uploaded_files):
            # Leggi l'immagine caricata
            image = Image.open(uploaded_file)

            # Crea due colonne: una per l'immagine, una per il grafico
            col1, col2 = st.columns([1, 1.5])

            with col1:
                st.image(
                    image, caption=f"Immagine {i + 1}", use_container_width=True)

                # Verifica se l'immagine contiene un cane
                is_dog_image, dog_confidence = is_dog(image, dog_detector_model)

                if is_dog_image:
                    st.success(
                        f"✅ L'immagine contiene un cane (confidenza: {dog_confidence * 100:.1f}%)")

                    # Fai la previsione della razza solo se l'immagine contiene un cane
                    breed, confidence, prediction_probs, processed_img = predict_breed(
                        image, dog_breed_model, unique_breeds)

                    st.success(f"Razza predetta: {breed}")
                    st.info(f"Confidenza: {confidence:.2f}%")

                    # Pulsante per vedere l'immagine preprocessata
                    if st.button(f"Mostra immagine preprocessata {i + 1}"):
                        st.image(
                            processed_img, caption="Immagine preprocessata", use_container_width=True)

                    with col2:
                        # Crea e mostra il grafico delle top 10 razze
                        plot_top_breeds(prediction_probs, unique_breeds, n=10)
                else:
                    st.error(
                        f"❌ L'immagine non sembra contenere un cane (confidenza cane: {dog_confidence * 100:.1f}%)")
                    st.warning(
                        "Per favore carica un'immagine con un cane per vedere la classificazione delle razze.")

            # Aggiungi un separatore tra le immagini
            if i < len(uploaded_files) - 1:
                st.markdown("---")
    else:
        # Mostra alcune istruzioni quando non ci sono immagini caricate
        st.info("Carica le foto dei cani per vedere le previsioni e i grafici delle razze più probabili.")

        # Opzionale: mostra esempi di razze che il modello può identificare
        if unique_breeds is not None and len(unique_breeds) > 0:
            st.write("Alcune delle razze che il modello può identificare:")
            sample_breeds = unique_breeds[:10] if len(
                unique_breeds) > 10 else unique_breeds
            st.write(", ".join(sample_breeds))

    # Aggiungi una nota informativa
    st.markdown("---")
    st.write("Questo classificatore utilizza un modello di deep learning addestrato su diverse razze di cani.")
    st.write("Nota: l'accuratezza delle previsioni può variare in base alla qualità dell'immagine.")
    # Aggiungi il link alla repo
    st.markdown(
        "### Vuoi scoprire il processo dietro la costruzione del modello? Dai un’occhiata al notebook su GitHub! Il modello è stato realizzato con TensorFlow utilizzando il transfer learning su MobileNet 👇")
    st.markdown(
        "🔗 [Codice Notebook per il lavoro sul modello su GitHub](https://github.com/Pandagan-85/ZTM-Machine-learning/blob/main/end_to_end_dog_vision.ipynb)")




# 📌 LOGICA: ANALISI FILM
elif game_choice == "Analisi Film":
    st.title("🎥 Hollywood movies!")
    st.markdown("Questa è una lista di film prodotti dal 2007 al 2013")


    @st.cache_data
    def load_data():
        url = "https://raw.githubusercontent.com/reisanar/datasets/refs/heads/master/HollywoodMovies.csv"
        df = pd.read_csv(url)
        return df


    df = load_data()

    # Mostra le prime righe del dataframe
    st.write(df.head())

    # Aggiungi "All" come opzione per l'anno
    years = ['All'] + list(df['Year'].unique())
    selected_anno = st.selectbox('Scegli l\'anno', years, index=0)

    # Aggiungi l'opzione "All" al filtro per il genere
    genres = ['All'] + list(df['Genre'].unique())
    genre = st.selectbox('Scegli il genere', genres, index=0)

    # Applica i filtri
    if selected_anno == 'All' and genre == 'All':
        df_filtered = df  # Nessun filtro applicato, mostra tutto
    elif selected_anno == 'All':
        df_filtered = df[df['Genre'] == genre]  # Filtro solo per genere
    elif genre == 'All':
        df_filtered = df[df['Year'] == selected_anno]  # Filtro solo per anno
    else:
        df_filtered = df[(df['Year'] == selected_anno) & (df['Genre'] == genre)]  # Filtro per anno e genere

    # Mostra i dati filtrati
    anno_genere = f"dell'anno {selected_anno} e del genere {genre}" if selected_anno != 'All' and genre != 'All' else ''
    st.subheader(f"Film {anno_genere}")
    st.write(df_filtered)

    st.divider()
    st.subheader('Numero di film per anno raggruppati per genere')
    movies_per_year_genre = df.groupby(["Year", "Genre"]).size().reset_index(name="Count")

    # Crea un grafico a barre
    plt.figure(figsize=(12, 6))
    sns.barplot(data=movies_per_year_genre, x="Year", y="Count", hue="Genre", palette="pastel")

    # Personalizza il grafico
    plt.title("Numero di Film per Anno e Genere")
    plt.xlabel("Anno di Uscita")
    plt.ylabel("Numero di Film")
    plt.xticks(rotation=45)
    plt.legend(title="Genere", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Mostra il grafico in Streamlit
    st.pyplot(plt)

    st.write(
        'Ha quasi sempre vinto la commedia, tranne più recentemente, dove si è fatto strada il drama, e action. Sembra anche che vengano prodotti molti meno film dal 2011')

    st.divider()

    st.subheader('Rapporto tra Budget e World gross')

    st.write(
        """
    - Se la barra arancione (World Gross) è molto più lunga della barra gialla (Budget), il film è stato un successo.
- Se le due barre sono simili, il film ha recuperato il budget ma senza grandi guadagni.
 - Se la barra gialla è più lunga, il film ha perso soldi! (Green Lantern è stato 💩💩💩, povero Ryan Reynolds)
        """)
    action_movies = df[df["Genre"] == "Action"].sort_values(by="Budget", ascending=False)

    # Seleziona i primi 10 film d'azione
    top_action_movies = action_movies.head(10)

    # Creazione del grafico
    plt.figure(figsize=(10, 5))
    plt.barh(top_action_movies["Movie"], top_action_movies["WorldGross"], color="orange", label="World Gross")
    plt.barh(top_action_movies["Movie"], top_action_movies["Budget"], color="yellow", alpha=0.6, label="Budget")

    # Aggiungi titoli ed etichette
    plt.xlabel("Importo ($ Milioni)")
    plt.ylabel("Film")
    plt.title("Budget vs World Gross per i film Action più costosi")
    plt.legend()
    plt.gca().invert_yaxis()  # Per avere il film più costoso in alto

    # Mostra il grafico in Streamlit
    st.pyplot(plt)

    st.divider()

    st.markdown(
        """
        ## Differenza tra critici e pubblico per tutti i film (RottenTomatoes vs. AudienceScore)
        Grafico a dispersione (scatter plot) che confronta i punteggi di Rotten Tomatoes (critici) e di AudienceScore (pubblico) per ogni film, con il budget che influenza sia il colore che la dimensione dei punti.

Relazione tra critica e pubblico: Se i punti sono allineati lungo una diagonale (da sinistra a destra), significa che critici e pubblico hanno valutato in modo simile i film. Se i punti si disperdono molto tra l’asse X e l’asse Y, potrebbe significare che c’è una discrepanza tra la valutazione dei critici e quella del pubblico.
Effetto del budget:
Se vedi che i film con budget alto tendono ad avere punteggi migliori da parte della critica o del pubblico, potrebbe indicare che un alto investimento porta a un prodotto più apprezzato.
Se i punti grandi (alta dimensione) sono distribuiti in modo uniforme tra alti e bassi punteggi, potrebbe suggerire che un grande budget non garantisce necessariamente un buon risultato dal punto di vista delle recensioni.
Cluster di punti: Se noti gruppi di punti concentrati in una specifica area (ad esempio, budget medio con alti punteggi sia da parte della critica che del pubblico), potrebbe indicare che quella fascia di budget è particolarmente apprezzata.
        """
    )

    # Crea il grafico a dispersione (scatterplot)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="RottenTomatoes", y="AudienceScore", hue="Budget", size="Budget", sizes=(20, 200),
                    palette="coolwarm")

    # Aggiungi titoli e etichette
    plt.xlabel("Punteggio Critici (RottenTomatoes)")
    plt.ylabel("Punteggio Pubblico (AudienceScore)")
    plt.title("Confronto tra Critici e Pubblico")
    plt.legend(title="Budget")

    # Mostra il grafico in Streamlit
    st.pyplot(plt)

# 📌 LOGICA: CHUCK JOKE
elif game_choice == "Chuck Norris Jokes":
    st.title("😂 Analisi NLP delle battute di Chuck Norris")
    st.markdown("""
        Questa app genera 10 battute casuali di Chuck Norris e ne analizza il
        tono usando il Natural Language Processing (NLP).

        ✅ Ogni battuta viene analizzata con **NLTK** (sentiment
          positivo, negativo o neutro).

    """)


    # Funzione per ottenere il colore in base al sentimento
    def get_sentiment_color(sentiment):
        if sentiment == "Positivo":
            return "green"
        elif sentiment == "Negativo":
            return "red"
        else:
            return "blue"


    buff, col, buff2 = st.columns([0.1, 0.8, 0.1])
    with col:
        st.image(
            "https://raw.githubusercontent.com/Pandagan-85/chuck-front/refs/heads/main/public/Chuck_norris_mia_illustrazione.png")
        if st.button("Genera 10 Battute"):
            jokes = fetch_jokes()
            # Visualizza le battute con il colore corrispondente al sentimento
            for joke in jokes:
                container = st.container(border=True)
                color = get_sentiment_color(joke["sentiment"])
                container.write(f":{color}[{joke['text']}]")
                container.write(f"**Sentimento:** :{color}[{joke['sentiment']}]")



