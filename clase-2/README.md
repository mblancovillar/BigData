# Clase 2 - API de Inferencia + Docker Multi-Stage + Terraform

Práctica de BigData: servir un modelo de ML como API REST usando FastAPI, containerizar con Docker multi-stage build, y desplegar infraestructura con Terraform.

---

## Requisitos

- **Python 3.11**
- **Docker Desktop** (Windows/Mac)
- **Terraform** (>= 1.0)
- **Git Bash** (Windows) o Terminal (Mac)
- Cuenta **GitHub**

---

## Árbol del Proyecto

```
clase-2/
├─ src/
│  ├─ train.py              # Entrenamiento + guardado del modelo
│  └─ main.py               # API FastAPI
├─ tests/
│  ├─ test_train.py          # Tests del entrenamiento
│  └─ test_api.py            # Tests de la API
├─ infra/
│  ├─ provider.tf            # Proveedor Docker para Terraform
│  ├─ variables.tf           # Variables configurables
│  ├─ main.tf                # Recursos (imagen + container)
│  └─ outputs.tf             # URLs de salida
├─ Dockerfile                # Multi-stage: entrena + sirve
├─ requirements.txt
├─ requirements-dev.txt
├─ .pre-commit-config.yaml
├─ .gitignore
├─ README.md
└─ ONBOARDING.md
```

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Build (Multi-Stage)                  │
│                                                                     │
│  Stage 1: Builder               Stage 2: Runtime                   │
│  ┌─────────────────────┐        ┌──────────────────────────────┐   │
│  │ python:3.11-slim     │        │ python:3.11-slim              │   │
│  │                     │        │                              │   │
│  │ pip install deps    │        │ pip install deps             │   │
│  │ python train.py     │──────→ │ COPY model.joblib            │   │
│  │ → model.joblib      │ modelo │ COPY main.py                 │   │
│  │                     │        │ uvicorn main:app :8000       │   │
│  └─────────────────────┘        └──────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

                              ↓ Terraform despliega

┌──────────────────────────────────────────────────────────────────┐
│  Docker Container                                                │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  FastAPI (uvicorn :8000)                                  │    │
│  │                                                          │    │
│  │  GET  /         → info del servicio                      │    │
│  │  GET  /health   → health check                           │    │
│  │  GET  /info     → metadata del modelo                    │    │
│  │  POST /predict  → predicción (4 features → especie)      │    │
│  │  GET  /docs     → Swagger UI (documentación automática)  │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Instalación y Setup

### Windows (Git Bash)

```bash
cd /c/Users/<tu-usuario>/Desktop/BigData/clase-2

py -3.11 -m venv .venv || python -m venv .venv
source .venv/Scripts/activate

pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

pre-commit install
```

### Mac

```bash
cd ~/Desktop/BigData/clase-2

python3.11 -m venv .venv || python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

pre-commit install
```

---

## Uso Local (sin Docker)

### 1. Entrenar el modelo

```bash
python src/train.py
# Crea model.joblib en el directorio actual
```

### 2. Levantar la API

```bash
MODEL_PATH=model.joblib uvicorn src.main:app --reload --port 8000
```

### 3. Probar la API

```bash
# Abrir Swagger UI en el navegador:
#   http://localhost:8000/docs

# O desde la terminal:
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

---

## Docker

### Build + Run manual

```bash
# Construir imagen (entrena el modelo dentro)
docker build -t iris-api:latest .

# Correr el container
docker run -d --name iris-api -p 8000:8000 iris-api:latest

# Probar
curl http://localhost:8000/health

# Detener
docker stop iris-api && docker rm iris-api
```

### Con Terraform

```bash
# Primero: construir la imagen
docker build -t iris-api:latest .

# Luego: Terraform maneja el container
cd infra
terraform init
terraform plan
terraform apply

# Probar
curl http://localhost:8000/health

# Destruir
terraform destroy
```

---

## Tests

```bash
# Tests de entrenamiento
python -m pytest tests/test_train.py -v

# Tests de la API
python -m pytest tests/test_api.py -v

# Todos
python -m pytest -v
```
