# Onboarding - Clase 1

Guía paso a paso para configurar el entorno de BigData.

---

## ¿Qué es Git?

Git es un **sistema de control de versiones** — registra cada cambio que hacés en tu código como una "foto" (commit). Esto permite:

- **Volver atrás** si algo se rompe
- **Ver el historial** de quién cambió qué y cuándo
- **Trabajar en paralelo** sin pisarse (ramas)

### Conceptos clave

| Concepto | Qué es | Ejemplo |
|----------|--------|---------|
| **Repositorio** | Carpeta con historial de Git | Este proyecto |
| **Commit** | Una "foto" del código en un momento dado | `git commit -m "Agregué modelo"` |
| **Rama (branch)** | Línea de trabajo independiente | `feature/juanperez` |
| **Push** | Subir tus commits a GitHub | `git push` |
| **Pull** | Descargar cambios de GitHub | `git pull` |
| **Clone** | Copiar un repo remoto a tu máquina | `git clone <url>` |

### Flujo básico de Git

```
1. Editás archivos         →  tu código cambia localmente
2. git add .               →  marcás los cambios para el próximo commit
3. git commit -m "mensaje" →  creás una "foto" con descripción
4. git push                →  subís esa foto a GitHub
```

---

## ¿Qué es CI/CD?

**CI** = Continuous Integration (Integración Continua)
**CD** = Continuous Delivery/Deployment (Entrega/Despliegue Continuo)

En la práctica: **cada vez que hacés `git push`, GitHub ejecuta automáticamente** tests, formateo y builds para verificar que tu código funciona.

```
Developer hace push → GitHub Actions detecta el push → Corre los checks automáticamente

   git push  ──→  ┌──────────────────────┐
                   │   GitHub Actions      │
                   │                      │
                   │  1. Formateo (black) │
                   │  2. Linting (ruff)   │
                   │  3. Tests (pytest)   │
                   │  4. Build (Docker)   │
                   │                      │
                   │  ✅ Todo pasó        │
                   │  ❌ Algo falló       │
                   └──────────────────────┘
```

**¿Por qué importa?**
- Detecta errores **antes de que lleguen a producción**
- Nadie se olvida de correr los tests
- Todo el equipo tiene las mismas reglas

En este proyecto, el archivo `.github/workflows/ci-clase-1.yml` define qué pasos correr en cada push.

---

## 1. Requisitos Previos — Instalar todo antes de empezar

### Windows

1. **Git for Windows** (incluye Git Bash, la terminal que vamos a usar):
   - Descargar de: https://git-scm.com/download/win
   - Instalar con las opciones por defecto
   - Al finalizar, abrir **Git Bash** desde el menú inicio

2. **Python 3.11**:
   - Descargar de: https://www.python.org/downloads/
   - **IMPORTANTE:** Tildar ✅ "Add Python to PATH" durante la instalación

3. **Docker Desktop**:
   - Descargar de: https://www.docker.com/products/docker-desktop
   - Instalar y abrir Docker Desktop (debe quedar corriendo)

4. **Visual Studio Code**:
   - Descargar de: https://code.visualstudio.com/
   - Instalar siguiendo los pasos del instalador

### Mac

1. **Git** (ya viene instalado en Mac, verificar):
   ```bash
   git --version
   ```

2. **Python 3.11**:
   ```bash
   brew install python@3.11
   python3.11 --version
   ```

3. **Docker Desktop**:
   - Descargar de: https://www.docker.com/products/docker-desktop
   - Instalar y abrir Docker Desktop

4. **Visual Studio Code**:
   - Descargar de: https://code.visualstudio.com/

---

## 2. Configuración Git

Abrir **Git Bash** (Windows) o **Terminal** (Mac) y configurar tu identidad:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

**Solo Windows — configurar line endings:**

```bash
git config --global core.autocrlf input
```

---

## 3. Activar GitHub Copilot (Alumnos)

