import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import streamlit as st

# URL del dataset
url = 'https://dati.beniculturali.it/dataset/dataset-eventiMeseCorrente.json'

st.title("Analisi del dataset - Eventi culturali in Italia 🌍")

# Funzione per ottenere il label
def get_label(item):
    label = item.get("rdfs:label", "Sconosciuto")
    if isinstance(label, list) and len(label) > 0:
        first_elem = label[0]
        return first_elem["@value"] if isinstance(first_elem, dict) else first_elem
    elif isinstance(label, dict):
        return label.get("@value", "Sconosciuto")
    elif isinstance(label, str):
        return label
    else:
        return "Sconosciuto"


# Funzione per caricare i dati
def load_data():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "@graph" in data:
                data = data["@graph"]
            else:
                st.error("Errore: chiave '@graph' non trovata nel JSON.")
                return pd.DataFrame()

            df = pd.DataFrame([{
                "nome": get_label(item),
                "indirizzo": item.get("clvapit:fullAddress", "Sconosciuto"),
                "regione": item.get("clvapit:hasRegion", {}).get("@id", "").split("/")[-1] or "Sconosciuto",
                "provincia": item.get("clvapit:hasProvince", {}).get("@id", "").split("/")[-1] or "Sconosciuto",
                "città": item.get("clvapit:hasCity", {}).get("@id", "").split("/")[-1] or "Sconosciuto"
            } for item in data])
            return df
        else:
            st.error("Errore nel download del JSON")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta API: {e}")
        return pd.DataFrame()


