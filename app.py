import streamlit as st
import pandas as pd
from src.utils import get_api_key, tracks_to_dataframe, save_weekly_snapshot, compare_weeks, show_weekly_trend
from src.api import fetch_geo_toptracks, fetch_global_toptracks
from src.render import render_comparison, render_single_country
from src.styles import apply_styles
from src.ml_analysis import clustering_analysis, prediction_analysis
from vega_datasets import data
import altair as alt
from src.constants import COUNTRY_MAP, COUNTRY_TO_ID, PASTEL_COLORS_50
from src.utils import manage_weekly_data

# Executa uma verificação automática diária de snapshots
manage_weekly_data()


countries_pt = sorted(list(COUNTRY_MAP.keys()))
if "Brasil" in countries_pt:
    countries_pt.remove("Brasil")
countries_pt = ["Brasil"] + countries_pt

def show_country_map(country1: str, country2: str = None):
    highlight_ids = [COUNTRY_TO_ID.get(c) for c in [country1, country2] if c in COUNTRY_TO_ID]
    if not highlight_ids:
        st.warning("Nenhum país válido para destacar no mapa.")
        return

    world = alt.topo_feature(data.world_110m.url, "countries")
    df = pd.DataFrame({"id": highlight_ids, "highlight": [True]*len(highlight_ids)})

    chart = alt.Chart(world).mark_geoshape(stroke='black', strokeWidth=0.5).encode(
        color=alt.condition(
            alt.FieldOneOfPredicate(field='id', oneOf=highlight_ids),
            alt.value('fuchsia'),
            alt.value('lightgray')
        )
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df, 'id', ['highlight'])
    ).properties(width=700, height=400).project('equirectangular')

    st.altair_chart(chart, use_container_width=True)

