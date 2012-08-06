import os

# Fixture folder name
FIXTURE_FOLDER_NAME = 'fixtures'

# Path to fixture folder
FIXTURE_FOLDER_PATH = os.path.join(
    os.path.dirname(__file__), FIXTURE_FOLDER_NAME)

# Default image used for testing
DEFAULT_IMAGE_PATH = '%s/dummy1.jpg' % FIXTURE_FOLDER_PATH