1. Ir a: `https://github.com/settings/education/benefits`
2. Solicitar acceso a **GitHub Education / Student Developer Pack**
3. **Adjuntar certificado de alumno regular de la Universidad**
4. Una vez aprobado (puede tardar 1-3 días), activar **GitHub Copilot** en tu cuenta
5. Instalar extensión de **GitHub Copilot** en VS Code

---

## 4. Clonar el Repositorio

### Opción 1: Desde VS Code (Recomendado)

1. Abrir **VS Code**
2. Presionar `Ctrl+Shift+P` (Windows/Linux) o `Cmd+Shift+P` (Mac)
3. Buscar y seleccionar **"Git: Clone"**
4. Pegar la URL del repositorio:
   ```
   https://github.com/PabloBandeira/BigData.git
   ```
5. Seleccionar dónde guardar (ej: `~/Desktop/BigData`)
6. VS Code abrirá automáticamente el repositorio

### Opción 2: Desde Terminal

```bash
cd ~/Desktop
git clone https://github.com/PabloBandeira/BigData.git
cd BigData/clase-1
```

---

## 5. Setup del Proyecto

### Windows (Git Bash)

```bash
# Navegar a clase-1
cd /c/Users/<tu-usuario>/Desktop/BigData/clase-1

# Crear y activar venv
py -3.11 -m venv .venv || python -m venv .venv || python3 -m venv .venv
source .venv/Scripts/activate

# Verificar activación (debe mostrar ruta a .venv)
which python

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# Configurar pre-commit
pre-commit install

# Verificar instalación
python -m pytest -q
python src/train.py
```

### Mac (bash/zsh)

```bash
# Navegar a clase-1
cd ~/Desktop/BigData/clase-1

# Crear y activar venv
python3.11 -m venv .venv || python3 -m venv .venv
source .venv/bin/activate

# Verificar activación (debe mostrar ruta a .venv)
which python

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# Configurar pre-commit
pre-commit install

# Verificar instalación
python -m pytest -q
python src/train.py
```

---

## 6. Workflow: Subir tus Cambios (Alumnos)

### Práctica guiada — Comandos esenciales

```bash
# Ver el estado actual (qué archivos cambiaron)
git status

# Agregar TODOS los archivos modificados al staging
git add .

# Agregar un archivo específico
git add src/train.py

# Crear un commit (foto del código) con mensaje descriptivo
git commit -m "Entrené modelo RandomForest con Iris"

# Ver el historial de commits
git log --oneline

# Subir los commits a GitHub
git push
```

**Buenas prácticas para commits:**
- Escribir mensajes **claros y descriptivos** (no "asdf" o "cambios")
- Hacer commits **pequeños y frecuentes** (un commit por tarea)
- Ejemplos buenos: `"Agregué test de reproducibilidad"`, `"Corregí accuracy baja"`

### Crear tu rama personal

```bash
# Crear y cambiar a tu rama (usá tu nombre y apellido sin espacios)
git checkout -b feature/nombreapellido
```

**Ejemplo:**
```bash
git checkout -b feature/juanperez
```

### Subir tus cambios

```bash
# Ver qué cambios hiciste
git status

# Agregar tus cambios
git add .

# Crear commits con descripciones claras
git commit -m "Experimento: [descripción de qué hiciste]"

# ⚠️ PRIMER push (solo la primera vez, vincula tu rama local con GitHub)
git push --set-upstream origin "feature/nombreapellido"

# A partir de ahí, todos los pushes siguientes son simplemente:
git push
```

### El profesor revisa tu código

El profesor accede a GitHub y revisa:
- Tu rama en: `https://github.com/PabloBandeira/BigData`
- Todos tus commits
- Los cambios que hiciste
- Tus resultados y experimentos

### ⚠️ Importante

- **NO pushees directamente a `main`** — siempre usá tu rama personal (`feature/nombreapellido`)
- Cada cambio importante = nuevo commit con descripción clara
- Los commits permiten que el profesor vea el progreso paso a paso

