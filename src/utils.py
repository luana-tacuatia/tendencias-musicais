import os
import json
import datetime
from pathlib import Path
from typing import Any, Optional
import pandas as pd
import streamlit as st
import altair as alt
from dotenv import load_dotenv
import time

# ========================
# API Key
# ========================
def get_api_key() -> str:
    load_dotenv()
    key = os.getenv("LASTFM_API_KEY") or st.secrets.get("LASTFM_API_KEY")
    if not key:
        raise ValueError("API key do Last.fm não encontrada. Configure .env ou st.secrets")
    return key

# ========================
# Conversões seguras
# ========================
def safe_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None

# ========================
# Conversão de tracks para DataFrame
# ========================
def tracks_to_dataframe(tracks: list) -> pd.DataFrame:
    df = pd.DataFrame([t.to_dict() for t in tracks])
    if "Playcount" in df.columns:
        try:
            df_sorted = df.copy()
            df_sorted["_pc_sort"] = df_sorted["Playcount"].apply(
                lambda x: int(x) if isinstance(x, (int, float)) else -1
            )
            df_sorted = df_sorted.sort_values("_pc_sort", ascending=False).drop(columns=["_pc_sort"]).reset_index(drop=True)
            df_sorted.insert(0, "Posição", range(1, len(df_sorted) + 1))
            return df_sorted
        except Exception:
            df.insert(0, "Posição", range(1, len(df) + 1))
            return df
    else:
        df.insert(0, "Posição", range(1, len(df) + 1))
    return df

# ========================
# Salvamento semanal genérico
# ========================
def save_weekly_snapshot(df: pd.DataFrame, region: str = "Brasil", base_dir: str = "data"):
    output_dir = Path(base_dir) / region.lower().replace(" ", "_")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.date.today()
    year, week, weekday = today.isocalendar()
    file_path = output_dir / f"{year}-W{week}.json"

    if weekday == 2 and not file_path.exists():  # quarta-feira
        df.to_json(file_path, orient="records", force_ascii=False, indent=2)
        st.toast(f"📁 Snapshot semanal salvo ({region}): {file_path}", icon="💾")
    elif file_path.exists():
        st.info(f"📁 Snapshot já existe para {region}, semana {week}: {file_path}")

# ========================
# Carregar snapshots semanais
# ========================
def load_weekly_snapshots(region: str = "Brasil", base_dir: str = "data"):
    folder = Path(base_dir) / region.lower().replace(" ", "_")
    if not folder.exists():
        return []
    files = sorted(folder.glob("*.json"))
    dfs = []
    for f in files:
        week = int(f.stem.split("-W")[1])
        dfs.append((week, pd.read_json(f)))
    return dfs

# ========================
# Comparação de semanas
# ========================
def compare_weeks(region: str = "Brasil", base_dir: str = "data", top_n: int = 5, analysis_type: str = "Top Músicas"):
    dfs = load_weekly_snapshots(region, base_dir)
    if len(dfs) < 2:
        st.info("Ainda não há dados suficientes para comparação semanal.")
        return

    week1, df1 = dfs[-2]
    week2, df2 = dfs[-1]

    # Seleciona colunas de interesse de acordo com o tipo de análise
    if analysis_type == "Top Músicas":
        cols_needed = ["Música", "Playcount", "Listeners"]
    elif analysis_type == "Top Artistas":
        cols_needed = ["Artista", "Playcount", "Listeners"]
    elif analysis_type == "Top Gêneros Musicais":
        cols_needed = ["Gênero musical da música", "Playcount", "Listeners"]
    else:
        cols_needed = ["Música", "Playcount", "Listeners"]

    df1_subset = df1[[c for c in cols_needed if c in df1.columns]].copy()
    df2_subset = df2[[c for c in cols_needed if c in df2.columns]].copy()

    df1_subset = df1_subset.loc[:, ~df1_subset.columns.duplicated()]
    df2_subset = df2_subset.loc[:, ~df2_subset.columns.duplicated()]

    # Garantir colunas obrigatórias
    for col in cols_needed:
        if col not in df1_subset.columns:
            df1_subset[col] = "" if "Playcount" not in col and "Listeners" not in col else 0
        if col not in df2_subset.columns:
            df2_subset[col] = "" if "Playcount" not in col and "Listeners" not in col else 0

    key_col = cols_needed[0]  # primeira coluna é usada para merge
    merged = df1_subset.merge(df2_subset, on=key_col, suffixes=(f"_sem{week1}", f"_sem{week2}"))

    merged["ΔPlaycount"] = merged.filter(like=f"Playcount_sem{week2}").iloc[:, 0] - \
                           merged.filter(like=f"Playcount_sem{week1}").iloc[:, 0]
    merged["ΔListeners"] = merged.filter(like=f"Listeners_sem{week2}").iloc[:, 0] - \
                            merged.filter(like=f"Listeners_sem{week1}").iloc[:, 0]

    cols_to_show = [key_col, "ΔPlaycount", "ΔListeners"]
    if "Artista" in merged.columns:
        cols_to_show.insert(1, "Artista")

    st.subheader(f"📊 Variação semanal ({week1} → {week2}) - {region}")
    st.dataframe(merged[cols_to_show])

