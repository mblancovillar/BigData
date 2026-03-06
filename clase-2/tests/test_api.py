"""
Tests para la API de inferencia (FastAPI).
Usa TestClient para simular peticiones HTTP sin levantar un servidor real.
"""

import sys
import os
import tempfile
from pathlib import Path

# Agregar src/ al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Entrenar modelo temporal antes de importar la app
from train import train_model  # noqa: E402

# Crear modelo en /tmp para los tests
_test_model_path = os.path.join(tempfile.gettempdir(), "test_model.joblib")
train_model(model_path=_test_model_path)
os.environ["MODEL_PATH"] = _test_model_path

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)


def test_root():
    """GET / devuelve info del servicio."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "endpoints" in data


def test_health():
    """GET /health confirma que el modelo está cargado."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_info():
    """GET /info devuelve metadata del modelo."""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_type"] == "RandomForestClassifier"
    assert "accuracy" in data
    assert "feature_names" in data


def test_predict_setosa():
    """POST /predict con features típicas de Setosa."""
    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["prediction_label"] == "setosa"
    assert data["confidence"] > 0.5
    assert "prediction_id" in data


def test_predict_returns_all_fields():
    """POST /predict devuelve todos los campos del schema."""
    response = client.post(
        "/predict",
        json={
            "sepal_length": 6.7,
            "sepal_width": 3.0,
            "petal_length": 5.2,
            "petal_width": 2.3,
        },
    )
    assert response.status_code == 200
    data = response.json()
    required_fields = [
        "prediction",
        "prediction_label",
        "confidence",
        "probabilities",
        "model_version",
        "prediction_id",
        "timestamp",
    ]
    for field in required_fields:
        assert field in data, f"Falta campo: {field}"


def test_predict_invalid_input():
    """POST /predict con datos inválidos devuelve 422."""
    response = client.post(
        "/predict",
        json={
            "sepal_length": "no_es_numero",
        },
    )
    assert response.status_code == 422
