import streamlit as st
import pandas as pd
import altair as alt
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

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

def render_comparison(df1: pd.DataFrame, df2: pd.DataFrame, label1="Primeiro país", label2="Segundo país / Mundial", pastel_colors=None):
    """Renderiza a comparação de top músicas entre dois países ou mundial."""
    st.subheader("Comparação de Top Músicas")
    col1, col2 = st.columns(2)

    common_songs = set(df1["Música"]).intersection(df2["Música"])

    if pastel_colors is None:
        pastel_colors = [
            "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B9F2F0", "#FFE599"
        ]

    color_map = {song: pastel_colors[i % len(pastel_colors)] for i, song in enumerate(common_songs)}

    def assign_color(song):
        return color_map.get(song, "#E8E8E8")  # cinza pastel para exclusivas

    df1["Cor"] = df1["Música"].apply(assign_color)
    df2["Cor"] = df2["Música"].apply(assign_color)

    def make_chart(df, y_col="Listeners"):
        if y_col in df.columns:
            return (
                alt.Chart(df)
                .mark_bar(stroke="#FFFFFF", strokeWidth=0.5)
                .encode(
                    x=alt.X("Música", sort="-y", title="Música"),
                    y=alt.Y(y_col, title=y_col),
                    color=alt.Color("Cor:N", scale=None, legend=None),
                    tooltip=["Música", "Artista", "Listeners", "Playcount"]
                )
                .properties(height=400)
            )
        return None

    with col1:
        st.markdown(f"**{label1}**")
        show_aggrid(df1)
        chart1 = make_chart(df1)
        if chart1:
            st.altair_chart(chart1, use_container_width=True)

    with col2:
        st.markdown(f"**{label2}**")
        show_aggrid(df2)
        chart2 = make_chart(df2)
        if chart2:
            st.altair_chart(chart2, use_container_width=True)

    if len(common_songs) > 0:
        st.markdown("---")
        st.markdown(
            f"🎵 **Músicas em comum entre {label1} e {label2}:** " +
            ", ".join(sorted(common_songs))
        )
