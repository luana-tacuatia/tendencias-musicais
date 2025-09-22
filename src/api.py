import requests
from src.models import Track
from src.utils import safe_int
import streamlit as st

LASTFM_API_BASE = "https://ws.audioscrobbler.com/2.0/"

def _fetch_track_info(track: str, artist: str, api_key: str) -> int | None:
    """Busca playcount detalhado de uma música usando track.getInfo"""
    params = {
        "method": "track.getInfo",
        "track": track,
        "artist": artist,
        "api_key": api_key,
        "format": "json",
    }
    resp = requests.get(LASTFM_API_BASE, params=params, timeout=10)
    data = resp.json()
    try:
        return safe_int(data["track"].get("playcount"))
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def fetch_geo_toptracks(country: str, limit: int, api_key: str) -> list[Track]:
    params = {
        "method": "geo.gettoptracks",
        "country": country,
        "limit": limit,
        "api_key": api_key,
        "format": "json",
    }
    resp = requests.get(LASTFM_API_BASE, params=params, timeout=10)
    data = resp.json()
    if "tracks" not in data or "track" not in data["tracks"]:
        raise RuntimeError(f"Erro ao obter top tracks de {country}")
    
    tracks = []
    for t in data["tracks"]["track"]:
        name = t.get("name", "")
        artist = t.get("artist", {}).get("name", "")
        listeners = safe_int(t.get("listeners"))
        # agora buscamos o playcount de cada música individualmente
        playcount = _fetch_track_info(name, artist, api_key)
        tracks.append(Track(
            name=name,
            artist=artist,
            playcount=playcount,
            listeners=listeners,
        ))
    return tracks

@st.cache_data(show_spinner=False)
def fetch_global_toptracks(limit: int, api_key: str) -> list[Track]:
    params = {
        "method": "chart.gettoptracks",
        "limit": limit,
        "api_key": api_key,
        "format": "json",
    }
    resp = requests.get(LASTFM_API_BASE, params=params, timeout=10)
    data = resp.json()
    if "tracks" not in data or "track" not in data["tracks"]:
        raise RuntimeError("Erro ao obter top tracks globais")
    
    tracks = []
    for t in data["tracks"]["track"]:
        tracks.append(Track(
            name=t.get("name", ""),
            artist=t.get("artist", {}).get("name", ""),
            playcount=safe_int(t.get("playcount")),
            listeners=safe_int(t.get("listeners")),
        ))
    return tracks
