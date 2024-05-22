import json
import os


# Path to the mocked data file
path_tests = os.path.dirname(__file__)
MOCK_DATA_FILE_FUNCTION = os.path.join(path_tests, 'mocks/cloud_function.json')
MOCK_DATA_FILE_GCS = os.path.join(path_tests, 'mocks/gcs_bucket.json')
MOCK_DATA_FILE_PUBSUB_TOPIC = os.path.join(path_tests, 'mocks/pubsub_topic.json')


def mock_data(file):
    with open(file, 'r') as file:
        data = json.load(file)
    return data
