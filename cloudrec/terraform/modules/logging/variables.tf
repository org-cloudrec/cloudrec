# variables.tf

variable "google_logging_project_sink_name" {
  description = "The name of the logging sink"
  type        = string
}

variable "log_topic_name" {
  description = "The name of the log topic"
  type        = string
}

variable "log_topic_id" {
  description = "The id of the log topic"
  type        = string
}