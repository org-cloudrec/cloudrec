# cloudrec/terraform/modules/pubsub/main.tf
resource "google_pubsub_topic" "log_topic" {
  name = var.log_topic_name
}

output "topic_id" {
  value = google_pubsub_topic.log_topic.id
  description = "The ID of the Pub/Sub topic created."
}