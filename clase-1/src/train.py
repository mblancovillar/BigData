"""
Entrenamiento básico de modelo con scikit-learn.
Dataset: Iris
Semilla fija para reproducibilidad.
"""

# scikit-learn es la librería estándar de ML en Python
# Cada import trae una herramienta específica del pipeline
from sklearn.datasets import (
    load_iris,
)  # Dataset de flores Iris (150 muestras, 3 clases)
from sklearn.model_selection import (
    train_test_split,
)  # Divide datos en entrenamiento y evaluación
from sklearn.ensemble import (
    RandomForestClassifier,
)  # Modelo: bosque de árboles de decisión
from sklearn.metrics import accuracy_score, f1_score  # Métricas para evaluar el modelo


def main():
    # --- 1. CARGAR DATOS ---
    # Iris: 150 flores con 4 features (largo/ancho de sépalo y pétalo)
    # X = features (matriz), y = etiquetas numéricas → 3 especies:
    #   0 = Iris Setosa
    #   1 = Iris Versicolor
    #   2 = Iris Virginica
    iris = load_iris()
    X, y = iris.data, iris.target

    # --- 2. DIVIDIR EN TRAIN Y TEST ---
    # test_size=0.2 → 80% para entrenar, 20% para evaluar
    # random_state fijo → garantiza que la división sea siempre la misma (reproducibilidad)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=39758307
    )

    # --- 3. ENTRENAR EL MODELO ---
    # RandomForest: ensemble de 100 árboles de decisión
    # Cada árbol vota, gana la clase más votada (reduce overfitting vs un solo árbol)
    # random_state fijo → mismo modelo en cada ejecución
    model = RandomForestClassifier(n_estimators=100, random_state=39758307)
    model.fit(X_train, y_train)  # Aprende los patrones del conjunto de entrenamiento

    # --- 4. EVALUAR ---
    # Predice las clases del conjunto de test (datos que el modelo nunca vio)
    y_pred = model.predict(X_test)

    # Accuracy: % de predicciones correctas sobre el total
    acc = accuracy_score(y_test, y_pred)

    # F1 macro: combina precisión y recall en una sola métrica por clase, luego los promedia
    #
    #                     PREDICCIÓN DEL MODELO
    #                    Positivo      Negativo
    #                 ┌─────────────┬─────────────┐
    #  R  Positivo    │     TP      │     FN      │ ← era real pero no lo detecté
    #  E              │  (acierto)  │ (me escapó) │
    #  A              ├─────────────┼─────────────┤
    #  L  Negativo    │     FP      │     TN      │
    #                 │(falsa alarma│  (acierto)  │
    #                 └─────────────┴─────────────┘
    #
    #   Precisión = TP / (TP + FP)  → de lo que predije positivo, ¿cuánto era real?
    #   Recall    = TP / (TP + FN)  → de lo real, ¿cuánto encontré?
    #   F1        = 2 × (Precisión × Recall) / (Precisión + Recall)
    #
    #   "macro" = calcula F1 para cada especie (Setosa, Versicolor, Virginica) y promedia
    f1 = f1_score(y_test, y_pred, average="macro")

    print(f"acc: {acc:.4f}")
    print(f"f1_macro: {f1:.4f}")

    # Retornamos las métricas para que los tests puedan validarlas automáticamente
    return acc, f1


if __name__ == "__main__":
    # Este bloque solo se ejecuta si corremos el archivo directamente (python src/train.py)
    # No se ejecuta si otro módulo hace `from train import main`
    main()
