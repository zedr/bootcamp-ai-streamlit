import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


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
game_choice = st.sidebar.radio("🐼 Scegli cosa vuoi fare:", ["Indovina il numero", "Analisi Film", "Chuck Norris Jokes"],
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
    st.subheader(
        f"Film {('dell\'anno ' + str(selected_anno) + ' e del genere ' + genre) if selected_anno != 'All' and genre != 'All' else ''}")
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



