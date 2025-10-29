import streamlit as st
import pandas as pd
from src.utils import get_api_key, tracks_to_dataframe, save_weekly_snapshot, compare_weeks, show_weekly_trend
from src.api import fetch_geo_toptracks, fetch_global_toptracks
from src.render import render_comparison
from src.styles import apply_styles
from src.ml_analysis import clustering_analysis, prediction_analysis
from vega_datasets import data
import altair as alt
from src.constants import COUNTRY_MAP, COUNTRY_TO_ID, PASTEL_COLORS_50


# =======================
# Lista de países ordenada
# =======================
countries_pt = sorted(list(COUNTRY_MAP.keys()))
if "Brasil" in countries_pt:
    countries_pt.remove("Brasil")
countries_pt = ["Brasil"] + countries_pt

# =======================
# Função de mapa
# =======================
def show_country_map(country1: str, country2: str = None):
    highlight_ids = [COUNTRY_TO_ID.get(c) for c in [country1, country2] if c in COUNTRY_TO_ID]
    if not highlight_ids:
        st.warning("Nenhum país válido para destacar no mapa.")
        return

    world = alt.topo_feature(data.world_110m.url, "countries")
    df = pd.DataFrame({"id": highlight_ids, "highlight": [True]*len(highlight_ids)})

    chart = alt.Chart(world).mark_geoshape(
        stroke='black',
        strokeWidth=0.5
    ).encode(
        color=alt.condition(
            alt.FieldOneOfPredicate(field='id', oneOf=highlight_ids),
            alt.value('fuchsia'),
            alt.value('lightgray')
        )
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df, 'id', ['highlight'])
    ).properties(
        width=700,
        height=400
    ).project('equirectangular')

    st.altair_chart(chart, use_container_width=True)

# =======================
# Função principal
# =======================
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

    with tabs[0]:
        st.header("Análise Atual - Dados do Momento")
        st.markdown("Visualize as músicas mais ouvidas em diferentes países ou analise um país isoladamente.")

        country1 = st.selectbox("Escolha o primeiro país:", countries_pt, key="country1")
        remaining_countries = ["Nenhum (analisar apenas um país)"] + [c for c in countries_pt if c != country1] + ["Mundial"]
        country2 = st.selectbox("Escolha o segundo país (ou 'Nenhum'):", remaining_countries, key="country2")
        limit = st.slider("Quantidade de músicas", min_value=5, max_value=50, value=10, step=5)

        with st.spinner("Buscando dados do Last.fm..."):
            try:
                df1 = tracks_to_dataframe(fetch_geo_toptracks(COUNTRY_MAP[country1], limit, api_key))
                save_weekly_snapshot(df1, COUNTRY_MAP[country1])

                if country2 == "Nenhum (analisar apenas um país)":
                    # Exibe o mapa primeiro
                    show_country_map(country1)
                    st.subheader(f"Top {limit} músicas em {country1}")
                    st.dataframe(df1.drop(columns=["Cor"], errors="ignore"))

                elif country2 == "Mundial":
                    df2 = tracks_to_dataframe(fetch_global_toptracks(limit, api_key))
                    save_weekly_snapshot(df2, "Global")
                    show_country_map(country1)
                    render_comparison(df1, df2, label1=country1, label2="Mundial", pastel_colors=PASTEL_COLORS_50)

                else:
                    df2 = tracks_to_dataframe(fetch_geo_toptracks(COUNTRY_MAP[country2], limit, api_key))
                    save_weekly_snapshot(df2, COUNTRY_MAP[country2])
                    # Mapa acima da comparação
                    show_country_map(country1, country2)
                    render_comparison(df1, df2, label1=country1, label2=country2, pastel_colors=PASTEL_COLORS_50)

            except Exception as e:
                st.error(f"Ocorreu um erro ao buscar dados: {e}")
    

    with tabs[1]:
        st.header("Análise Semanal")
        selected_country = st.selectbox("Escolha o país para análise:", countries_pt)
        compare_weeks(COUNTRY_MAP[selected_country])
        show_weekly_trend(COUNTRY_MAP[selected_country], top_n=5)

    with tabs[2]:
        st.header("Descubra Padrões e Tendências")
        st.markdown("---")
        st.markdown("""
            <div style="background-color: #e9f5ff; padding: 1.2em; border-radius: 10px; border-left: 6px solid #1f77b4;">
                <h4 style="color: #1f77b4;">💡 Entenda o que você está vendo</h4>
                <p>O painel identifica automaticamente <b>padrões de popularidade</b> e <b>tendências de crescimento</b>.</p>
            </div>
        """, unsafe_allow_html=True)

        selected_country_ml = st.selectbox("Escolha o país:", countries_pt)
        clustering_analysis(COUNTRY_MAP[selected_country_ml])
        prediction_analysis(COUNTRY_MAP[selected_country_ml])

if __name__ == "__main__":
    main()
