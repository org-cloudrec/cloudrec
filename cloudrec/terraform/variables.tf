# variables.tf

variable "project_id" {
  description = "The ID of the project to deploy resources."
  type        = string
}

variable "region" {
  description = "The region to deploy resources."
  type        = string
  default     = "us-central1"
}