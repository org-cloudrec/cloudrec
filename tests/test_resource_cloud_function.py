from cloudrec.terraform.modules.cloud_functions.function_export.logging_to_tf import LoggingToTfFactory
from tests.utils import mock_data, MOCK_DATA_FILE_FUNCTION


def test_logging_to_tf_function():
    message = mock_data(MOCK_DATA_FILE_FUNCTION)

    logging_to_tf = LoggingToTfFactory()
    logging_to_tf.set_resource_data(message)
    logging_to_tf.set_resource_type()
    logging_to_tf.set_resource_fullname()

    resource_instance = logging_to_tf.get_instance()
    resource_name, resource_details = resource_instance.describe()

    resource_instance.set_details(resource_details)
    assert resource_instance.resource_details == resource_details

    resource_instance.set_name(resource_name)
    assert resource_instance.resource_name == resource_name
