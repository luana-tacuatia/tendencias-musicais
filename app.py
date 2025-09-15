import requests
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('LASTFM_API_KEY')

st.title('Tendências Musicais com Last.fm API')

artist = st.text_input('Digite o nome do artista:')

if artist:
    url = f'https://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist}&api_key={API_KEY}&format=json'
    response = requests.get(url)
    data = response.json()

    if "toptracks" in data and "track" in data["toptracks"]:
        tracks = data["toptracks"]["track"]
        df = pd.DataFrame(tracks)
        st.dataframe(df[['name', 'playcount', 'listeners']])
    else:
        st.error('Artista não encontrado ou erro na API.')
