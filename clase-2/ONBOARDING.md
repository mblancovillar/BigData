# Onboarding - Clase 2

Guía paso a paso para la clase 2 de BigData: API de inferencia + Docker multi-stage + Terraform.

---

## ¿Qué vamos a hacer en esta clase?

En la clase 1 entrenamos un modelo y lo corrimos localmente. Ahora vamos a:

1. **Guardar el modelo** entrenado en un archivo (`.joblib`) para poder reutilizarlo
2. **Crear una API REST** con FastAPI para que cualquiera pueda hacer predicciones
3. **Containerizar todo** con Docker (multi-stage build)
4. **Gestionar la infraestructura** con Terraform (Infrastructure as Code)

```
Clase 1                          Clase 2
───────                          ───────
python train.py → métricas       python train.py → model.joblib
                                                      ↓
                                 FastAPI sirve el modelo como API REST
                                                      ↓
                                 Docker empaqueta entrenamiento + API
                                                      ↓
                                 Terraform despliega el container
```

---

## Conceptos Clave

### ¿Qué es una API REST?

Una **API** (Application Programming Interface) es una forma de comunicarse con un programa a través de **peticiones HTTP** (como cuando el navegador pide una página web).

**REST** es un estilo de diseño que usa **URLs + verbos HTTP**:

| Verbo  | URL         | Qué hace                        |
|--------|-------------|----------------------------------|
| GET    | `/`         | Info del servicio                |
| GET    | `/health`   | ¿Está viva la API?              |
| GET    | `/info`     | Metadata del modelo              |
| POST   | `/predict`  | Enviar datos → recibir predicción|

**Ejemplo: predicción**

```
Petición (POST /predict):
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}

Respuesta:
{
  "prediction": 0,
  "prediction_label": "setosa",
  "confidence": 0.97,
  "probabilities": {
    "setosa": 0.97,
    "versicolor": 0.02,
    "virginica": 0.01
  }
}
```

### ¿Qué es FastAPI?

**FastAPI** es un framework de Python para crear APIs. Se elige porque:

- **Rápido**: uno de los frameworks más rápidos de Python
- **Validación automática**: con Pydantic, valida que los datos de entrada sean correctos
- **Documentación automática**: genera Swagger UI en `/docs` sin escribir nada extra
- **Async**: soporta operaciones asíncronas nativamente

### ¿Qué es un Docker Multi-Stage Build?

En la clase 1, el Dockerfile tenía una sola etapa. Ahora usamos **dos etapas**:

```
Stage 1: "Builder"                    Stage 2: "Runtime"
┌──────────────────────────┐          ┌──────────────────────────┐
│ Instala dependencias     │          │ Instala dependencias     │
│ Copia train.py           │          │ Copia main.py (API)      │
│ Ejecuta python train.py  │          │ Copia model.joblib ←──── │ (del builder)
│ Genera model.joblib      │──────→   │ Inicia uvicorn           │
└──────────────────────────┘          └──────────────────────────┘
  (se descarta al final)               (esta es la imagen final)
```

**¿Por qué?**
- El modelo se entrena **una sola vez** durante el build
- La imagen final **no incluye el código de entrenamiento** (más liviana y segura)
- El modelo queda "cocinado" dentro de la imagen

### ¿Qué es Terraform?

**Terraform** es una herramienta de **Infrastructure as Code (IaC)** — definís tu infraestructura en archivos `.tf` y Terraform la crea/modifica/destruye automáticamente.

**Sin Terraform:**
```bash
# Cada vez que querés correr la API, escribís estos comandos a mano:
docker run -d --name iris-api -p 8000:8000 --restart unless-stopped iris-api:latest
# ¿Y si te equivocás en un parámetro? ¿Y si el equipo usa comandos diferentes?
```

**Con Terraform:**
```hcl
# main.tf — la infraestructura queda documentada y versionada
resource "docker_container" "iris_api" {
  name  = "iris-api"
  image = docker_image.iris_api.image_id
  ports {
    internal = 8000
    external = 8000
  }
}
```

**Flujo de Terraform:**

```
terraform init      →  Descarga el provider (plugin de Docker)
terraform plan      →  Muestra qué va a crear/cambiar/destruir
terraform apply     →  Ejecuta los cambios
terraform destroy   →  Elimina todo lo que creó
```

**Archivos de Terraform en este proyecto:**

| Archivo         | Qué define                                         |
|-----------------|-----------------------------------------------------|
| `provider.tf`   | Qué provider usar (Docker, en nuestro caso)         |
| `variables.tf`  | Variables configurables (nombre, puerto, imagen)     |
| `main.tf`       | Los recursos a crear (imagen Docker + container)     |
| `outputs.tf`    | Valores de salida (URLs para probar la API)          |

---

## 1. Requisitos Previos

Todo lo de la clase 1 sigue siendo necesario (Git, Python 3.11, Docker Desktop, VS Code).

Además, necesitás instalar **Terraform**:

### Windows

