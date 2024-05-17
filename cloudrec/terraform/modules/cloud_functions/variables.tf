# variables.tf

variable "google_cloudfunctions_function_name" {
  description = "The name of the cloud function"
  type        = string
}

variable "cloudrec_bucket" {
  description = "The name of the bucket of cloudrec"
  type        = string
}

variable "log_topic_id" {
  description = "The id of the log topic"
  type        = string
}

variable "region" {
  description = "The region of the cloudrec"
  type        = string
}