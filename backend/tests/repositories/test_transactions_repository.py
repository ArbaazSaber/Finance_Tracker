"""Tests for Transaction repository functionality."""

import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import datetime

from models.transaction import Transaction, TransactionType
from repositories import transactions_repository
from tests.test_utils import TestDataFactory


class TestTransactionsRepository:
    """Test cases for transactions repository."""
    
    @patch('repositories.transactions_repository.get_connection')
    def test_get_transaction_by_id_success(self, mock_get_connection):
        """Test successfully getting a transaction by ID."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock database result
        mock_row = {
            'transaction_id': 1,
            'transaction_time': datetime.now(),
            'description': 'Test transaction',
            'old_description': None,
            'amount': Decimal('-100.50'),
            'reference_id': 'TXN123',
            'type': 'debit',
            'created_at': datetime.now(),
            'modified_at': None,
            'tag_id': 1,
            'acc_id': 1,
            'user_id': 1
        }
        mock_cursor.fetchone.return_value = mock_row
        
        # Execute
        result = transactions_repository.get_transaction_by_id(1)
        
        # Assertions
        assert result is not None
        assert result.transaction_id == 1
        assert result.reference_id == 'TXN123'
        assert result.amount == Decimal('-100.50')
        
        # Verify database call
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM transactions WHERE transaction_id = %s", (1,)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('repositories.transactions_repository.get_connection')
    def test_get_transaction_by_id_not_found(self, mock_get_connection):
        """Test getting a non-existent transaction."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        # Execute
        result = transactions_repository.get_transaction_by_id(999)
        
        # Assertions
        assert result is None
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM transactions WHERE transaction_id = %s", (999,)
        )
    
    @patch('repositories.transactions_repository.get_connection')
    def test_get_transaction_by_id_database_error(self, mock_get_connection):
        """Test handling database errors when getting transaction."""
        # Setup mock to raise exception
        mock_get_connection.side_effect = Exception("Database error")
        
        # Execute
        result = transactions_repository.get_transaction_by_id(1)
        
        # Assertions
        assert result is None
    
    @patch('repositories.transactions_repository.get_connection')
    def test_get_all_transaction_for_user_success(self, mock_get_connection):
        """Test successfully getting all transactions for a user."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock database results
        mock_rows = [
            {
                'transaction_id': 1,
                'transaction_time': datetime.now(),
                'description': 'Transaction 1',
                'old_description': None,
                'amount': Decimal('-100.50'),
                'reference_id': 'TXN123',
                'type': 'debit',
                'created_at': datetime.now(),
                'modified_at': None,
                'tag_id': 1,
                'acc_id': 1,
                'user_id': 1
            },
            {
                'transaction_id': 2,
                'transaction_time': datetime.now(),
                'description': 'Transaction 2',
                'old_description': None,
                'amount': Decimal('200.00'),
                'reference_id': 'TXN124',
                'type': 'credit',
                'created_at': datetime.now(),
                'modified_at': None,
                'tag_id': 2,
                'acc_id': 1,
                'user_id': 1
            }
        ]
        mock_cursor.fetchall.return_value = mock_rows
        
        # Execute
        result = transactions_repository.get_all_transaction_for_user(1)
        
        # Assertions
        assert len(result) == 2
        assert result[0].transaction_id == 1
        assert result[1].transaction_id == 2
        assert result[0].type == TransactionType.DEBIT
        assert result[1].type == TransactionType.CREDIT
        
        # Verify database call
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM transactions WHERE user_id = %s", (1,)
        )
    
    @patch('repositories.transactions_repository.get_connection')
    def test_insert_transaction_success(self, mock_get_connection):
        """Test successfully inserting a transaction."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [123]  # Returned transaction_id
        
        # Create test transaction
        transaction = TestDataFactory.create_test_transaction()
        
        # Execute
        result = transactions_repository.insert_transaction(transaction)
        
        # Assertions
        assert result == 123
        
        # Verify database calls
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('repositories.transactions_repository.get_connection')
    def test_insert_transaction_database_error(self, mock_get_connection):
        """Test handling database errors when inserting transaction."""
        # Setup mock to raise exception
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")
        
        # Create test transaction
        transaction = TestDataFactory.create_test_transaction()
        
        # Execute
        result = transactions_repository.insert_transaction(transaction)
        
        # Assertions
        assert result is None
        mock_conn.rollback.assert_called_once()
    
    @patch('repositories.transactions_repository.get_connection')
    def test_update_transaction_success(self, mock_get_connection):
        """Test successfully updating a transaction."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1  # One row affected
        
        # Create test transaction
        transaction = TestDataFactory.create_test_transaction()
        
        # Execute
        result = transactions_repository.update_transaction(1, transaction)
        
        # Assertions
        assert result is True
        
        # Verify database calls
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    @patch('repositories.transactions_repository.get_connection')
    def test_update_transaction_not_found(self, mock_get_connection):
        """Test updating a non-existent transaction."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 0  # No rows affected
        
        # Create test transaction
        transaction = TestDataFactory.create_test_transaction()
        
        # Execute
        result = transactions_repository.update_transaction(999, transaction)
        
        # Assertions
        assert result is False
    
    @patch('repositories.transactions_repository.execute_batch')
    @patch('repositories.transactions_repository.get_connection')
    def test_bulk_insert_transactions_success(self, mock_get_connection, mock_execute_batch):
        """Test successfully bulk inserting transactions."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock the returned transaction IDs
        mock_cursor.fetchall.return_value = [(3,), (2,), (1,)]
        
        # Create test transactions
        transactions = [
            TestDataFactory.create_test_transaction(reference_id="TXN123"),
            TestDataFactory.create_test_transaction(reference_id="TXN124"),
            TestDataFactory.create_test_transaction(reference_id="TXN125")
        ]
        
        # Execute
        inserted_ids, errors = transactions_repository.bulk_insert_transactions(transactions)
        
        # Assertions
        assert len(inserted_ids) == 3
        assert inserted_ids == [1, 2, 3]  # Should be reversed
        assert len(errors) == 0
        
        # Verify database calls
        mock_conn.commit.assert_called_once()
    
    @patch('repositories.transactions_repository.execute_batch')
    @patch('repositories.transactions_repository.get_connection')
    def test_bulk_insert_transactions_with_invalid_data(self, mock_get_connection, mock_execute_batch):
        """Test bulk inserting with some invalid transactions."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1,)]
        
        # Create test transactions with one invalid
        transactions = [
            TestDataFactory.create_test_transaction(user_id=1, acc_id=1),
            TestDataFactory.create_test_transaction(user_id=None, acc_id=1),  # Invalid
            TestDataFactory.create_test_transaction(user_id=1, acc_id=None),  # Invalid
        ]
        
        # Execute
        inserted_ids, errors = transactions_repository.bulk_insert_transactions(transactions)
        
        # Assertions
        assert len(inserted_ids) == 1
        assert len(errors) == 2
        assert "Missing required user_id or acc_id" in errors[0]
        assert "Missing required user_id or acc_id" in errors[1]
    
    def test_bulk_insert_transactions_empty_list(self):
        """Test bulk inserting with empty transaction list."""
        # Execute
        inserted_ids, errors = transactions_repository.bulk_insert_transactions([])
        
        # Assertions
        assert len(inserted_ids) == 0
        assert len(errors) == 0