import streamlit as st
import pandas as pd
import requests
from matplotlib import pyplot as plt
import seaborn as sns

st.title('Analisi dati sui laureati a Milano (Giorgia V)')


url = "https://dati.comune.milano.it/dataset/ae03c361-051b-4f75-8174-f343b198602d/resource/f5a5cc0f-b95c-47b2-b380-7bf2c55079fb/download/ds764_laureati_per_genere_anno_solare_2013.json"
response = requests.get(url)

data = response.json()
df = pd.DataFrame(data)
st.title('Dataset 2013')
st.write(df)
#Vedo le informazioni più importanti sul dataset tramite:
df.info()
df.describe()
#Controllo se ci sono dati nan:
df.isnull().sum()
#Non ci sono dati nulli. Quindi non ho bisogno di ripulire i dati.
#Vediamo la percentuale di laureati per diversi atenei di Milano nel 2013


labels_0 = list(set(df['NOME_ATENEO']))
sizes_0 = list(df['LAUREATI_TOTALE'].loc[df['Sesso']=='M'])

fig0, ax0 = plt.subplots()
plt.title('Laureati uomini nel 2013')
ax0.pie(sizes_0,labels=labels_0,autopct="%.2f%%")
st.pyplot(fig0)


labels_1 = list(set(df['NOME_ATENEO']))
sizes_1 = list(df['LAUREATI_TOTALE'].loc[df['Sesso']=='F'])

fig1, ax1 = plt.subplots()
plt.title('Laureate donne nel 2013')
ax1.pie(sizes_1,labels=labels_1,autopct="%.2f%%")
st.pyplot(fig1)


st.write('Vediamo la differenza di genere dei laureati:')
fig11, ax11 = plt.subplots()
sns.barplot(
x="Sesso",
y="LAUREATI_TOTALE",
data=df
)
plt.title("Laureati suddivisi per genere (2013)")
st.pyplot(fig11)
st.write('Le donne laureate sono in numero maggiore rispetto agli uomini nel 2013.')

url2 = "https://dati.comune.milano.it/dataset/c8cc2240-f6d2-4b8f-a230-1fb22a3ea190/resource/5b2ff8f3-2005-49d3-a8dd-6288a2327a1f/download/ds2714_laureati_negli_atenei_milanesi.json"
resp2 = requests.get(url2)
data2 = resp2.json()
df2 = pd.DataFrame(data2)
st.title('Dataset 2021')
st.write(df2)

labels2 = list(set(df2['AteneoNOME']))
sizes2 = list(df2['Femmine'])

fig, ax = plt.subplots()
plt.title('Laureate donne nel 2021')
ax.pie(sizes2,labels=labels2,autopct="%.2f%%")
st.pyplot(fig)

labels3 = list(set(df2['AteneoNOME']))
sizes3 = list(df2['Maschi'])

fig3, ax3 = plt.subplots()
plt.title('Laureati uomini nel 2021')
ax3.pie(sizes3,labels=labels3,autopct="%.2f%%")
st.pyplot(fig3)

fig4, ax4 = plt.subplots(figsize=(15,5))
ax4.plot(df2['AteneoNOME'],df2['Femmine'])
ax4.plot(df2['Maschi'])
ax4.legend(['Femmine','Maschi'])
plt.title("Laureati donne e uomini nei vari atenei milanesi (2021)")
st.pyplot(fig4)

st.write('Dammi un feedback sulla mia analisi dati!')
voto = st.slider('Voto:',1,10,5)

st.write('Inserisci il tuo nome:')
name = st.text_input('Nome:')

st.write('Grazie', name, 'per il feedback, hai votato il mio lavoro con', voto)

