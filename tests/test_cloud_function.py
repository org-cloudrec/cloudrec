import json
import pytest

# Import the function to test
from cloudrec.terraform.modules.cloud_functions.function_export.main import get_resource_type, get_resource_name, describe_function, describe_bucket

# Path to the mocked data file
MOCK_DATA_FILE_FUNCTION = 'tests/mocks/cloud_function.json'
MOCK_DATA_FILE_GCS = 'tests/mocks/gcs_bucket.json'


# Load mock data from the JSON file
@pytest.fixture(scope='module')
def mock_data(file):
    with open(file, 'r') as file:
        data = json.load(file)
    return data


def test_example_function_with_name(mock_data):
    message = mock_data(MOCK_DATA_FILE_FUNCTION)
    assert get_resource_type(message) == "cloud_function"
    resource_name = get_resource_name(message)
    assert describe_function(resource_name)


def test_example_gcs_with_name(mock_data):
    message = mock_data(MOCK_DATA_FILE_GCS)
    assert get_resource_type(message) == "gcs_bucket"
    resource_name = get_resource_name(message)
    assert describe_bucket(resource_name)
