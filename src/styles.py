import streamlit as st

# 🎨 Paleta de cores por gênero musical
GENRE_COLOR_MAP = {
    "Pop": "#ff4cff",       # rosa vibrante
    "Rock": "#1f77b4",      # azul forte
    "Jazz": "#ff7f0e",      # laranja brilhante
    "Clássica": "#8c564b",  # marrom/terra
    # Pode adicionar mais gêneros conforme necessário
}

def apply_styles():
    """
    Aplica estilos customizados à interface Streamlit.
    """
    st.markdown(
        """
        <style>
        /* Fundo geral */
        .stApp {
            background-color: #f8f9fa;
            color: #212529;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Títulos */
        h1, h2, h3 {
            color: #2c3e50;
        }

        /* Botões */
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

        /* DataFrames */
        .stDataFrame {
            border: 1px solid #dee2e6;
            border-radius: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
