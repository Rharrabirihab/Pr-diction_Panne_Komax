import streamlit as st

# Real entrypoint for the Streamlit multi-page app.
# Uses pages implemented in `src/streamlit_app/pages/*`.
from .config import setup_page

# Ensure assets load relative to this module
from pathlib import Path

def main() -> None:
    setup_page()

    st.title("Prédiction des pannes Komax")
    st.write("Bienvenue dans l'application de maintenance prédictive")

    assets_dir = Path(__file__).resolve().parent / "assets"
    st.image(str(assets_dir / "predictkomax.jpg"), width=200)

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choisir une page",
        ["Accueil", "Se connecter", "S'inscrire", "EDA", "Prediction", "About"],
    )


    if page == "Accueil":
        st.write("Projet Machine Learning pour prédire les pannes")



    elif page == "Se connecter":
        from .pages import Se_connecter  # noqa: F401

    elif page == "S'inscrire":
        from .pages import S_inscrire  # noqa: F401

    elif page == "EDA":
        from .pages import EDA  # noqa: F401


    elif page == "Prediction":
        from .pages import predict  # noqa: F401

    elif page == "About":
        from .pages import about  # noqa: F401


if __name__ == "__main__":
    main()


