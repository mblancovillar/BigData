"""
API de inferencia para el modelo Iris usando FastAPI.
Carga el modelo entrenado (.joblib) y expone endpoints REST
para hacer predicciones.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import os
from typing import Dict
import logging
import uuid
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="Iris Prediction API",
    description="API de inferencia para clasificación de flores Iris",
    version="1.0.0",
)

# Variable global para el modelo
MODEL = None
MODEL_METADATA = {}


# --- SCHEMAS ---
# Pydantic valida automáticamente los datos de entrada y salida


class IrisFeatures(BaseModel):
    """Schema de entrada: las 4 medidas de la flor"""

    sepal_length: float = Field(
        ..., ge=0, le=10, description="Longitud del sépalo (cm)"
    )
    sepal_width: float = Field(..., ge=0, le=10, description="Ancho del sépalo (cm)")
    petal_length: float = Field(
        ..., ge=0, le=10, description="Longitud del pétalo (cm)"
    )
    petal_width: float = Field(..., ge=0, le=10, description="Ancho del pétalo (cm)")

    class Config:
        json_schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
        }


class PredictionResponse(BaseModel):
    """Schema de salida: resultado de la predicción"""

    prediction: int = Field(..., description="Clase predicha (0, 1, 2)")
    prediction_label: str = Field(..., description="Nombre de la especie")
    confidence: float = Field(..., description="Confianza de la predicción")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades por clase")
    model_version: str = Field(..., description="Versión del modelo")
    prediction_id: str = Field(..., description="ID único de la predicción")
    timestamp: str = Field(..., description="Timestamp ISO 8601")


# --- CARGA DEL MODELO ---


def load_model():
    """Carga el modelo desde model.joblib (creado durante el docker build)."""
    global MODEL, MODEL_METADATA

    model_path = os.environ.get("MODEL_PATH", "/app/model.joblib")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo no encontrado en {model_path}")

    logger.info(f"Cargando modelo desde {model_path}...")
    model_artifact = joblib.load(model_path)
    MODEL = model_artifact["model"]
    MODEL_METADATA = {
        "feature_names": model_artifact["feature_names"],
        "target_names": model_artifact["target_names"],
        "accuracy": model_artifact["accuracy"],
        "version": model_artifact["version"],
    }
    logger.info(
        f"Modelo cargado — versión: {MODEL_METADATA['version']}, accuracy: {MODEL_METADATA['accuracy']:.4f}"
    )


@app.on_event("startup")
async def startup_event():
    """Se ejecuta al iniciar la API — carga el modelo"""
    load_model()
    logger.info("API lista para recibir peticiones")


# --- ENDPOINTS ---


@app.get("/")
async def root():
    """Información del servicio"""
    return {
        "service": "Iris Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "predict": "POST /predict",
            "health": "GET /health",
            "info": "GET /info",
            "docs": "GET /docs",
        },
    }


@app.get("/health")
async def health_check():
    """Health check — usado por Docker/Kubernetes para saber si la API está viva"""
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    return {"status": "healthy", "model_loaded": True}


@app.get("/info")
async def model_info():
    """Información del modelo cargado"""
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    return {
        "model_type": "RandomForestClassifier",
        "version": MODEL_METADATA.get("version"),
        "accuracy": MODEL_METADATA.get("accuracy"),
        "feature_names": MODEL_METADATA.get("feature_names"),
        "target_names": MODEL_METADATA.get("target_names"),
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: IrisFeatures):
    """
    Endpoint principal de predicción.
    Recibe las 4 medidas de una flor Iris → devuelve la especie predicha.
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")

    # Convertir features a array numpy
    feature_array = np.array(
        [
            [
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width,
            ]
        ]
    )

    # Predicción
    prediction = MODEL.predict(feature_array)[0]
    probabilities = MODEL.predict_proba(feature_array)[0]

    # Obtener etiqueta
    target_names = MODEL_METADATA.get("target_names", ["0", "1", "2"])
    prediction_label = target_names[prediction]
    confidence = float(probabilities[prediction])

    # Probabilidades por clase
    prob_dict = {target_names[i]: float(p) for i, p in enumerate(probabilities)}

    logger.info(f"Predicción: {prediction_label} (confianza: {confidence:.4f})")

    return PredictionResponse(
        prediction=int(prediction),
        prediction_label=prediction_label,
        confidence=confidence,
        probabilities=prob_dict,
        model_version=MODEL_METADATA.get("version", "1.0.0"),
        prediction_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow().isoformat() + "Z",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