1. Descargar de: https://developer.hashicorp.com/terraform/install
2. Extraer el archivo `.zip` (contiene un solo ejecutable: `terraform.exe`)
3. Mover `terraform.exe` a una carpeta que esté en el PATH (ej: `C:\Windows\`)

Alternativamente, con **Chocolatey**:
```bash
choco install terraform
```

4. Verificar instalación:
```bash
terraform --version
```

### Mac

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform --version
```

---

## 2. Setup del Proyecto

### Windows (Git Bash)

```bash
cd /c/Users/<tu-usuario>/Desktop/BigData/clase-2

py -3.11 -m venv .venv || python -m venv .venv || python3 -m venv .venv
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

## 3. Flujo Paso a Paso

### Paso 1 — Entrenar el modelo

```bash
python src/train.py
```

**Salida esperada:**
```
acc: 0.9667
f1_macro: 0.9667
modelo guardado en: model.joblib
```

Esto crea `model.joblib` — un archivo que contiene el modelo entrenado + metadata.

### Paso 2 — Levantar la API localmente

```bash
MODEL_PATH=model.joblib uvicorn src.main:app --reload --port 8000
```

**Salida esperada:**
```
INFO:     Cargando modelo desde model.joblib...
INFO:     Modelo cargado — versión: 1.0.0, accuracy: 0.9667
INFO:     API lista para recibir peticiones
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Paso 3 — Probar la API

Abrir en el navegador: **http://localhost:8000/docs**

Esto abre **Swagger UI** (documentación interactiva). Desde ahí se puede probar cada endpoint visualmente.

O desde otra terminal:

```bash
# Health check
curl http://localhost:8000/health

# Predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

**Detener la API:** `Ctrl + C` en la terminal donde corre uvicorn.

### Paso 4 — Docker Build

```bash
docker build -t iris-api:latest .
```

**¿Qué pasa durante el build?**
1. Stage 1 (builder): instala dependencias → ejecuta `train.py` → genera `model.joblib`
2. Stage 2 (runtime): copia `model.joblib` del builder → copia `main.py` → configura uvicorn

### Paso 5 — Terraform

```bash
cd infra

# Inicializar Terraform (descarga el provider de Docker)
terraform init

# Ver qué va a hacer (sin ejecutar nada)
terraform plan

# Ejecutar: crea el container
terraform apply
# Terraform pregunta "Do you want to perform these actions?" → escribir "yes"
```

**Salida esperada después de `apply`:**
```
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

api_url = "http://localhost:8000"
docs_url = "http://localhost:8000/docs"
health_url = "http://localhost:8000/health"
```

### Paso 6 — Verificar

```bash
# Health check
curl http://localhost:8000/health

# Predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 6.7, "sepal_width": 3.0, "petal_length": 5.2, "petal_width": 2.3}'
```

### Paso 7 — Destruir la infraestructura

```bash
cd infra
terraform destroy
# Escribir "yes" cuando pregunte
```

---

## 4. Tests

```bash
# Desde clase-2/ (no desde infra/)
python -m pytest -v
```

**Salida esperada:**
```
tests/test_train.py::test_train_returns_valid_metrics PASSED
tests/test_train.py::test_train_saves_model PASSED
tests/test_train.py::test_train_reproducibility PASSED
tests/test_api.py::test_root PASSED
tests/test_api.py::test_health PASSED
tests/test_api.py::test_info PASSED
tests/test_api.py::test_predict_setosa PASSED
tests/test_api.py::test_predict_returns_all_fields PASSED
tests/test_api.py::test_predict_invalid_input PASSED
9 passed
```

---

## 5. Chequeos de Validación

### Pre-commit

```bash
pre-commit run --all-files
```

**Salida esperada:**
```
black....................................................................Passed
ruff.....................................................................Passed
```

Si black reformatea un archivo, agregar con `git add .` y volver a correr.

---

## 6. Workflow: Subir tus Cambios

Mismo flujo que clase 1:

```bash
# Asegurarse de estar en tu rama
git checkout feature/nombreapellido

# Ver cambios
git status

# Agregar y commitear
git add .
git commit -m "Clase 2: API con FastAPI + Docker + Terraform"

# Subir
git push
```

---

## Problemas Comunes

### "Modelo no encontrado"

La API busca `model.joblib` en la ruta definida por `MODEL_PATH`. Si corrés localmente:
```bash
# Asegurarse de haber entrenado primero
python src/train.py
# Luego levantar con la ruta correcta
MODEL_PATH=model.joblib uvicorn src.main:app --reload --port 8000
```

### Docker: "port is already allocated"

El puerto 8000 ya está en uso. Opciones:
```bash
# Ver qué usa el puerto
lsof -i :8000

# Detener el container anterior
docker stop iris-api && docker rm iris-api

# O usar otro puerto
docker run -d --name iris-api -p 9000:8000 iris-api:latest
```

### Terraform: "Error acquiring the state lock"

```bash
terraform force-unlock <LOCK_ID>
```

### Terraform: "image not found"

Hay que construir la imagen Docker ANTES de correr terraform:
```bash
# Volver a clase-2/
cd ..
docker build -t iris-api:latest .
cd infra
terraform apply
```

### Apple Silicon (M1/M2/M3)

Si Docker falla durante el build:
```bash
docker build --platform=linux/amd64 -t iris-api:latest .
```

### curl no disponible en Windows

Usar Git Bash o PowerShell. En Git Bash, curl viene incluido.
