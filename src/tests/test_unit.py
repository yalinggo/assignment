import pytest
from unittest.mock import patch, AsyncMock
from utils.config import DB_HOST, DB_NAME, DB_C_TASK
from utils.connect import Database


@pytest.fixture
def mock_motor_client():
    with patch('motor.motor_asyncio.AsyncIOMotorClient') as mock_client:
        yield mock_client

def test_database_connection(mock_motor_client):
    mock_db = AsyncMock()
    mock_motor_client.return_value = mock_db

    db_instance = Database()
    mock_motor_client.assert_called_once_with(DB_HOST)
    assert db_instance.db == mock_db[DB_NAME]
    assert db_instance.tasks_collection == mock_db[DB_NAME][DB_C_TASK]
