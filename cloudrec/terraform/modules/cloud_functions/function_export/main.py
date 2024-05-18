from google.cloud import storage, functions_v1
import base64
import json
import os


def generate_terraform_file(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The event metadata.
    """
    if 'data' in event:
        resource_data = get_json_message(event)

        resource_type = get_resource_type(resource_data)
        resource_name = get_resource_name(resource_data)

        if resource_type == 'gcs_bucket':
            bucket_name, bucket_details = describe_bucket(resource_name)
            create_bucket_tf(bucket_name, bucket_details, resource_type)
        elif resource_type == 'cloud_function':
            function_name, function_details = describe_function(resource_name)
            create_function_tf(function_name, function_details, resource_type)
        else:
            print(f"Unsupported resource type: {resource_type}")


def get_json_message(event):
        message = base64.b64decode(event['data']).decode('utf-8')
        json_message = json.loads(message)
        return json_message


def get_resource_type(json_message):
    return json_message.get('resource').get('type')


def get_resource_name(json_message):
    return json_message.get('protoPayload').get('resourceName')


def describe_bucket(resource_name):
    """Retrieve details about a GCS bucket using the Google Cloud Storage Client."""
    storage_client = storage.Client()
    bucket_name = resource_name.split('/')[-1]
    bucket = storage_client.get_bucket(bucket_name)
    return bucket_name, bucket


def describe_function(resource_name):
    """Retrieve details about a Google Cloud Function using the Cloud Functions Client."""
    functions_client = functions_v1.CloudFunctionsServiceClient()
    function_name = resource_name.split('/')[-1]
    function = functions_client.get_function(name=resource_name)
    return function_name, function


def create_bucket_tf(name, properties, resource_type):
    try:
        file_content = f"""
resource "google_storage_bucket" "{name}" {{
  name          = "{properties.name}"
  location      = "{properties.location}"
  force_destroy = true
  storage_class = "{properties.storage_class}"
}}
"""
        write_tf_file(name, resource_type, file_content)
    except Exception as e:
        print(f"Error creating bucket: {e}")


def create_function_tf(name, properties, resource_type):
    try:
        file_content = f"""
resource "google_cloudfunctions_function" "{name}" {{
  name        = "{properties.name}"
  description = "{properties.description}"
  runtime     = "{properties.runtime}"
  entry_point = "{properties.entry_point}"

  trigger_http = {'true' if properties.https_trigger else 'false'}
  available_memory_mb = {properties.available_memory_mb}
}}
"""
        write_tf_file(name, resource_type, file_content)
    except Exception as e:
        print(f"Error creating bucket: {e}")


def write_tf_file(name, resource, content):
    output_bucket = os.getenv('OUTPUT_BUCKET')
    file_path = f"records/{resource}/{name}.tf"
    client = storage.Client()
    bucket = client.bucket(output_bucket)
    blob = bucket.blob(file_path)
    blob.upload_from_string(content)
    print(f"File written: {file_path}")