# Funzione principale per visualizzare i dati e le analisi
def main():
    # Carica i dati
    df = load_data()

    # Verifica se il DataFrame è vuoto
    if df.empty:
        st.warning("Il dataset è vuoto o non ha la struttura prevista.")
    else:
        # Mostra le prime righe
        st.subheader("Prime righe del dataset")
        st.write(df.head())

        # Analisi 1: Distribuzione delle strutture per regione
        st.subheader("Distribuzione dei luoghi culturali per regione")
        df_filtered = df[df['regione'] != 'Sconosciuto']
        region_counts = df_filtered['regione'].value_counts()
        fig, ax = plt.subplots(figsize=(12, 8))
        region_counts.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title('Distribuzione dei luoghi culturali per regione')
        ax.set_xlabel('Regione')
        ax.set_ylabel('Numero di luoghi culturali')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Commento
        st.markdown("""
        ### 📊 Grafico a barre: Distribuzione dei luoghi culturali per regione

        Il grafico a barre mostra la distribuzione dei luoghi culturali per regione d'Italia. Ogni barra rappresenta il numero di luoghi culturali presenti in ciascuna regione. Alcune regioni emergono con un numero significativamente maggiore di luoghi culturali rispetto ad altre (Lazio, Toscana, Campania). Questo può indicare una maggiore concentrazione di risorse culturali e infrastrutture nelle aree con più barre alte. La differenza nel numero di luoghi culturali tra le diverse regioni suggerisce una distribuzione geografica disomogenea. Alcune regioni, specialmente quelle con una maggiore densità di popolazione o una tradizione storica e culturale consolidata, possono vantare un numero più alto di strutture culturali.
        """)

        # Analisi 2: Top 10 province con più strutture
        st.subheader("Distribuzione dei luoghi culturali per provincia (prime 10)")
        df_filtered = df[df['provincia'] != 'Sconosciuto']
        province_counts = df_filtered['provincia'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(12, 8))
        province_counts.plot(kind='bar', color='lightgreen', ax=ax)
        ax.set_title('Distribuzione dei luoghi culturali per provincia (prime 10)')
        ax.set_xlabel('Provincia')
        ax.set_ylabel('Numero di luoghi culturali')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Commento
        st.markdown("""
        ### 📊 Grafico a barre: Distribuzione dei luoghi culturali per provincia

        Il grafico a barre mostra la distribuzione dei luoghi culturali per provincia in Italia, escludendo i casi in cui la provincia è "Sconosciuto". Sono state selezionate le prime 10 province con il maggior numero di luoghi culturali. Le prime 10 province, evidenziate nel grafico, mostrano una forte concentrazione di luoghi culturali, indicando che alcune aree hanno una presenza culturale significativamente maggiore rispetto ad altre. Le province con le barre più alte sono quelle con il numero maggiore di strutture culturali (Roma e Firenze). La distribuzione dei luoghi culturali tra le province mostra una forte disparità, con alcune province che emergono nettamente per numero di luoghi, mentre altre sono meno rappresentate. Questo potrebbe essere il riflesso di differenze economiche, storiche e sociali tra le diverse aree del paese. L'analisi potrebbe suggerire che investimenti in cultura nelle province meno rappresentate potrebbero contribuire a bilanciare la distribuzione culturale a livello nazionale e ad aumentare l'accesso alla cultura per un pubblico più ampio, anche nelle aree meno centrali.
        """)

        # Analisi 3: Distribuzione delle strutture per città
        st.subheader("Distribuzione dei luoghi culturali per città (prime 10)")
        df_filtered = df[df['città'] != 'Sconosciuto']
        city_counts = df_filtered['città'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(12, 8))
        city_counts.plot(kind='bar', color='salmon', ax=ax)
        ax.set_title('Distribuzione dei luoghi culturali per città (prime 10)')
        ax.set_xlabel('Città')
        ax.set_ylabel('Numero di luoghi culturali')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Commento
        st.markdown("""
        ### 📊 Grafico a barre: Distribuzione dei luoghi culturali per città

        Le città con il numero maggiore di luoghi culturali sono facilmente identificabili grazie alle barre più alte (Roma e Firenze, Siena e Napoli a seguire). Queste città rappresentano i principali centri culturali del paese, con una forte presenza di strutture dedicate alla cultura, come musei, teatri e gallerie. L'analisi suggerisce che, sebbene le principali città siano ben servite da strutture culturali, ci potrebbe essere un'opportunità di crescita per le città più piccole o meno centrali, che potrebbero beneficiare di investimenti mirati nel settore culturale per migliorare la loro offerta e attrarre più visitatori.
        """)

        # Analisi 4: Mappa della distribuzione dei luoghi culturali per regione
        st.subheader("Mappa della distribuzione dei luoghi culturali per regione")
        df_filtered = df[df['regione'] != 'Sconosciuto']
        region_counts = df_filtered['regione'].value_counts().reset_index()
        region_counts.columns = ['regione', 'count']
        italy_regions = gpd.read_file(
            "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson")
        italy_regions = italy_regions.merge(region_counts, left_on="reg_name", right_on="regione", how="left").fillna(0)
        fig, ax = plt.subplots(1, 1, figsize=(10, 12))
        italy_regions.plot(column="count", cmap="OrRd", linewidth=0.8, edgecolor="black", legend=True, ax=ax)
        plt.title("Distribuzione dei luoghi culturali per regione in Italia")
        plt.axis("off")
        st.pyplot(fig)

        # Commento
        st.markdown("""
        ### 🌍 Mappa tematica-coropletica: Distribuzione geografica dei luoghi culturali

        Il grafico presentato è una mappa tematica o mappa coropletica. In una mappa coropletica, le aree geografiche (in questo caso, le regioni italiane) sono colorate in base a una variabile quantitativa (in questo caso, il numero di luoghi culturali per regione). Il colore delle regioni varia a seconda del valore indicato, permettendo di evidenziare le aree con valori più alti o più bassi. Le regioni con una maggiore concentrazione di luoghi culturali sono evidenziate con tonalità più scure, mentre quelle con una presenza inferiore sono più chiare. Questo grafico fornisce una visione della distribuzione geografica dei luoghi culturali in Italia, evidenziando le aree che potrebbero richiedere più attenzione o interventi di sviluppo in termini di accesso alla cultura.
        """)

        # Analisi 5: Distribuzione percentuale dei luoghi culturali per regione
        st.subheader("Distribuzione percentuale dei luoghi culturali per regione")
        df_filtered = df[df['regione'] != 'Sconosciuto']
        region_counts = df_filtered['regione'].value_counts()
        top_regions = region_counts[:10]
        others_count = region_counts[10:].sum()
        top_regions["Altre"] = others_count
        fig, ax = plt.subplots(figsize=(10, 6))
        top_regions.plot(kind='pie', autopct='%1.1f%%', cmap='tab10', startangle=140, ax=ax)
        ax.set_title("Distribuzione percentuale dei luoghi culturali per regione in Italia")
        ax.set_ylabel("")
        st.pyplot(fig)

        # Commento
        st.markdown("""
        ### 📊 Grafico a torta: Distribuzione percentuale dei luoghi culturali per regione

        Il grafico a torta mostra la distribuzione percentuale dei luoghi culturali per regione in Italia. Le prime 10 regioni sono rappresentate con le fette più grandi, mentre le regioni minori sono riunite nella categoria "Altre". Questo grafico mostra la distribuzione dei luoghi culturali e suggerisce una possibile necessità di politiche culturali più inclusive a livello nazionale.
        """)

# Avvio della funzione main
if __name__ == "__main__":
    main()