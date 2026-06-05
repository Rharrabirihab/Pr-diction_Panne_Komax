# TODO: Correction Erreurs Code et Intégration Validation Croisée pour Prédiction Panne Komax

## Étapes
- [x] 0. Explorer le repo
- [x] 1. Identifier la page prédiction
- [x] 2. Dockeriser le repo (Dockerfile + .dockerignore)
- [x] 3. Aligner l’app Streamlit pour utiliser `src/streamlit_app/pages/predict.py` (model.pkl + UI dynamique)
- [x] 4. Sécuriser le chargement du modèle via `MODEL_PATH`
- [ ] 5. Valider : build/run Docker + ouvrir /Prediction

## Notes
- L’app `src/streamlit_app/app.py` actuelle charge `model_panne_komax.pkl` (UI fixe). 
- La page `src/streamlit_app/pages/predict.py` charge `model.pkl` et génère une UI dynamique à partir de `n_features_in_`.

