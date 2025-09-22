import streamlit as st
from src.utils import get_api_key, tracks_to_dataframe
from src.api import fetch_geo_toptracks, fetch_global_toptracks
from src.render import render_comparison
from src.styles import apply_styles

def main():
    st.set_page_config(page_title="Top Músicas Comparação", layout="wide")
    apply_styles()
    st.title("Comparação de Top Músicas por País")

    try:
        api_key = get_api_key()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    countries = ["Brazil", "United States", "United Kingdom", "Germany", "France", "Japan"]

    country1 = st.selectbox("Escolha o primeiro país:", countries)
    country2 = st.selectbox("Escolha o segundo país ou Mundial:", countries + ["Mundial"])

    limit = st.slider("Quantidade (limit)", min_value=5, max_value=50, value=10, step=5)

    if st.button("Atualizar (limpar cache)"):
        fetch_geo_toptracks.clear()
        fetch_global_toptracks.clear()
        st.success("Cache limpo! Atualize a página para buscar novamente.")


    with st.spinner("Buscando dados do Last.fm..."):
        try:
            tracks1 = fetch_geo_toptracks(country=country1, limit=limit, api_key=api_key)
            if country2 == "Mundial":
                tracks2 = fetch_global_toptracks(limit=limit, api_key=api_key)
            else:
                tracks2 = fetch_geo_toptracks(country=country2, limit=limit, api_key=api_key)

            df1 = tracks_to_dataframe(tracks1)
            df2 = tracks_to_dataframe(tracks2)

            render_comparison(df1, df2, label1=country1, label2=country2)

        except Exception as e:
            st.error(f"Ocorreu um erro ao buscar dados: {e}")

if __name__ == "__main__":
    main()
