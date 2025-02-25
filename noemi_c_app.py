import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="Dashboard Interattiva & Machine Learning", layout="wide")

# Titolo dell'app
st.title("Dashboard Interattiva con Predizioni di Machine Learning")

# Caricamento dinamico del file CSV
uploaded_file = st.file_uploader("Carica un file CSV", type=["csv"])


@st.cache_data
def load_data(file):
    df = pd.read_csv(file, sep=';', encoding='latin1')
    df.columns = ['Anno', 'Tipologia', 'Numero Premi/Sussidi', 'Importo Complessivo (€)',
                  'Modalità di Assegnazione', 'Numero Candidati', 'Numero Premi/Sussidi Erogati']
    numeric_columns = ['Numero Premi/Sussidi', 'Importo Complessivo (€)', 'Numero Candidati',
                       'Numero Premi/Sussidi Erogati']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    return df


if uploaded_file:
    df = load_data(uploaded_file)
    st.success("Dati caricati con successo!")

    # Dashboard Interattiva
    st.header("Dashboard Interattiva")

    # Selezione della variabile numerica per il grafico
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    selected_x_var = st.selectbox("Seleziona la Variabile X", options=numeric_columns, index=0)
    selected_y_var = st.selectbox("Seleziona la Variabile Y", options=numeric_columns, index=1)

    # Grafico interattivo con Plotly
    st.subheader("Grafico Interattivo")
    fig = px.scatter(df, x=selected_x_var, y=selected_y_var, color="Tipologia",
                     title=f"{selected_y_var} vs {selected_x_var}", template="plotly_white")
    st.plotly_chart(fig)

    # Analisi delle correlazioni
    st.subheader("Matrice di Correlazione")
    numeric_df = df.select_dtypes(include=[np.number])
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    # Sezione di Predizione con Machine Learning
    st.header("Predizioni con Machine Learning")

    # Selezione delle feature per il modello
    st.markdown("**Seleziona le variabili per addestrare il modello di previsione:**")
    selected_features = st.multiselect("Scegli le feature", options=numeric_columns, default=numeric_columns[:-1])
    target_variable = st.selectbox("Scegli la variabile target", options=numeric_columns,
                                   index=len(numeric_columns) - 1)

if st.button("Addestra il Modello"):
    # Preparazione dei dati
    X = df[selected_features].dropna()
    y = df[target_variable].dropna()
    X, y = X.align(y, join='inner', axis=0)

    # Controlla la dimensione del dataset
    st.write(f"Numero di campioni disponibili per l'addestramento: {len(X)}")

    if len(X) < 2:
        st.error("Il dataset è troppo piccolo per addestrare un modello. Aggiungi più dati o modifica i filtri.")
    else:
        test_size = 0.2 if len(X) > 5 else 0.5  # Aumenta il test_size se ci sono pochi campioni
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        # Addestramento del modello di Random Forest
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predizioni
        y_pred = model.predict(X_test)

        # Metriche di valutazione
        st.subheader("Valutazione del Modello")
        st.write(f"**R2 Score:** {r2_score(y_test, y_pred):.2f}")
        st.write(f"**Mean Squared Error:** {mean_squared_error(y_test, y_pred):.2f}")

        # Grafico delle predizioni vs valori reali
        st.subheader("Confronto tra Valori Reali e Predetti")
        result_df = pd.DataFrame({"Valori Reali": y_test, "Valori Predetti": y_pred})
        fig = px.scatter(result_df, x="Valori Reali", y="Valori Predetti",
                         title="Confronto Predizioni vs Valori Reali", template="plotly_white")
        st.plotly_chart(fig)