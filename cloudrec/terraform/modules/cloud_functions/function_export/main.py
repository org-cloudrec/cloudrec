import base64
import json

from logging_to_tf import LoggingToTfFactory


def generate_terraform_file(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The event metadata.
    """
    if 'data' in event:
        resource_data = get_json_message(event)

        logging_to_tf = LoggingToTfFactory()
        logging_to_tf.set_resource_data(resource_data)
        logging_to_tf.set_resource_type()
        logging_to_tf.set_resource_fullname()

        resource_instance = logging_to_tf.get_instance()
        resource_name, resource_details = resource_instance.describe()
        resource_instance.set_details(resource_details)
        resource_instance.set_name(resource_name)
        resource_instance.create_tf_file()


def get_json_message(event):
        message = base64.b64decode(event['data']).decode('utf-8')
        json_message = json.loads(message)
        return json_message
