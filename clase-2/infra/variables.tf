# ================================================
# Variables configurables
# ================================================
# Estas variables permiten cambiar el comportamiento
# del despliegue sin modificar el código principal.

variable "container_name" {
  description = "Nombre del contenedor Docker"
  type        = string
  default     = "iris-api"
}

variable "image_name" {
  description = "Nombre de la imagen Docker"
  type        = string
  default     = "iris-api:latest"
}

variable "external_port" {
  description = "Puerto externo (el que usás en el navegador)"
  type        = number
  default     = 8000
}

variable "internal_port" {
  description = "Puerto interno del contenedor"
  type        = number
  default     = 8000
}
