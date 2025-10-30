import streamlit as st
import pandas as pd
import altair as alt
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

def show_aggrid(df: pd.DataFrame):
    """Exibe DataFrame no AgGrid, sem duplicidade de colunas."""
    df_display = df.copy()
    gb = GridOptionsBuilder.from_dataframe(df_display)
    for col in df_display.columns:
        gb.configure_column(col, header_name=col)
    grid_options = gb.build()
    AgGrid(df_display, gridOptions=grid_options, enable_enterprise_modules=False, fit_columns_on_grid_load=True)

def make_bar_chart(df: pd.DataFrame, label_col: str, title: str, pastel_colors):
    """Cria gráfico de barras Altair a partir de df com colunas Label, Ouvintes, Reproduções."""
    if df.empty:
        st.warning("⚠️ Dados insuficientes para gerar o gráfico.")
        return

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(label_col + ":N", sort="-y", title=label_col),
            y=alt.Y("Reproduções:Q", title="Reproduções"),
            color=alt.Color(label_col + ":N", scale=alt.Scale(range=pastel_colors), legend=None),
            tooltip=[label_col, "Ouvintes", "Reproduções"]
        )
        .properties(height=400, width=700, title=title)
    )
    return chart

def render_single_country(df: pd.DataFrame, label: str, analysis_type: str, pastel_colors=None):
    """Renderiza tabela e gráfico para 1 país."""
    if df.empty:
        st.warning(f"Não há dados disponíveis para {label}.")
        return

    if pastel_colors is None:
        pastel_colors = [
            "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B9F2F0", "#FFE599"
        ]

    # Define coluna alvo e nome correto
    if analysis_type == "Top Músicas":
        label_col = "Música"
        df_temp = df[["Música", "Ouvintes", "Reproduções"]].copy()
    elif analysis_type == "Top Artistas":
        label_col = "Artista"
        df_temp = df[["Artista", "Ouvintes", "Reproduções"]].copy()
    elif analysis_type == "Top Gêneros Musicais":
        label_col = "Gênero musical"
        df_temp = df[["Gênero musical da música", "Ouvintes", "Reproduções"]].copy()
        df_temp = df_temp.rename(columns={"Gênero musical da música": "Gênero musical"})

    # Exibe tabela
    st.subheader(f"Tabela detalhada de {analysis_type.lower()} em {label}")
    show_aggrid(df_temp)

    # Exibe gráfico
    chart = make_bar_chart(df_temp, label_col, f"Top {len(df_temp)} {analysis_type.lower()} em {label}", pastel_colors)
    if chart:
        st.altair_chart(chart, use_container_width=True)

def render_comparison(df1: pd.DataFrame, df2: pd.DataFrame, label1: str, label2: str, analysis_type: str, pastel_colors=None):
    """Renderiza comparação entre 2 países."""
    if pastel_colors is None:
        pastel_colors = [
            "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B9F2F0", "#FFE599"
        ]

    # Ajusta coluna alvo e cria df temporário
    def prepare_df(df):
        if analysis_type == "Top Músicas":
            return df[["Música", "Ouvintes", "Reproduções"]].rename(columns={"Música": "Label"})
        elif analysis_type == "Top Artistas":
            return df[["Artista", "Ouvintes", "Reproduções"]].rename(columns={"Artista": "Label"})
        elif analysis_type == "Top Gêneros Musicais":
            return df[["Gênero musical da música", "Ouvintes", "Reproduções"]].rename(columns={"Gênero musical da música": "Label"})

    df1_temp = prepare_df(df1)
    df2_temp = prepare_df(df2)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{analysis_type} - {label1}")
        show_aggrid(df1_temp)
        chart1 = make_bar_chart(df1_temp, "Label", f"Top {len(df1_temp)} {analysis_type.lower()} - {label1}", pastel_colors)
        if chart1:
            st.altair_chart(chart1, use_container_width=True)

    with col2:
        st.subheader(f"{analysis_type} - {label2}")
        show_aggrid(df2_temp)
        chart2 = make_bar_chart(df2_temp, "Label", f"Top {len(df2_temp)} {analysis_type.lower()} - {label2}", pastel_colors)
        if chart2:
            st.altair_chart(chart2, use_container_width=True)

# ==========================================================
# Funções exclusivas para a aba "Análise Semanal"
# ==========================================================

def render_weekly_single(df: pd.DataFrame, label: str, analysis_type: str, pastel_colors=None):
    """Renderiza visualização para análise semanal de um país ou global."""
    if pastel_colors is None:
        from src.constants import PASTEL_COLORS_50
        pastel_colors = PASTEL_COLORS_50

    if df.empty:
        st.warning(f"Não há dados disponíveis para {label}.")
        return

    # Define coluna de exibição
    if analysis_type == "Top Músicas" and "Música" in df.columns:
        df["Label"] = df["Música"]
    elif analysis_type == "Top Artistas" and "Artista" in df.columns:
        df["Label"] = df["Artista"]
    elif analysis_type == "Top Gêneros Musicais" and "Gênero musical da música" in df.columns:
        df["Label"] = df["Gênero musical da música"]

    st.subheader(f"{analysis_type} - {label}")
    st.dataframe(df, use_container_width=True)

    import altair as alt
    chart = (
        alt.Chart(df)
        .mark_bar(size=18)
        .encode(
            x=alt.X("Label:N", sort='-y', title=None),
            y=alt.Y("Reproduções:Q", title="Reproduções"),
            color=alt.value(pastel_colors[0]),
            tooltip=["Label", "Ouvintes", "Reproduções"]
        )
        .properties(width="container", height=350)
    )
    st.altair_chart(chart, use_container_width=True)


def render_weekly_comparison(df1: pd.DataFrame, df2: pd.DataFrame, label1: str, label2: str, analysis_type: str, pastel_colors=None):
    """Renderiza comparação semanal entre dois conjuntos (ex: Brasil x Mundial)."""
    if pastel_colors is None:
        from src.constants import PASTEL_COLORS_50
        pastel_colors = PASTEL_COLORS_50

    if df1.empty or df2.empty:
        st.warning("Não há dados suficientes para comparação.")
        return

    st.subheader(f"Comparação Semanal: {label1} x {label2} — {analysis_type}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {label1}")
        st.dataframe(df1, use_container_width=True)

        import altair as alt
        chart1 = (
            alt.Chart(df1)
            .mark_bar(size=18)
            .encode(
                x=alt.X("Label:N", sort='-y', title=None),
                y=alt.Y("Reproduções:Q", title="Reproduções"),
                color=alt.value(pastel_colors[0]),
                tooltip=["Label", "Ouvintes", "Reproduções"]
            )
            .properties(width="container", height=350)
        )
        st.altair_chart(chart1, use_container_width=True)

    with col2:
        st.markdown(f"### {label2}")
        st.dataframe(df2, use_container_width=True)

        import altair as alt
        chart2 = (
            alt.Chart(df2)
            .mark_bar(size=18)
            .encode(
                x=alt.X("Label:N", sort='-y', title=None),
                y=alt.Y("Reproduções:Q", title="Reproduções"),
                color=alt.value(pastel_colors[1]),
                tooltip=["Label", "Ouvintes", "Reproduções"]
            )
            .properties(width="container", height=350)
        )
        st.altair_chart(chart2, use_container_width=True)
