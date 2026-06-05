import streamlit as st
from config import setup_page

setup_page

st.title("Prédiction des pannes Komax")
st.write("Bienvenue dans l'applicaation de maintenance prédictive")
st.image("assets/logo.png", width=200)
st.sidebar.title("Navigation")

page=st.sidebar.selectbox("Choisir une page", ["Accueil", "EDA", "Prediction", "Aboout"])
if page == "Accueil":
    st.write("Projet Machine Learning pour prédir les pannes")

elif page == "EDA":
    import pages.EDA

elif page == "Prediction":
    import pages.predict

elif page == "About":
    import pages.about


