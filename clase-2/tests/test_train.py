"""
Tests para el módulo de entrenamiento (clase-2).
Verifica que train_model() entrene, evalúe y guarde el modelo.
"""

import sys
import os
import tempfile
from pathlib import Path

import joblib

# Agregar src/ al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from train import train_model  # noqa: E402


def test_train_returns_valid_metrics():
    """Verifica que el entrenamiento devuelva métricas válidas."""
    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "model.joblib")
        metrics = train_model(model_path=model_path)

        # train_model() devuelve un dict con accuracy y f1_macro
        assert "accuracy" in metrics
        assert "f1_macro" in metrics

        # Validar rango
        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert 0.0 <= metrics["f1_macro"] <= 1.0

        # Calidad mínima (Iris es un dataset fácil)
        assert metrics["accuracy"] >= 0.85, f"Accuracy muy baja: {metrics['accuracy']}"
        assert metrics["f1_macro"] >= 0.85, f"F1 muy bajo: {metrics['f1_macro']}"


def test_train_saves_model():
    """Verifica que train_model() guarde el modelo en disco."""
    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "model.joblib")
        train_model(model_path=model_path)

        # Verificar que el archivo existe
        assert os.path.exists(model_path), "El modelo no se guardó"

        # Verificar que se puede cargar
        artifact = joblib.load(model_path)
        assert "model" in artifact
        assert "feature_names" in artifact
        assert "target_names" in artifact
        assert "accuracy" in artifact
        assert "version" in artifact


def test_train_reproducibility():
    """Verifica que el entrenamiento sea reproducible."""
    with tempfile.TemporaryDirectory() as tmpdir:
        m1 = train_model(model_path=os.path.join(tmpdir, "m1.joblib"))
        m2 = train_model(model_path=os.path.join(tmpdir, "m2.joblib"))

        assert m1["accuracy"] == m2["accuracy"], "Accuracy no reproducible"
        assert m1["f1_macro"] == m2["f1_macro"], "F1 no reproducible"
