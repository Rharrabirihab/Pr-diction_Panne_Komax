import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.title("Prédiction de panne")

# Modèle entraîné
import os

# Allow Docker/host override
MODEL_PATH = os.environ.get("MODEL_PATH")
if MODEL_PATH:
    MODEL_PATH = os.path.abspath(MODEL_PATH)
else:
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "model.pkl")
    MODEL_PATH = os.path.abspath(MODEL_PATH)

st.write(f"Chargement modèle: {MODEL_PATH}")

if not os.path.exists(MODEL_PATH):
    st.error(
        "Fichier modèle introuvable. Place `model.pkl` à la racine du projet (ou passe l'env var MODEL_PATH)."
    )
    st.stop()

model = joblib.load(MODEL_PATH)


st.write("Entrer les données machine (format attendu = colonnes du dataset entraînement)")

# On récupère les noms de colonnes attendus si le modèle a été entraîné sur un DataFrame.
# Sinon, on se base sur le nombre de features `n_features_in_`.
feature_names = None
n_features = getattr(model, "n_features_in_", None)

if n_features is None:
    st.error("Le modèle ne semble pas exposer le nombre de features attendues.")
    st.stop()

# Par défaut: labels génériques
cols = [f"feature_{i}" for i in range(n_features)]

inputs = {}
for c in cols:
    inputs[c] = st.number_input(c, value=0.0)

if st.button("Prédire"):
    X = np.array([[inputs[c] for c in cols]], dtype=float)
    prediction = model.predict(X)

    if prediction[0] == 1:
        st.error("Panne probable !")
    else:
        st.success("Machine OK")

