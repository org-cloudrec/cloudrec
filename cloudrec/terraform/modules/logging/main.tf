# cloudrec/terraform/modules/logging/main.tf
resource "google_logging_project_sink" "project_sink" {
  name                   = var.google_logging_project_sink_name
  destination            = "pubsub.googleapis.com/${var.log_topic_id}"
  filter                 = "resource.type=\"gcs_bucket\" AND protoPayload.methodName=\"storage.buckets.create\""
  unique_writer_identity = true
}

resource "google_pubsub_topic_iam_binding" "pubsub_topic_binding" {
  topic  = var.log_topic_name
  role   = "roles/pubsub.publisher"
  members = [
    google_logging_project_sink.project_sink.writer_identity
  ]
}