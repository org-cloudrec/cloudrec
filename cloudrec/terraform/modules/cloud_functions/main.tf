// cloud_functions.tf
resource "google_storage_bucket" "cloudrec_bucket_functions" {
  name = var.cloudrec_bucket
  location = var.region
}

# if you need a variable with interpolation, you can use locals
locals {
  zip_path = "./modules/cloud_functions/function_export/function.zip"
}

resource "google_storage_bucket_object" "function_source" {
  name   = "functions/function_export.zip"
  bucket = google_storage_bucket.cloudrec_bucket_functions.name
  source = local.zip_path
}

resource "google_cloudfunctions_function" "cloudrec_function_export_logging" {
  name        = var.google_cloudfunctions_function_name
  entry_point = "generate_terraform_file"
  runtime     = "python39"
  available_memory_mb   = 128
  timeout               = 30

  source_archive_bucket = google_storage_bucket.cloudrec_bucket_functions.name
  source_archive_object = google_storage_bucket_object.function_source.name

  depends_on = [google_storage_bucket_object.function_source]

  environment_variables = {
    OUTPUT_BUCKET = var.cloudrec_bucket
    CODE_SHA = filebase64sha256(local.zip_path)
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = var.log_topic_id
  }
}