def main():
    st.set_page_config(page_title="Análise de Tendências Musicais", layout="wide")
    apply_styles()
    st.title("Análise de Tendências Musicais com Last.fm")

    try:
        api_key = get_api_key()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    tabs = st.tabs(["Análise Atual", "Análise Semanal", "Descubra Padrões e Tendências"])

    # ========================
    # Aba 1 - Análise do momento
    # ========================
    with tabs[0]:
        st.header("Análise Atual - Dados do Momento")
        st.markdown("Visualize as músicas mais ouvidas em diferentes países ou analise um país isoladamente.")

        country1 = st.selectbox("Escolha o primeiro país:", countries_pt, key="country1")
        remaining_countries = ["Nenhum (analisar apenas um país)"] + [c for c in countries_pt if c != country1] + ["Mundial"]
        country2 = st.selectbox("Escolha o segundo país (ou 'Nenhum'):", remaining_countries, key="country2")
        limit = st.slider("Quantidade de músicas / artistas / gêneros", min_value=5, max_value=50, value=10, step=5)
        analysis_type = st.radio("Escolha o tipo de análise:", ["Top Músicas", "Top Artistas", "Top Gêneros Musicais"])

        with st.spinner("Buscando dados do Last.fm..."):
            try:
                # ======== País 1 ========
                country_api_name1 = COUNTRY_MAP.get(country1, country1)
                df1 = tracks_to_dataframe(fetch_geo_toptracks(country_api_name1, limit, api_key))
                save_weekly_snapshot(df1, COUNTRY_MAP[country1])
                df1 = df1.rename(columns={"Playcount": "Reproduções", "Listeners": "Ouvintes"})
                df1 = df1.drop_duplicates()

                # Agrupamento conforme o tipo de análise
                if analysis_type == "Top Artistas":
                    df1 = (
                        df1.groupby("Artista", as_index=False)[["Reproduções", "Ouvintes"]]
                        .sum()
                        .sort_values("Reproduções", ascending=False)
                        .head(limit)
                    )
                elif analysis_type == "Top Gêneros Musicais":
                    col_genre = "Gênero musical da música"
                    if col_genre in df1.columns:
                        df1 = (
                            df1.groupby(col_genre, as_index=False)[["Reproduções", "Ouvintes"]]
                            .sum()
                            .sort_values("Reproduções", ascending=False)
                            .head(limit)
                        )
                    else:
                        st.warning("Dados de gênero musical indisponíveis para este país.")
                        return

                # ======== Apenas 1 país ========
                if country2 == "Nenhum (analisar apenas um país)":
                    show_country_map(country1)
                    render_single_country(df1, label=country1, analysis_type=analysis_type, pastel_colors=PASTEL_COLORS_50)

                # ======== País vs Mundial ========
                elif country2 == "Mundial":
                    df2 = tracks_to_dataframe(fetch_global_toptracks(limit, api_key))
                    save_weekly_snapshot(df2, "Global")
                    df2 = df2.rename(columns={"Playcount": "Reproduções", "Listeners": "Ouvintes"})
                    df2 = df2.drop_duplicates()

                    if analysis_type == "Top Artistas":
                        df2 = (
                            df2.groupby("Artista", as_index=False)[["Reproduções", "Ouvintes"]]
                            .sum()
                            .sort_values("Reproduções", ascending=False)
                            .head(limit)
                        )
                    elif analysis_type == "Top Gêneros Musicais":
                        col_genre = "Gênero musical da música"
                        if col_genre in df2.columns:
                            df2 = (
                                df2.groupby(col_genre, as_index=False)[["Reproduções", "Ouvintes"]]
                                .sum()
                                .sort_values("Reproduções", ascending=False)
                                .head(limit)
                            )

                    show_country_map(country1)
                    render_comparison(
                        df1, df2,
                        label1=country1,
                        label2="Mundial",
                        analysis_type=analysis_type,
                        pastel_colors=PASTEL_COLORS_50
                    )

                # ======== Dois países ========
                else:
                    df2 = tracks_to_dataframe(fetch_geo_toptracks(COUNTRY_MAP[country2], limit, api_key))
                    save_weekly_snapshot(df2, COUNTRY_MAP[country2])
                    df2 = df2.rename(columns={"Playcount": "Reproduções", "Listeners": "Ouvintes"})
                    df2 = df2.drop_duplicates()

                    if analysis_type == "Top Artistas":
                        df2 = (
                            df2.groupby("Artista", as_index=False)[["Reproduções", "Ouvintes"]]
                            .sum()
                            .sort_values("Reproduções", ascending=False)
                            .head(limit)
                        )
                    elif analysis_type == "Top Gêneros Musicais":
                        col_genre = "Gênero musical da música"
                        if col_genre in df2.columns:
                            df2 = (
                                df2.groupby(col_genre, as_index=False)[["Reproduções", "Ouvintes"]]
                                .sum()
                                .sort_values("Reproduções", ascending=False)
                                .head(limit)
                            )

                    show_country_map(country1, country2)
                    render_comparison(
                        df1, df2,
                        label1=country1,
                        label2=country2,
                        analysis_type=analysis_type,
                        pastel_colors=PASTEL_COLORS_50
                    )

            except Exception as e:
                st.error(f"Ocorreu um erro ao buscar dados: {e}")


    # ========================
    # Aba 2 - Análise Semanal
    # ========================
    with tabs[1]:
        st.header("📈 Análise Semanal de Tendências")

        analysis_type = st.selectbox(
            "Escolha o tipo de análise:",
            ["Top Músicas", "Top Artistas", "Top Gêneros Musicais"],
            key="analysis_type_weekly"
        )

        col1, col2 = st.columns(2)
        with col1:
            option = st.radio(
                "Escolha o tipo de comparação:",
                ["Brasil", "Mundial", "Brasil x Mundial"],
                key="region_selection_weekly"
            )

        top_n = st.slider(
            "Selecione o número de itens (Top N):",
            min_value=5, max_value=30, value=10, step=5,
            key="top_n_weekly"
        )

        # Lógica principal
        if option in ["Brasil", "Mundial"]:
            region = "Brasil" if option == "Brasil" else "Global"
            st.subheader(f"Análise Semanal - {region}")
            compare_weeks(region=region, analysis_type=analysis_type, top_n=top_n)
            show_weekly_trend(region=region, analysis_type=analysis_type, top_n=top_n)

        else:  # Brasil x Mundial
            st.subheader("Comparativo Semanal - Brasil x Mundial")
            col_b, col_m = st.columns(2)

            with col_b:
                st.markdown("#### Brasil")
                compare_weeks(region="Brasil", analysis_type=analysis_type, top_n=top_n)
                show_weekly_trend(region="Brasil", analysis_type=analysis_type, top_n=top_n)

            with col_m:
                st.markdown("#### Mundial")
                compare_weeks(region="Global", analysis_type=analysis_type, top_n=top_n)
                show_weekly_trend(region="Global", analysis_type=analysis_type, top_n=top_n)


    # ========================
    # Aba 3 - Análise com Machine Learning
    # ========================
    with tabs[2]:
        st.header("Análise com Aprendizado de Máquina")

        st.markdown("""
        Nesta aba, aplicamos técnicas de **aprendizado de máquina (do inglês _Machine Learning_; ML)** para identificar **tendências**, 
        **padrões de comportamento** e **agrupamentos** entre músicas, artistas e gêneros musicais.  
        O objetivo é explorar como os dados evoluem ao longo do tempo — tanto no **Brasil** quanto no **mundo** —
        e prever **tendências futuras de popularidade**.
        """)

        st.info("""
        **Como funciona:**  
        - **Agrupamento (_Clustering_):** Agrupa músicas/artistas/gêneros com características similares de ouvintes e reproduções.  
        - **Previsão:** Estima o crescimento médio nas próximas semanas com base no histórico de popularidade.  
        """)

        st.markdown("---")

        analysis_type = st.selectbox(
            "Escolha o tipo de análise:",
            ["Top Músicas", "Top Artistas", "Top Gêneros Musicais"],
            key="ml_analysis_type"
        )

        col1, col2 = st.columns(2)
        with col1:
            option = st.radio(
                "Escolha a origem dos dados:",
                ["Brasil", "Mundial", "Brasil x Mundial"],
                key="ml_region_option"
            )

        st.markdown("---")
        st.markdown("### Análise de Agrupamento (_Clustering_)")
        st.caption("Agrupamento baseado em ouvintes e reproduções — útil para identificar padrões de popularidade.")

        if option == "Brasil":
            clustering_analysis("Brasil", analysis_type)
        elif option == "Mundial":
            clustering_analysis("Global", analysis_type)
        else:
            col_b, col_m = st.columns(2)
            with col_b:
                st.markdown("#### Brasil")
                clustering_analysis("Brasil", analysis_type)
            with col_m:
                st.markdown("#### Mundial")
                clustering_analysis("Global", analysis_type)

        st.markdown("---")
        st.markdown("### Análise Preditiva (Tendências Futuras)")
        st.caption("Estima o crescimento médio semanal de reproduções para identificar tendências emergentes.")

        if option == "Brasil":
            prediction_analysis("Brasil", analysis_type)
        elif option == "Mundial":
            prediction_analysis("Global", analysis_type)
        else:
            col_b, col_m = st.columns(2)
            with col_b:
                st.markdown("#### 🇧🇷 Brasil")
                prediction_analysis("Brasil", analysis_type)
            with col_m:
                st.markdown("#### 🌐 Mundial")
                prediction_analysis("Global", analysis_type)



if __name__ == "__main__":
    main()
