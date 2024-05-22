from cloudrec.terraform.modules.cloud_functions.function_export.logging_to_tf import LoggingToTfFactory
from tests.utils import mock_data, MOCK_DATA_FILE_FUNCTION, MOCK_DATA_FILE_GCS, MOCK_DATA_FILE_PUBSUB_TOPIC


def test_logging_to_tf_function():
    logging_to_tf = LoggingToTfFactory()
    message = mock_data(MOCK_DATA_FILE_FUNCTION)
    logging_to_tf.set_resource_data(message)
    assert logging_to_tf.resource_data == message

    logging_to_tf.set_resource_type()
    assert logging_to_tf.resource_type == "cloud_function"

    logging_to_tf.set_resource_fullname()
    assert logging_to_tf.resource_fullname == "projects/prj-thalesgibbon-56789/locations/us-central1/functions/test-cloudrec-1234567890"


def test_logging_to_tf_gcs():
    logging_to_tf = LoggingToTfFactory()
    message = mock_data(MOCK_DATA_FILE_GCS)
    logging_to_tf.set_resource_data(message)
    assert logging_to_tf.resource_data == message

    logging_to_tf.set_resource_type()
    assert logging_to_tf.resource_type == "gcs_bucket"

    logging_to_tf.set_resource_fullname()
    assert logging_to_tf.resource_fullname == "projects/_/buckets/test-cloudrec-1234567890"


def test_logging_to_tf_pubsub_topic():
    logging_to_tf = LoggingToTfFactory()
    message = mock_data(MOCK_DATA_FILE_PUBSUB_TOPIC)
    logging_to_tf.set_resource_data(message)
    assert logging_to_tf.resource_data == message

    logging_to_tf.set_resource_type()
    assert logging_to_tf.resource_type == "pubsub_topic"

    logging_to_tf.set_resource_fullname()
    assert logging_to_tf.resource_fullname == "projects/prj-thalesgibbon-56789/topics/test-cloudrec-1234567890"
