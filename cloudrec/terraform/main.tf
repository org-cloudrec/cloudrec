# cloudrec/terraform/main.tf
provider "google" {
  project     = var.project_id
  region      = var.region
}

# if you need a variable with interpolation, you can use locals
locals {
  log_topic_name = "cloudrec-topic-creation-logs"
  google_logging_project_sink_name = "bucket-creation-sink"
  google_cloudfunctions_function_name = "cloudrec-function-export-logging-test"
  cloudrec_bucket = "cloudrec-bucket-${var.project_id}"
}

module "googleapis" {
  source = "./modules/googleapis"
}

module "pubsub" {
  source = "./modules/pubsub"
  log_topic_name = local.log_topic_name
}

module "logging" {
  source = "./modules/logging"
  google_logging_project_sink_name = local.google_logging_project_sink_name
  log_topic_name = local.log_topic_name
  log_topic_id = module.pubsub.topic_id
}

module "cloud_functions" {
  source = "./modules/cloud_functions"
  google_cloudfunctions_function_name = local.google_cloudfunctions_function_name
  cloudrec_bucket = local.cloudrec_bucket
  log_topic_id = module.pubsub.topic_id
  region      = var.region
}