# ========================
# Tendência semanal
# ========================
def show_weekly_trend(region: str = "Brasil", top_n: int = 5, analysis_type: str = "Top Músicas", base_dir: str = "data"):
    dfs = load_weekly_snapshots(region, base_dir)
    if len(dfs) < 2:
        st.info("Ainda não há dados suficientes para exibir tendências semanais.")
        return

    records = []
    for week, df in dfs:
        df = df.loc[:, ~df.columns.duplicated()]
        for col in ["Música", "Artista", "Gênero musical da música", "Playcount", "Listeners"]:
            if col not in df.columns:
                df[col] = "" if col in ["Música", "Artista", "Gênero musical da música"] else 0
        for _, row in df.iterrows():
            playcount = int(row["Playcount"]) if pd.notnull(row["Playcount"]) else 0
            listeners = int(row["Listeners"]) if pd.notnull(row["Listeners"]) else 0
            key_val = row.get("Música") or row.get("Artista") or row.get("Gênero musical da música")
            records.append({
                "Semana": week,
                "Chave": key_val,
                "Playcount": playcount,
                "Listeners": listeners,
            })

    df_all = pd.DataFrame(records)
    latest_week = df_all["Semana"].max()
    top_items = (
        df_all[df_all["Semana"] == latest_week]
        .nlargest(top_n, "Playcount")["Chave"]
        .tolist()
    )
    df_filtered = df_all[df_all["Chave"].isin(top_items)]

    st.subheader(f"🎶 Tendência Semanal Top {top_n} - {region}")
    chart = (
        alt.Chart(df_filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("Semana:O", title="Semana ISO"),
            y=alt.Y("Playcount:Q", title="Reproduções"),
            color=alt.Color("Chave:N", legend=alt.Legend(title="Item")),
            tooltip=["Chave", "Playcount", "Semana"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

# ========================
# Gerenciamento diário de dados
# ========================
def manage_weekly_data(base_dir: str = "data"):
    """Garante snapshots do Brasil e Mundial e limpa dados desnecessários"""
    start_time = time.time()
    regions_to_keep = ["brasil", "global"]
    data_path = Path(base_dir)
    if not data_path.exists():
        data_path.mkdir(parents=True, exist_ok=True)

    for folder in data_path.iterdir():
        if folder.is_dir() and folder.name not in regions_to_keep:
            for file in folder.glob("*.json"):
                file.unlink()
            try:
                folder.rmdir()
            except OSError:
                pass
            st.toast(f"🧹 Limpando dados antigos: {folder.name}", icon="🗑️")

    for region in ["Brasil", "Global"]:
        region_dir = data_path / region.lower().replace(" ", "_")
        region_dir.mkdir(parents=True, exist_ok=True)
        today = datetime.date.today()
        year, week, _ = today.isocalendar()
        file_path = region_dir / f"{year}-W{week}.json"
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            st.toast(f"💾 Snapshot inicial criado para {region}", icon="📦")

    elapsed = time.time() - start_time
    st.toast(f"✅ Verificação concluída em {elapsed:.2f}s", icon="✨")
