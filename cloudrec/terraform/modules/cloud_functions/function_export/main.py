from google.cloud import storage
import base64
import json
import os


def generate_terraform_file(event, context):
    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')
        log_entry = json.loads(message)
    else:
        raise ValueError("No data found in event")

    process_log_entry(log_entry)


def process_log_entry(log_entry):
    try:
        bucket_name = log_entry['resource']['labels']['bucket_name']
        location = log_entry['resource']['labels']['location']
        output_bucket = os.getenv('OUTPUT_BUCKET')
        create_terraform_file(bucket_name, location, output_bucket)
    except KeyError as e:
        print(f"Key error: {e} - Possibly incorrect log format")


def create_terraform_file(bucket_name, location, output_bucket):
    terraform_config = f"""
    resource "google_storage_bucket" "{bucket_name}" {{
        name     = "{bucket_name}"
        location = "{location}"
    }}
    """
    client = storage.Client()
    bucket = client.bucket(output_bucket)
    blob = bucket.blob(f"records/{bucket_name}.tf")
    blob.upload_from_string(terraform_config)
    print(f"Terraform file created and uploaded for bucket: {bucket_name}")
