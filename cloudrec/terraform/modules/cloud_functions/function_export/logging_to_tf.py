from google.cloud import storage, functions_v1, pubsub_v1
import os


# Environment variable for the output bucket
OUTPUT_BUCKET = os.getenv('OUTPUT_BUCKET')


class GeneralResource(object):
    """
    A general class for Google Cloud resources. This class is not meant to be instantiated directly.
    Instead, it serves as a base class for specific Google Cloud resources like GCS buckets, Cloud Functions, and Pub/Sub topics.
    """
    def __init__(self, resource_type: str, resource_fullname: str):
        """
        Initialize a GeneralResource instance.

        :param resource_type: The type of the resource (e.g., 'gcs_bucket', 'cloud_function', 'pubsub_topic').
        :param resource_fullname: The full name of the resource.
        """
        self.resource_type = resource_type
        self.resource_fullname = resource_fullname
        self.resource_name = None
        self.resource_details = None

    def set_name(self, name):
        """
        Set the name of the resource.

        :param name: The name of the resource.
        """
        self.resource_name = name

    def set_details(self, details):
        """
        Set the details of the resource.

        :param details: The details of the resource.
        """
        self.resource_details = details

    def describe(self):
        """
        Describe the resource. This method should be overridden by subclasses.

        :raises NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError

    def create_tf_file(self):
        """
        Create a Terraform file for the resource. This method should be overridden by subclasses.

        :raises NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError

    def write_tf_file(self, content):
        """
        Write a Terraform file to a GCS bucket.

        :param content: The content to write to the Terraform file.
        """
        file_path = f"records/{self.resource_type}/{self.resource_name}.tf"
        client = storage.Client()
        bucket = client.bucket(OUTPUT_BUCKET)
        blob = bucket.blob(file_path)
        blob.upload_from_string(content)
        print(f"File written: {file_path}")


class GcsBucket(GeneralResource):
    """
    A class that represents a Google Cloud Storage (GCS) bucket.
    """
    def __init__(self, resource_fullname: str):
        """
        Initialize a GcsBucket instance.

        :param resource_fullname: The full name of the GCS bucket.
        """
        super().__init__(
            resource_type='gcs_bucket',
            resource_fullname=resource_fullname
        )

    def describe(self):
        """
        Retrieve details about a GCS bucket using the Google Cloud Storage Client.

        :return: A tuple containing the bucket name and the bucket object.
        """
        storage_client = storage.Client()
        bucket_name = self.resource_fullname.split('/')[-1]
        bucket = storage_client.get_bucket(bucket_name)
        return bucket_name, bucket

    def create_tf_file(self):
        """
        Create a Terraform file for the GCS bucket.
        """
        try:
            file_content = f"""
resource "google_storage_bucket" "{self.resource_name}" {{
  name          = "{self.resource_details.name}"
  location      = "{self.resource_details.location}"
  force_destroy = true
  storage_class = "{self.resource_details.storage_class}"
}}
"""
            self.write_tf_file(file_content)
        except Exception as e:
            print(f"Error creating bucket: {e}")


class CloudFunction(GeneralResource):
    """
    A class that represents a Google Cloud Function.
    """
    def __init__(self, resource_fullname: str):
        """
        Initialize a CloudFunction instance.

        :param resource_fullname: The full name of the Cloud Function.
        """
        super().__init__(
            resource_type='cloud_function',
            resource_fullname=resource_fullname
        )

    def describe(self):
        """
        Retrieve details about a Google Cloud Function using the Cloud Functions Client.

        :return: A tuple containing the function name and the function object.
        """
        functions_client = functions_v1.CloudFunctionsServiceClient()
        function_name = self.resource_fullname.split('/')[-1]
        function = functions_client.get_function(name=self.resource_fullname)
        return function_name, function

    def create_tf_file(self):
        """
        Create a Terraform file for the Cloud Function.
        """
        try:
            file_content = f"""
resource "google_cloudfunctions_function" "{self.resource_name}" {{
  name        = "{self.resource_details.name}"
  description = "{self.resource_details.description}"
  runtime     = "{self.resource_details.runtime}"
  entry_point = "{self.resource_details.entry_point}"

  trigger_http = {'true' if self.resource_details.https_trigger else 'false'}
  available_memory_mb = {self.resource_details.available_memory_mb}
}}
"""
            self.write_tf_file(file_content)
        except Exception as e:
            print(f"Error creating bucket: {e}")


class PubsubTopic(GeneralResource):
    """
    A class that represents a Google Cloud Pub/Sub topic.
    """
    def __init__(self, resource_fullname: str):
        """
        Initialize a PubsubTopic instance.

        :param resource_fullname: The full name of the Pub/Sub topic.
        """
        super().__init__(
            resource_type='pubsub_topic',
            resource_fullname=resource_fullname
        )

    def describe(self):
        """
        Retrieve details about a Pub/Sub topic using the resource name from protoPayload.

        :return: A tuple containing the topic name and the topic object.
        """
        publisher = pubsub_v1.PublisherClient()
        topic = publisher.get_topic(topic=self.resource_fullname)
        parts = self.resource_fullname.split('/')
        topic_name = parts[3]
        return topic_name, topic

    def create_tf_file(self):
        """
        Create a Terraform file for the Pub/Sub topic.
        """
        try:
            file_content = f"""
resource "google_pubsub_topic" "{self.resource_name}" {{
  name = "{self.resource_details.name}"
}}
"""
            self.write_tf_file(file_content)
        except Exception as e:
            print(f"Error creating Pub/Sub topic Terraform file: {e}")


class LoggingToTfFactory(object):
    """
    A factory class for creating instances of GeneralResource subclasses based on the resource type.
    """
    def __init__(self):
        """
        Initialize a LoggingToTfFactory instance.
        """
        self.resource_type = None
        self.resource_data = None
        self.resource_fullname = None

    def get_instance(self):
        """
        Get an instance of a GeneralResource subclass based on the resource type.

        :return: An instance of a GeneralResource subclass.
        :raises ValueError: If the resource type is not supported.
        """
        if self.resource_type == 'gcs_bucket':
            return GcsBucket(resource_fullname=self.resource_fullname)
        elif self.resource_type == 'cloud_function':
            return CloudFunction(resource_fullname=self.resource_fullname)
        elif self.resource_type == 'pubsub_topic':
            return PubsubTopic(resource_fullname=self.resource_fullname)
        else:
            raise ValueError(f"Unsupported resource type: {self.resource_type}")

    def set_resource_data(self, resource_data):
        """
        Set the resource data.

        :param resource_data: The resource data.
        """
        self.resource_data = resource_data

    def set_resource_type(self):
        """
        Set the resource type based on the resource data.
        """
        self.resource_type = self.resource_data.get('resource').get('type')

    def set_resource_fullname(self):
        """
        Set the full name of the resource based on the resource data.
        """
        self.resource_fullname = self.resource_data.get('protoPayload').get('resourceName')