---

## 7. Chequeos de Validación

Ejecutar cada comando y verificar la salida esperada:

### Pre-commit checks

```bash
pre-commit run --all-files
```

**¿Qué hace cada check?**
- **black** → formateador automático de Python. Corrige espacios, indentación, saltos de línea para que el código siga un estilo uniforme.
- **ruff** → linter rápido. Detecta errores, imports sin usar, variables mal nombradas, etc.

**Salida esperada (todo bien):**
```
black....................................................................Passed
ruff.....................................................................Passed
```

**Si black muestra "Failed":**
```
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted clase-1/src/train.py

All done! ✨ 🍰 ✨
1 file reformatted.

ruff.....................................................................Passed
```

**Esto NO es un error grave.** Significa que black reformateó tu archivo automáticamente. ¿Qué hacer?

```bash
# 1. Ver qué archivo cambió
git status

# 2. Agregar el archivo reformateado
git add .

# 3. Volver a correr pre-commit para verificar que ahora pasa
pre-commit run --all-files

# Ahora debería mostrar:
# black....................................................................Passed
# ruff.....................................................................Passed
```

Después de eso ya podés hacer el commit normalmente.

### Tests

```bash
python -m pytest -q
```

**Salida esperada:**
```
..                                                                [100%]
2 passed in 0.XX s
```

### Entrenamiento local

```bash
python src/train.py
```

**Salida esperada:**
```
acc: 0.9667
f1_macro: 0.9667
```

---

## 8. Docker

**Primero: abrir Docker Desktop**

### Docker build

**Windows (Git Bash):**
```bash
cd /c/Users/<tu-usuario>/Desktop/BigData/clase-1
docker build -t demo-ml:local .
```

**Mac:**
```bash
cd ~/Desktop/BigData/clase-1
docker build -t demo-ml:local .
```

### Docker run

**Windows (Git Bash):**
```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$PWD:/app" demo-ml:local
```

**Mac:**
```bash
docker run --rm -v "$PWD:/app" demo-ml:local
```

**Apple Silicon (M1/M2/M3) — si Docker falla:**
```bash
docker build --platform=linux/amd64 -t demo-ml:local .
docker run --rm --platform=linux/amd64 -v "$PWD:/app" demo-ml:local
```

**Salida esperada:**
```
acc: 0.9667
f1_macro: 0.9667
```

---

## Problemas Comunes

### Windows Git Bash

**`py` no funciona:**
```bash
python --version
python -m venv .venv
```

**Docker paths no funcionan:**
```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$PWD:/app" demo-ml:local
```

**Scripts `.sh` no ejecutan:**
```bash
dos2unix scripts/*.sh
# O ejecutar con bash explícitamente
bash scripts/nombre.sh
```

### Mac

**`python3.11` no encontrado:**
```bash
brew install python@3.11
brew link python@3.11
```

**Permission denied en Docker:**
```bash
sudo usermod -aG docker $USER
# Logout y login nuevamente
```

---

## Resumen de Comandos por OS

| Tarea | Windows (Git Bash) | Mac (bash/zsh) |
|-------|-------------------|----------------|
| Crear venv | `py -3.11 -m venv .venv` | `python3.11 -m venv .venv` |
| Activar venv | `source .venv/Scripts/activate` | `source .venv/bin/activate` |
| Docker run | `MSYS_NO_PATHCONV=1 docker run -v "$PWD:/app"` | `docker run -v "$PWD:/app"` |
| Docker interactivo | `winpty docker run -it` | `docker run -it` |

---

## Siguiente Paso

Una vez que todos los chequeos pasen localmente:

1. **Crear tu rama**: `git checkout -b feature/nombreapellido`
2. **Hacer cambios y experimentar**
3. **Pushear** a tu rama
4. **GitHub Actions correrá automáticamente** y verás si los tests pasan
5. **El profesor revisará tu rama** directamente en GitHub
6. Cuando estés listo, continúa con **Clase 2**


