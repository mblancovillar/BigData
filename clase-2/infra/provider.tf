# ================================================
# Provider: Docker
# ================================================
# Terraform usa el provider de Docker para gestionar
# imágenes y contenedores directamente desde código.

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
  required_version = ">= 1.0"
}

provider "docker" {
  # Se conecta al Docker daemon local
}
