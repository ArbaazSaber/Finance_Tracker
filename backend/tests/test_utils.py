"""Test utilities and fixtures for Finance Tracker tests."""

import pytest
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any
from unittest.mock import MagicMock

from models.user import User, UserCreate
from models.bank import Bank
from models.account import Account
from models.category import Category
from models.tag import Tag
from models.transaction import Transaction, TransactionType
from models.category_target import CategoryTarget
from models.tag_rule import TaggingRule

class TestDataFactory:
    """Factory class for creating test data objects."""
    
    @staticmethod
    def create_test_user(user_id: int = 1, **overrides) -> User:
        """Create a test user with default values."""
        defaults = {
            "user_id": user_id,
            "username": f"testuser{user_id}",
            "email": f"test{user_id}@example.com",
            "password_hash": "hashed_password_123",
            "created_at": datetime.now(),
            "is_active": True
        }
        defaults.update(overrides)
        return User(**defaults)
    
    @staticmethod
    def create_test_user_create(**overrides) -> UserCreate:
        """Create a test user creation request."""
        defaults = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
        defaults.update(overrides)
        return UserCreate(**defaults)
    
    @staticmethod
    def create_test_bank(bank_id: int = 1, **overrides) -> Bank:
        """Create a test bank with default values."""
        defaults = {
            "bank_id": bank_id,
            "bank_name": f"Test Bank {bank_id}"
        }
        defaults.update(overrides)
        return Bank(**defaults)
    
    @staticmethod
    def create_test_account(acc_id: int = 1, **overrides) -> Account:
        """Create a test account with default values."""
        defaults = {
            "acc_id": acc_id,
            "acc_name": f"Test Account {acc_id}",
            "user_id": 1,
            "bank_id": 1,
            "is_active": True
        }
        defaults.update(overrides)
        return Account(**defaults)
    
    @staticmethod
    def create_test_category(category_id: int = 1, **overrides) -> Category:
        """Create a test category with default values."""
        defaults = {
            "category_id": category_id,
            "category_name": f"Test Category {category_id}"
        }
        defaults.update(overrides)
        return Category(**defaults)
    
    @staticmethod
    def create_test_tag(tag_id: int = 1, **overrides) -> Tag:
        """Create a test tag with default values."""
        defaults = {
            "tag_id": tag_id,
            "tag_name": f"Test Tag {tag_id}",
            "category_id": 1
        }
        defaults.update(overrides)
        return Tag(**defaults)
    
    @staticmethod
    def create_test_transaction(transaction_id: int = None, **overrides) -> Transaction:
        """Create a test transaction with default values."""
        defaults = {
            "transaction_id": transaction_id,
            "transaction_time": datetime.now(),
            "description": "Test transaction",
            "amount": Decimal("-100.50"),
            "reference_id": f"TXN{transaction_id or '123'}",
            "type": TransactionType.DEBIT,
            "acc_id": 1,
            "user_id": 1,
            "tag_id": 1
        }
        defaults.update(overrides)
        return Transaction(**defaults)
    
    @staticmethod
    def create_test_category_target(target_id: int = 1, **overrides) -> CategoryTarget:
        """Create a test category target with default values."""
        defaults = {
            "target_id": target_id,
            "percentage": 25.0,
            "start_date": datetime.now(),
            "category_id": 1,
            "user_id": 1
        }
        defaults.update(overrides)
        return CategoryTarget(**defaults)
    
    @staticmethod
    def create_test_tag_rule(rule_id: int = 1, **overrides) -> TaggingRule:
        """Create a test tagging rule with default values."""
        defaults = {
            "rule_id": rule_id,
            "keyword": f"test_keyword_{rule_id}",
            "tag_id": 1
        }
        defaults.update(overrides)
        return TaggingRule(**defaults)

class MockDatabase:
    """Mock database for testing repositories."""
    
    def __init__(self):
        self.connection = MagicMock()
        self.cursor = MagicMock()
        self.connection.cursor.return_value = self.cursor
        
    def setup_fetchone_result(self, result: Dict[str, Any] = None):
        """Setup mock to return specific result for fetchone."""
        self.cursor.fetchone.return_value = result
        
    def setup_fetchall_result(self, results: list = None):
        """Setup mock to return specific results for fetchall."""
        self.cursor.fetchall.return_value = results or []
        
    def setup_execute_result(self, return_id: int = None):
        """Setup mock for execute operations that return IDs."""
        if return_id:
            self.cursor.fetchone.return_value = [return_id]
        self.cursor.rowcount = 1
        
    def verify_execute_called_with(self, query: str, params: tuple = None):
        """Verify that execute was called with specific query and params."""
        if params:
            self.cursor.execute.assert_called_with(query, params)
        else:
            self.cursor.execute.assert_called_with(query)

@pytest.fixture
def mock_db():
    """Fixture providing a mock database."""
    return MockDatabase()

@pytest.fixture
def test_data():
    """Fixture providing test data factory."""
    return TestDataFactory()