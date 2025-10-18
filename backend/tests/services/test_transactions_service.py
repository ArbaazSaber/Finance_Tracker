"""Tests for Transaction service functionality."""

import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import datetime

from models.transaction import Transaction, TransactionType, BulkTransactionResponse
from services import transactions_service
from tests.test_utils import TestDataFactory


class TestTransactionsService:
    """Test cases for transactions service."""
    
    @patch('services.transactions_service.transactions_repo.get_transaction_by_id')
    def test_fetch_transaction_by_id_success(self, mock_get_transaction):
        """Test successfully fetching a transaction by ID."""
        # Setup mock
        test_transaction = TestDataFactory.create_test_transaction(transaction_id=1)
        mock_get_transaction.return_value = test_transaction
        
        # Execute
        result = transactions_service.fetch_transaction_by_id(1)
        
        # Assertions
        assert result is not None
        assert result.transaction_id == 1
        mock_get_transaction.assert_called_once_with(1)
    
    @patch('services.transactions_service.transactions_repo.get_transaction_by_id')
    def test_fetch_transaction_by_id_invalid_id(self, mock_get_transaction):
        """Test fetching transaction with invalid ID."""
        # Execute
        result = transactions_service.fetch_transaction_by_id(0)
        
        # Assertions
        assert result is None
        mock_get_transaction.assert_not_called()
    
    @patch('services.transactions_service.transactions_repo.get_transaction_by_id')
    def test_fetch_transaction_by_id_not_found(self, mock_get_transaction):
        """Test fetching non-existent transaction."""
        # Setup mock
        mock_get_transaction.return_value = None
        
        # Execute
        result = transactions_service.fetch_transaction_by_id(999)
        
        # Assertions
        assert result is None
        mock_get_transaction.assert_called_once_with(999)
    
    @patch('services.transactions_service.transactions_repo.get_all_transaction_for_user')
    def test_get_all_transaction_for_user_success(self, mock_get_transactions):
        """Test successfully getting all transactions for a user."""
        # Setup mock
        test_transactions = [
            TestDataFactory.create_test_transaction(transaction_id=1, user_id=1),
            TestDataFactory.create_test_transaction(transaction_id=2, user_id=1)
        ]
        mock_get_transactions.return_value = test_transactions
        
        # Execute
        result = transactions_service.get_all_transaction_for_user(1)
        
        # Assertions
        assert len(result) == 2
        assert result[0].user_id == 1
        assert result[1].user_id == 1
        mock_get_transactions.assert_called_once_with(1)
    
    @patch('services.transactions_service.transactions_repo.get_all_transaction_for_user')
    def test_get_all_transaction_for_user_invalid_id(self, mock_get_transactions):
        """Test getting transactions with invalid user ID."""
        # Execute
        result = transactions_service.get_all_transaction_for_user(0)
        
        # Assertions
        assert result == []
        mock_get_transactions.assert_not_called()
    
    def test_validate_transaction_amount_sign_valid_debit(self):
        """Test amount sign validation for valid debit transaction."""
        # Create valid debit transaction
        transaction = TestDataFactory.create_test_transaction(
            amount=Decimal("-100.50"), 
            type=TransactionType.DEBIT
        )
        
        # Execute
        result = transactions_service._validate_transaction_amount_sign(transaction)
        
        # Assertions
        assert result is True
    
    def test_validate_transaction_amount_sign_valid_credit(self):
        """Test amount sign validation for valid credit transaction."""
        # Create valid credit transaction
        transaction = TestDataFactory.create_test_transaction(
            amount=Decimal("100.50"), 
            type=TransactionType.CREDIT
        )
        
        # Execute
        result = transactions_service._validate_transaction_amount_sign(transaction)
        
        # Assertions
        assert result is True
    
    def test_validate_transaction_amount_sign_invalid_debit(self):
        """Test amount sign validation for invalid debit transaction."""
        # Create invalid debit transaction (positive amount)
        transaction = TestDataFactory.create_test_transaction(
            amount=Decimal("100.50"), 
            type=TransactionType.DEBIT
        )
        
        # Execute
        result = transactions_service._validate_transaction_amount_sign(transaction)
        
        # Assertions
        assert result is False
    
    def test_validate_transaction_amount_sign_invalid_credit(self):
        """Test amount sign validation for invalid credit transaction."""
        # Create invalid credit transaction (negative amount)
        transaction = TestDataFactory.create_test_transaction(
            amount=Decimal("-100.50"), 
            type=TransactionType.CREDIT
        )
        
        # Execute
        result = transactions_service._validate_transaction_amount_sign(transaction)
        
        # Assertions
        assert result is False
    
    @patch('services.transactions_service.transactions_repo.insert_transaction')
    def test_add_transaction_success(self, mock_insert_transaction):
        """Test successfully adding a transaction."""
        # Setup mock
        mock_insert_transaction.return_value = 123
        
        # Create valid transaction
        transaction = TestDataFactory.create_test_transaction(
            amount=Decimal("-100.50"), 
            type=TransactionType.DEBIT,
            user_id=1,
            acc_id=1
        )
        
        # Execute
        result = transactions_service.add_transaction(transaction)
        
        # Assertions
        assert result == 123
        mock_insert_transaction.assert_called_once_with(transaction)
    
    @patch('services.transactions_service.transactions_repo.insert_transaction')
    def test_add_transaction_missing_required_fields(self, mock_insert_transaction):
        """Test adding transaction with missing required fields."""
        # Create transaction with missing user_id
        transaction = TestDataFactory.create_test_transaction(user_id=None)
        
        # Execute
        result = transactions_service.add_transaction(transaction)
        
        # Assertions
        assert result is None
        mock_insert_transaction.assert_not_called()
    
    @patch('services.transactions_service.transactions_repo.insert_transaction')
    def test_add_transaction_invalid_amount_sign(self, mock_insert_transaction):
        """Test adding transaction with invalid amount sign."""
        # Create debit transaction with positive amount
        transaction = TestDataFactory.create_test_transaction(
            amount=Decimal("100.50"), 
            type=TransactionType.DEBIT,
            user_id=1,
            acc_id=1
        )
        
        # Execute
        result = transactions_service.add_transaction(transaction)
        
        # Assertions
        assert result is None
        mock_insert_transaction.assert_not_called()
    
    @patch('services.transactions_service.transactions_repo.get_transaction_by_id')
    @patch('services.transactions_service.transactions_repo.update_transaction')
    def test_modify_transaction_success(self, mock_update_transaction, mock_get_transaction):
        """Test successfully modifying a transaction."""
        # Setup mocks
        existing_transaction = TestDataFactory.create_test_transaction(
            transaction_id=1,
            description="Original description",
            amount=Decimal("-100.50")
        )
        mock_get_transaction.return_value = existing_transaction
        mock_update_transaction.return_value = True
        
        # Create update data
        update_data = TestDataFactory.create_test_transaction(
            description="Updated description",
            amount=Decimal("-200.00")
        )
        
        # Execute
        result = transactions_service.modify_transaction(1, update_data)
        
        # Assertions
        assert result is True
        mock_get_transaction.assert_called_once_with(1)
        mock_update_transaction.assert_called_once()
    
    @patch('services.transactions_service.transactions_repo.get_transaction_by_id')
    def test_modify_transaction_not_found(self, mock_get_transaction):
        """Test modifying non-existent transaction."""
        # Setup mock
        mock_get_transaction.return_value = None
        
        # Create update data
        update_data = TestDataFactory.create_test_transaction()
        
        # Execute
        result = transactions_service.modify_transaction(999, update_data)
        
        # Assertions
        assert result is False
        mock_get_transaction.assert_called_once_with(999)
    
    def test_modify_transaction_invalid_id(self):
        """Test modifying transaction with invalid ID."""
        # Create update data
        update_data = TestDataFactory.create_test_transaction()
        
        # Execute
        result = transactions_service.modify_transaction(0, update_data)
        
        # Assertions
        assert result is False
    
    @patch('services.transactions_service.transactions_repo.bulk_insert_transactions')
    def test_bulk_add_transactions_success(self, mock_bulk_insert):
        """Test successfully bulk adding transactions."""
        # Setup mock
        mock_bulk_insert.return_value = ([1, 2, 3], [])
        
        # Create valid transactions
        transactions = [
            TestDataFactory.create_test_transaction(
                reference_id="TXN123",
                amount=Decimal("-100.50"), 
                type=TransactionType.DEBIT,
                user_id=1,
                acc_id=1
            ),
            TestDataFactory.create_test_transaction(
                reference_id="TXN124",
                amount=Decimal("200.00"), 
                type=TransactionType.CREDIT,
                user_id=1,
                acc_id=1
            ),
            TestDataFactory.create_test_transaction(
                reference_id="TXN125",
                amount=Decimal("-50.00"), 
                type=TransactionType.DEBIT,
                user_id=1,
                acc_id=1
            )
        ]
        
        # Execute
        result = transactions_service.bulk_add_transactions(transactions)
        
        # Assertions
        assert isinstance(result, BulkTransactionResponse)
        assert result.success_count == 3
        assert result.failure_count == 0
        assert result.total_processed == 3
        assert result.inserted_ids == [1, 2, 3]
        assert result.errors is None
        mock_bulk_insert.assert_called_once()
    
    @patch('services.transactions_service.transactions_repo.bulk_insert_transactions')
    def test_bulk_add_transactions_with_validation_errors(self, mock_bulk_insert):
        """Test bulk adding transactions with validation errors."""
        # Setup mock
        mock_bulk_insert.return_value = ([1], [])
        
        # Create transactions with validation issues
        transactions = [
            TestDataFactory.create_test_transaction(
                reference_id="TXN123",
                amount=Decimal("-100.50"), 
                type=TransactionType.DEBIT,
                user_id=1,
                acc_id=1
            ),
            TestDataFactory.create_test_transaction(
                reference_id="TXN124",
                amount=Decimal("100.50"),  # Invalid - positive amount for debit
                type=TransactionType.DEBIT,
                user_id=1,
                acc_id=1
            ),
            TestDataFactory.create_test_transaction(
                reference_id="TXN125",  # Valid reference_id but will fail validation due to amount/type mismatch
                amount=Decimal("-100.50"),  # Invalid - negative amount for credit
                type=TransactionType.CREDIT,
                user_id=1,
                acc_id=1
            )
        ]
        
        # Execute
        result = transactions_service.bulk_add_transactions(transactions)
        
        # Assertions
        assert isinstance(result, BulkTransactionResponse)
        assert result.success_count == 1
        assert result.failure_count == 2
        assert result.total_processed == 3
        assert len(result.errors) >= 2  # Should have validation errors
    
    def test_bulk_add_transactions_empty_list(self):
        """Test bulk adding with empty transaction list."""
        # Execute
        result = transactions_service.bulk_add_transactions([])
        
        # Assertions
        assert isinstance(result, BulkTransactionResponse)
        assert result.success_count == 0
        assert result.failure_count == 0
        assert result.total_processed == 0
        assert result.inserted_ids == []
        assert "No transactions provided" in result.errors[0]
    
    @patch('services.transactions_service.transactions_repo.bulk_insert_transactions')
    def test_bulk_add_transactions_all_invalid(self, mock_bulk_insert):
        """Test bulk adding where all transactions are invalid."""
        # Create invalid transactions
        transactions = [
            TestDataFactory.create_test_transaction(user_id=None),  # Missing user_id
            TestDataFactory.create_test_transaction(acc_id=None),   # Missing acc_id
        ]
        
        # Execute
        result = transactions_service.bulk_add_transactions(transactions)
        
        # Assertions
        assert isinstance(result, BulkTransactionResponse)
        assert result.success_count == 0
        assert result.failure_count == 2
        assert result.total_processed == 2
        assert len(result.errors) == 2
        mock_bulk_insert.assert_not_called()  # Should not call repo if no valid transactions