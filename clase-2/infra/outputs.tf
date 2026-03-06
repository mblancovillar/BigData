# ================================================
# Outputs: información útil después del deploy
# ================================================
# Terraform muestra estos valores al final de "terraform apply"

output "api_url" {
  description = "URL de la API"
  value       = "http://localhost:${var.external_port}"
}

output "docs_url" {
  description = "Documentación interactiva (Swagger UI)"
  value       = "http://localhost:${var.external_port}/docs"
}

output "health_url" {
  description = "Health check"
  value       = "http://localhost:${var.external_port}/health"
}

output "container_name" {
  description = "Nombre del contenedor desplegado"
  value       = docker_container.iris_api.name
}

output "test_predict" {
  description = "Comando para probar la API"
  value       = "curl -X POST http://localhost:${var.external_port}/predict -H 'Content-Type: application/json' -d '{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}'"
}
