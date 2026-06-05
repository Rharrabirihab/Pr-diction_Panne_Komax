from sklearn.metrics import accuracy_score, f1_score, classification_report, roc_auc_score
from sklearn.model_selection import cross_val_score, StratifiedKFold
import numpy as np

def evaluate_model(model, X_test, y_test):
    """Éval sur test set"""
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    print("Classification Report:\n", classification_report(y_test, y_pred))
    try:
        auc = roc_auc_score(y_test, model.predict_proba(X_test), multi_class='ovr')
        print(f"ROC AUC: {auc:.3f}")
    except:
        pass
    return {'accuracy': acc, 'f1': f1}

def cv_evaluate(model, X, y, cv_folds=5):
    """CV sur données fournies"""
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
    print(f"CV F1: {np.mean(cv_scores):.3f} (+/- {np.std(cv_scores)*2:.3f})")
    return np.mean(cv_scores)
