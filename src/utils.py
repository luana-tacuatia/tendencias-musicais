import os
from typing import Any
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from typing import Optional

def get_api_key() -> str:
    load_dotenv()
    key = os.getenv("LASTFM_API_KEY") or st.secrets.get("LASTFM_API_KEY")
    if not key:
        raise ValueError("API key do Last.fm não encontrada. Configure .env ou st.secrets")
    return key

def safe_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None

def tracks_to_dataframe(tracks: list) -> 'pd.DataFrame':    
    df = pd.DataFrame([t.to_dict() for t in tracks])
    if "Playcount" in df.columns:
        try:
            df_sorted = df.copy()
            df_sorted["_pc_sort"] = df_sorted["Playcount"].apply(lambda x: int(x) if isinstance(x, (int, float)) else -1)
            df_sorted = df_sorted.sort_values("_pc_sort", ascending=False).drop(columns=["_pc_sort"]).reset_index(drop=True)

            # Adiciona a coluna de posição começando em 1
            df_sorted.insert(0, "Posição", range(1, len(df_sorted) + 1))

            return df_sorted
        except Exception:
            # Mesmo em caso de erro, adiciona posição
            df.insert(0, "Posição", range(1, len(df) + 1))
            return df
    else:
        # Se não houver Playcount, apenas adiciona a posição
        df.insert(0, "Posição", range(1, len(df) + 1))
    return df
