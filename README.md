# Prédiction Panne Komax (Streamlit + Docker)

## Lancer en local
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501
```

## Lancer avec Docker
Pré-requis : avoir un modèle `model.pkl` (généré par `src/models/train.py`).

### Build
```bash
docker build -t komax-streamlit .
```

### Run
```bash
docker run --rm -p 8501:8501 \
  -e MODEL_PATH=/app/model.pkl \
  komax-streamlit
```

Puis ouvrir : http://localhost:8501

