# ================================================
# Recurso: Imagen Docker
# ================================================
# Terraform referencia la imagen que ya fue construida
# con "docker build" previamente.

resource "docker_image" "iris_api" {
  name         = var.image_name
  keep_locally = true
}

# ================================================
# Recurso: Contenedor Docker
# ================================================
# Terraform crea y gestiona el contenedor.
# Si cambias algo acá y hacés "terraform apply",
# Terraform destruye el viejo y crea uno nuevo.

resource "docker_container" "iris_api" {
  name  = var.container_name
  image = docker_image.iris_api.image_id

  ports {
    internal = var.internal_port
    external = var.external_port
  }

  # Reiniciar automáticamente si se cae
  restart = "unless-stopped"

  # Eliminar el contenedor al destruir
  must_run = true
}
