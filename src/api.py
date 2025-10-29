import requests
from src.models import Track
from src.utils import safe_int
import streamlit as st
from src.constants import LASTFM_API_BASE

# =====================================================
# Funções auxiliares de API
# =====================================================

def _fetch_track_info(track: str, artist: str, api_key: str) -> int | None:
    """Busca o playcount detalhado de uma música."""
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

def _fetch_track_tags(track: str, artist: str, api_key: str) -> str | None:
    """Busca as tags (gêneros) mais populares associadas a uma música."""
    params = {
        "method": "track.getTopTags",
        "track": track,
        "artist": artist,
        "api_key": api_key,
        "format": "json",
    }
    resp = requests.get(LASTFM_API_BASE, params=params, timeout=10)
    data = resp.json()
    try:
        tags = data.get("toptags", {}).get("tag", [])
        if isinstance(tags, list) and len(tags) > 0:
            # Retorna os dois principais gêneros
            return ", ".join([t["name"].title() for t in tags[:2]])
        elif isinstance(tags, dict):
            return tags.get("name", "").title()
        else:
            return None
    except Exception:
        return None

def _fetch_artist_tags(artist: str, api_key: str) -> str | None:
    """Busca as tags (gêneros) mais populares associadas a um artista."""
    params = {
        "method": "artist.getTopTags",
        "artist": artist,
        "api_key": api_key,
        "format": "json",
    }
    resp = requests.get(LASTFM_API_BASE, params=params, timeout=10)
    data = resp.json()
    try:
        tags = data.get("toptags", {}).get("tag", [])
        if isinstance(tags, list) and len(tags) > 0:
            return ", ".join([t["name"].title() for t in tags[:2]])
        elif isinstance(tags, dict):
            return tags.get("name", "").title()
        else:
            return None
    except Exception:
        return None

# =====================================================
# Funções principais de coleta
# =====================================================

@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def fetch_geo_toptracks(country: str, limit: int, api_key: str) -> list[Track]:
    """Busca as músicas mais populares de um país."""
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
        playcount = _fetch_track_info(name, artist, api_key)

        # Novas chamadas para gêneros
        genre = _fetch_track_tags(name, artist, api_key)
        artist_genre = _fetch_artist_tags(artist, api_key)

        tracks.append(Track(
            name=name,
            artist=artist,
            playcount=playcount,
            listeners=listeners,
            genre=genre,
            artist_genre=artist_genre,
        ))
    return tracks


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def fetch_global_toptracks(limit: int, api_key: str) -> list[Track]:
    """Busca as músicas mais populares globalmente."""
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
        name = t.get("name", "")
        artist = t.get("artist", {}).get("name", "")
        playcount = safe_int(t.get("playcount"))
        listeners = safe_int(t.get("listeners"))

        # Novas chamadas para gêneros
        genre = _fetch_track_tags(name, artist, api_key)
        artist_genre = _fetch_artist_tags(artist, api_key)

        tracks.append(Track(
            name=name,
            artist=artist,
            playcount=playcount,
            listeners=listeners,
            genre=genre,
            artist_genre=artist_genre,
        ))
    return tracks
