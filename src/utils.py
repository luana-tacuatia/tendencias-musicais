import os
import datetime
from pathlib import Path
from typing import Any, Optional
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import altair as alt


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
    """
    Salva os dados semanais em JSON, criando arquivos separados por semana ISO.
    - region: nome do país ou 'Global'
    - base_dir: diretório raiz dos dados
    """
    output_dir = Path(base_dir) / region.lower().replace(" ", "_")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.date.today()
    year, week, weekday = today.isocalendar()
    file_path = output_dir / f"{year}-W{week}.json"

    # Salva apenas na quarta-feira e se o arquivo ainda não existir
    if weekday == 2 and not file_path.exists():
        df.to_json(file_path, orient="records", force_ascii=False, indent=2)
        st.toast(f"📁 Snapshot semanal salvo ({region}): {file_path}", icon="💾")
    elif file_path.exists():
        st.info(f"📁 Snapshot já existe para {region}, semana {week}: {file_path}")


# ========================
# Carregar snapshots semanais
# ========================
def load_weekly_snapshots(region: str = "Brasil", base_dir: str = "data"):
    folder = Path(base_dir) / region.lower().replace(" ", "_")
    files = sorted(folder.glob("*.json"))
    dfs = []
    for f in files:
        # extrai a semana do nome do arquivo
        week = int(f.stem.split("-W")[1])
        dfs.append((week, pd.read_json(f)))
    return dfs


# ========================
# Comparação de semanas
# ========================
def compare_weeks(region: str = "Brasil", base_dir: str = "data"):
    dfs = load_weekly_snapshots(region, base_dir)
    if len(dfs) < 2:
        st.info("Ainda não há dados suficientes para comparação semanal.")
        return

    week1, df1 = dfs[-2]
    week2, df2 = dfs[-1]

    cols_needed = ["Música", "Artista", "Playcount", "Listeners"]
    df1_subset = df1[cols_needed].copy()
    df2_subset = df2[cols_needed].copy()

    df1_subset = df1_subset.loc[:, ~df1_subset.columns.duplicated()]
    df2_subset = df2_subset.loc[:, ~df2_subset.columns.duplicated()]

    for col in ["Música", "Artista", "Playcount", "Listeners"]:
        if col not in df1_subset.columns:
            df1_subset[col] = "" if col in ["Música", "Artista"] else 0
        if col not in df2_subset.columns:
            df2_subset[col] = "" if col in ["Música", "Artista"] else 0

    merged = df1_subset.merge(
        df2_subset,
        on="Música",
        suffixes=(f"_sem{week1}", f"_sem{week2}")
    )

    merged["ΔPlaycount"] = merged.filter(like=f"Playcount_sem{week2}").iloc[:, 0] - \
                           merged.filter(like=f"Playcount_sem{week1}").iloc[:, 0]

    merged["ΔListeners"] = merged.filter(like=f"Listeners_sem{week2}").iloc[:, 0] - \
                            merged.filter(like=f"Listeners_sem{week1}").iloc[:, 0]

    if "Artista" not in merged.columns:
        merged["Artista"] = ""

    cols_to_show = [c for c in ["Música", "Artista", "ΔPlaycount", "ΔListeners"] if c in merged.columns]
    st.subheader(f"📊 Variação semanal ({week1} → {week2}) - {region}")
    st.dataframe(merged[cols_to_show])


# ========================
# Tendência semanal
# ========================
def show_weekly_trend(region: str = "Brasil", top_n: int = 5, base_dir: str = "data"):
    dfs = load_weekly_snapshots(region, base_dir)
    if len(dfs) < 2:
        st.info("Ainda não há dados suficientes para exibir tendências semanais.")
        return

    records = []
    for week, df in dfs:
        df = df.loc[:, ~df.columns.duplicated()]
        for col in ["Música", "Artista", "Playcount", "Listeners"]:
            if col not in df.columns:
                df[col] = "" if col in ["Música", "Artista"] else 0
        for _, row in df.iterrows():
            playcount = int(row["Playcount"]) if pd.notnull(row["Playcount"]) else 0
            listeners = int(row["Listeners"]) if pd.notnull(row["Listeners"]) else 0
            records.append({
                "Semana": week,
                "Música": row["Música"],
                "Artista": row["Artista"],
                "Playcount": playcount,
                "Listeners": listeners,
            })

    df_all = pd.DataFrame(records)
    latest_week = df_all["Semana"].max()
    top_musics = (
        df_all[df_all["Semana"] == latest_week]
        .nlargest(top_n, "Playcount")["Música"]
        .tolist()
    )
    df_filtered = df_all[df_all["Música"].isin(top_musics)]
    if "Artista" not in df_filtered.columns:
        df_filtered["Artista"] = ""

    st.subheader(f"🎶 Tendência Semanal das Top {top_n} músicas ({region})")
    chart = (
        alt.Chart(df_filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("Semana:O", title="Semana ISO"),
            y=alt.Y("Playcount:Q", title="Reproduções"),
            color=alt.Color("Música:N", legend=alt.Legend(title="Música")),
            tooltip=["Música", "Artista", "Playcount", "Semana"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)
