import streamlit as st

# Real entrypoint for the Streamlit multi-page app.
# Uses pages implemented in `src/streamlit_app/pages/*`.
from .config import setup_page

# Ensure assets load relative to this module
from pathlib import Path

setup_page()

st.title("Prédiction des pannes Komax")
st.write("Bienvenue dans l'application de maintenance prédictive")

assets_dir = Path(__file__).resolve().parent / "assets"
st.image(str(assets_dir / "logo.png"), width=200)

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choisir une page",
    ["Accueil", "EDA", "Prediction", "Aboout"],
)

if page == "Accueil":
    st.write("Projet Machine Learning pour prédire les pannes")

elif page == "EDA":
    from .pages import EDA  # noqa: F401

elif page == "Prediction":
    from .pages import predict  # noqa: F401

elif page == "About":
    from .pages import about  # noqa: F401

