import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import altair as alt

display_cols = [
    "Posição",
    "Música",
    "Artista",
    "Gênero musical da música",
    "Gênero musical do artista",
    "Listeners",
    "Playcount"
]

def add_line_breaks(header: str, max_len: int = 15) -> str:
    if len(header) <= max_len:
        return header
    words = header.split(" ")
    return "\n".join(words)

def show_aggrid(df: pd.DataFrame):
    df_display = df.reset_index(drop=True)
    cols = [c for c in display_cols if c in df_display.columns]
    df_display = df_display[cols]

    gb = GridOptionsBuilder.from_dataframe(df_display)
    for col in df_display.columns:
        gb.configure_column(col, header_name=add_line_breaks(col))
    grid_options = gb.build()
    AgGrid(df_display, gridOptions=grid_options, enable_enterprise_modules=False, fit_columns_on_grid_load=True)

def show_bar_chart(df: pd.DataFrame, y_col="Listeners"):
    if y_col in df.columns:
        chart = alt.Chart(df).mark_bar(color="#1f77b4").encode(
            x="Música",
            y=y_col
        )
        st.altair_chart(chart, use_container_width=True)

def render_comparison(df1: pd.DataFrame, df2: pd.DataFrame, label1="Primeiro país", label2="Segundo país / Mundial"):
    st.subheader("Comparação de Top Músicas")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**{label1}**")
        show_aggrid(df1)
        show_bar_chart(df1)

    with col2:
        st.markdown(f"**{label2}**")
        show_aggrid(df2)
        show_bar_chart(df2)
