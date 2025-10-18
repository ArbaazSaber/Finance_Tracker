"""Test configuration and fixtures for pytest."""

import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from tests.test_utils import TestDataFactory, MockDatabase


@pytest.fixture(scope="session")
def test_data_factory():
    """Session-scoped fixture providing test data factory."""
    return TestDataFactory


@pytest.fixture
def mock_database():
    """Function-scoped fixture providing mock database."""
    return MockDatabase()


# Add any global test configuration here
pytest_plugins = []