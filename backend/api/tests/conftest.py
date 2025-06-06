import os
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


# @pytest.fixture
# def mock_dynamoDB_table():
#     with patch("api.runtime.resources.get_table") as mock_get_table:
#         mock_table_instance = MagicMock()
#         mock_get_table.return_value = mock_table_instance
#         yield mock_table_instance