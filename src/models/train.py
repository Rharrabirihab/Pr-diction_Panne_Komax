from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score
import joblib
import numpy as np
import pandas as pd

def train_model(X, y):
    # Split pour validation interne
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    # CV pour estimation robuste (5-fold stratified)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='f1')
    print(f"CV F1 scores: {cv_scores}")
    print(f"Mean CV F1: {np.mean(cv_scores):.3f} (+/- {np.std(cv_scores)*2:.3f})")
    
    # Fit final sur full data
    model.fit(X, y)
    
    # Quick eval on val
    val_pred = model.predict(X_val)
    print(f"Validation F1: {f1_score(y_val, val_pred):.3f}")
    
    return model

def save_model(model, path="model.pkl"):
    joblib.dump(model, path)
    print(f"Modèle sauvé: {path}")


if __name__ == "__main__":
    # Point d’entrée pour entraîner un modèle directement depuis le repo.
    # Hypothèse: dataset final contient une colonne cible nommée 'failure'.
    import os

    default_train_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "processed",
        "trainFinal.csv",
    )

    train_path = default_train_path
    if not os.path.exists(train_path):
        # fallback: depuis la racine du repo
        train_path = os.path.join("data", "processed", "trainFinal.csv")

    df = pd.read_csv(train_path)

    # Target name: use the first column that matches common conventions.
    target_candidates = ["failure", "Failure", "panne", "Panne", "target", "Target", "label", "Label"]
    target_col = next((c for c in target_candidates if c in df.columns), None)

    # If not found, fall back to an existing label column if present in this dataset.
    if target_col is None:
        # In your processed CSVs, the target is often one of these.
        for c in df.columns:
            if c.lower() in {"type of failure_label".lower(), "type of failure", "type_of_failure"}:
                target_col = c
                break

    if target_col is None:
        for c in df.columns:
            if "failure" in c.lower() and c.lower().endswith("_label"):
                target_col = c
                break


    if target_col is None:
        raise ValueError(
            "Colonne cible introuvable. Colonnes disponibles: "
            + ", ".join(df.columns)
        )

    X = df.drop(target_col, axis=1).values
    y = df[target_col].values

    # Ensure target is categorical for classification.
    # In this project, *_label columns are often encoded as floats (z-score or similar).
    # RandomForestClassifier needs discrete class labels.
    if y.dtype.kind in {"f", "c"}:
        y = pd.Series(y).astype(float)

    # Coerce to discrete class ids based on sorted unique values.
    # This preserves all classes without quantization.
    uniq = np.unique(y[~pd.isna(y)])
    mapping = {val: idx for idx, val in enumerate(sorted(uniq))}
    y = np.array([mapping[val] for val in y], dtype=int)


    print(f"Using target_col={target_col}")
    print(f"X shape: {X.shape}, y shape: {np.asarray(y).shape}, y dtype: {np.asarray(y).dtype}")
    model = train_model(X, y)

    # Sauvegarder sous le nom attendu par l’app Streamlit
    save_model(model, path="model.pkl")
    print("DONE TRAIN")


