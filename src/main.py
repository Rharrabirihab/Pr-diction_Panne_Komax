import streamlit as st

# Legacy single-file Streamlit app.
# Kept for compatibility; it now delegates to the real multi-page app package.

from streamlit_app.config import setup_page


setup_page()

from pathlib import Path

st.title("Prédiction des pannes Komax")
st.write("Bienvenue dans l'application de maintenance prédictive")

assets_dir = Path(__file__).resolve().parent / "streamlit_app" / "assets"
st.image(str(assets_dir / "predictkomax.jpg"), width=200)

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choisir une page",
    ["Accueil", "Se connecter", "S'inscrire", "EDA", "Prediction", "About"],
)


if page == "Accueil":
    st.write("Projet Machine Learning pour prédire les pannes")

elif page == "EDA":
    from src.streamlit_app.pages import EDA  # noqa: F401

elif page == "Prediction":
    from src.streamlit_app.pages import predict  # noqa: F401

elif page == "About":
    from src.streamlit_app.pages import about  # noqa: F401

