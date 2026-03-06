"""
Entrenamiento del modelo Iris con guardado de artefacto.
Evolución de clase-1: ahora el modelo se guarda con joblib
para poder ser servido por la API (FastAPI).
"""

import os
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score


def train_model(model_path="model.joblib"):
    """
    Entrena un RandomForest con el dataset Iris y guarda el modelo.

    Args:
        model_path: ruta donde guardar el artefacto (.joblib)

    Returns:
        dict con accuracy y f1_macro
    """
    # --- 1. CARGAR DATOS ---
    # Iris: 150 flores, 4 features, 3 especies:
    #   0 = Iris Setosa
    #   1 = Iris Versicolor
    #   2 = Iris Virginica
    iris = load_iris()
    X, y = iris.data, iris.target

    # --- 2. DIVIDIR EN TRAIN Y TEST ---
    # 80% entrenamiento, 20% evaluación
    # random_state fijo → reproducibilidad
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=39758307
    )

    # --- 3. ENTRENAR EL MODELO ---
    # RandomForest: ensemble de 100 árboles de decisión
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=39758307)
    model.fit(X_train, y_train)

    # --- 4. EVALUAR ---
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")

    print(f"acc: {acc:.4f}")
    print(f"f1_macro: {f1:.4f}")

    # --- 5. GUARDAR MODELO ---
    # Empaquetamos el modelo + metadata en un solo archivo .joblib
    # Esto es lo que la API (FastAPI) va a cargar para hacer predicciones
    os.makedirs(
        os.path.dirname(model_path) if os.path.dirname(model_path) else ".",
        exist_ok=True,
    )

    model_artifact = {
        "model": model,
        "feature_names": list(iris.feature_names),
        "target_names": iris.target_names.tolist(),
        "accuracy": acc,
        "version": "1.0.0",
    }

    joblib.dump(model_artifact, model_path)
    print(f"modelo guardado en: {model_path}")

    return {"accuracy": acc, "f1_macro": f1}


if __name__ == "__main__":
    train_model()
