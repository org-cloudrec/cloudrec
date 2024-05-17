# outputs.tf
output "project_id" {
  value       = "${var.project_id}"
  description = "O nome do bucket de armazenamento criado."
}