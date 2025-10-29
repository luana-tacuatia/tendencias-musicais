import streamlit as st

GENRE_COLOR_MAP = {
    "Pop": "#ff4cff",
    "Rock": "#1f77b4",
    "Jazz": "#ff7f0e",
    "Clássica": "#8c564b",
}


def apply_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f8f9fa;
            color: #212529;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3 {
            color: #2c3e50;
        }

        div.stButton > button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
        }
        div.stButton > button:hover {
            background-color: #155d8b;
        }

        .stDataFrame {
            border: 1px solid #dee2e6;
            border-radius: 6px;
        }

        /* --- Ajuste do tamanho e estilo das abas --- */
        button[data-baseweb="tab"] > div {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #1f77b4 !important;
        }

        /* Aba selecionada */
        button[data-baseweb="tab"][aria-selected="true"] > div {
            color: #0d3b66 !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
