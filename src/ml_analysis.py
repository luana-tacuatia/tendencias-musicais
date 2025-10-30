import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import altair as alt
from src.utils import load_weekly_snapshots


# ========================
# Carregamento de dados
# ========================
def load_all_data(country: str) -> pd.DataFrame:
    dfs = load_weekly_snapshots(country)
    if not dfs:
        st.warning(f"Ainda não há dados semanais salvos para análise em {country}.")
        return pd.DataFrame()

    records = []
    for week, df in dfs:
        df["Semana"] = week
        records.append(df)

    df_all = pd.concat(records, ignore_index=True)
    df_all = df_all.loc[:, ~df_all.columns.duplicated()]
    return df_all


# ========================
# Análise de Clustering
# ========================
def clustering_analysis(country: str, analysis_type: str):
    df = load_all_data(country)
    if df.empty:
        return

    if "Playcount" not in df.columns or "Listeners" not in df.columns:
        st.warning("Colunas 'Playcount' e 'Listeners' ausentes nos dados.")
        return

    # Define a chave conforme o tipo de análise
    if analysis_type == "Top Músicas":
        label_col = "Música"
    elif analysis_type == "Top Artistas":
        label_col = "Artista"
    else:
        label_col = "Gênero musical da música" if "Gênero musical da música" in df.columns else "Gênero"

    df = df[[label_col, "Playcount", "Listeners", "Semana"]].dropna()
    features = df[["Playcount", "Listeners"]].fillna(0)
    scaled = StandardScaler().fit_transform(features)

    # KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
    df["Cluster"] = kmeans.fit_predict(scaled)

    st.subheader(f"🎧 Agrupamento ({analysis_type}) - {country}")
    st.caption("Os pontos mostram agrupamentos de popularidade com base em ouvintes e reproduções.")

    chart = (
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(
            x=alt.X("Playcount:Q", title="Reproduções (Playcount)"),
            y=alt.Y("Listeners:Q", title="Ouvintes (Listeners)"),
            color=alt.Color("Cluster:N", legend=alt.Legend(title="Cluster")),
            tooltip=[label_col, "Cluster", "Playcount", "Listeners"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True, key=f"cluster_chart_{country}_{analysis_type}")


# ========================
# Análise Preditiva
# ========================
def prediction_analysis(country: str, analysis_type: str):
    df = load_all_data(country)
    if df.empty or len(df["Semana"].unique()) < 3:
        st.info(f"É necessário ter pelo menos 3 semanas de dados para previsão em {country}.")
        return

    # Define o alvo conforme o tipo
    if analysis_type == "Top Músicas":
        label_col = "Música"
    elif analysis_type == "Top Artistas":
        label_col = "Artista"
    else:
        label_col = "Gênero musical da música" if "Gênero musical da música" in df.columns else "Gênero"

    if "Playcount" not in df.columns:
        st.warning("Coluna 'Playcount' ausente nos dados.")
        return

    df["ΔPlaycount"] = df.groupby(label_col)["Playcount"].diff()
    df = df.dropna(subset=["ΔPlaycount"])

    X = df[["Semana"]]
    y = df["ΔPlaycount"]

    model = LinearRegression()
    model.fit(X, y)

    next_week = df["Semana"].max() + 1
    predicted = model.predict([[next_week]])[0]

    st.subheader(f"🔮 Previsão de Crescimento ({analysis_type}) - {country}")
    st.metric("Crescimento médio estimado (Playcount)", f"{predicted:.0f} reproduções")

    # Visualização da tendência real
    trend_chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Semana:O", title="Semana ISO"),
            y=alt.Y("ΔPlaycount:Q", title="Variação de Reproduções"),
            color=alt.Color(f"{label_col}:N", legend=None),
            tooltip=[label_col, "Semana", "ΔPlaycount"]
        )
        .interactive()
        .properties(height=400)
    )
    st.altair_chart(trend_chart, use_container_width=True, key=f"prediction_chart_{country}_{analysis_type}")
