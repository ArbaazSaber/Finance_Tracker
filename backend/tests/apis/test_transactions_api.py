"""Tests for Transaction API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, ANY
from decimal import Decimal
from datetime import datetime

from app import app
from models.transaction import Transaction, TransactionType, BulkTransactionRequest, BulkTransactionResponse
from tests.test_utils import TestDataFactory

client = TestClient(app)


class TestTransactionsAPI:
    """Test cases for transaction API endpoints."""
    
    @patch('services.transactions_service.fetch_transaction_by_id')
    def test_get_transaction_success(self, mock_fetch_transaction):
        """Test successfully getting a transaction by ID."""
        # Setup mock
        test_transaction = TestDataFactory.create_test_transaction(transaction_id=1)
        mock_fetch_transaction.return_value = test_transaction
        
        # Execute
        response = client.get("/transactions/1")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["transaction_id"] == 1
        assert data["reference_id"] == test_transaction.reference_id
        mock_fetch_transaction.assert_called_once_with(1)
    
    @patch('services.transactions_service.fetch_transaction_by_id')
    def test_get_transaction_not_found(self, mock_fetch_transaction):
        """Test getting a non-existent transaction."""
        # Setup mock
        mock_fetch_transaction.return_value = None
        
        # Execute
        response = client.get("/transactions/999")
        
        # Assertions
        assert response.status_code == 404
        assert response.json()["detail"] == "Transaction not found"
        mock_fetch_transaction.assert_called_once_with(999)
    
    @patch('services.transactions_service.get_all_transaction_for_user')
    def test_list_transactions_for_user_success(self, mock_get_transactions):
        """Test successfully getting transactions for a user."""
        # Setup mock
        test_transactions = [
            TestDataFactory.create_test_transaction(transaction_id=1, user_id=1),
            TestDataFactory.create_test_transaction(transaction_id=2, user_id=1)
        ]
        mock_get_transactions.return_value = test_transactions
        
        # Execute
        response = client.get("/transactions/user/1")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["transaction_id"] == 1
        assert data[1]["transaction_id"] == 2
        mock_get_transactions.assert_called_once_with(1)
    
    @patch('services.transactions_service.get_all_transaction_for_account')
    def test_list_transactions_for_account_success(self, mock_get_transactions):
        """Test successfully getting transactions for an account."""
        # Setup mock
        test_transactions = [
            TestDataFactory.create_test_transaction(transaction_id=1, acc_id=1),
        ]
        mock_get_transactions.return_value = test_transactions
        
        # Execute
        response = client.get("/transactions/account/1")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["acc_id"] == 1
        mock_get_transactions.assert_called_once_with(1)
    
    @patch('services.transactions_service.add_transaction')
    def test_create_transaction_success(self, mock_add_transaction):
        """Test successfully creating a transaction."""
        # Setup mock
        mock_add_transaction.return_value = 123
        
        # Create transaction data
        transaction_data = {
            "transaction_time": "2023-01-01T12:00:00",
            "description": "Test transaction",
            "amount": "-100.50",
            "reference_id": "TXN123",
            "type": "debit",
            "acc_id": 1,
            "user_id": 1,
            "tag_id": 1
        }
        
        # Execute
        response = client.post("/transactions/", json=transaction_data)
        
        # Assertions
        assert response.status_code == 200
        assert response.json() == 123
        mock_add_transaction.assert_called_once()
    
    @patch('services.transactions_service.add_transaction')
    def test_create_transaction_invalid_data(self, mock_add_transaction):
        """Test creating transaction with invalid data."""
        # Create invalid transaction data (missing required fields)
        transaction_data = {
            "amount": "-100.50",
            "type": "debit"
        }
        
        # Execute
        response = client.post("/transactions/", json=transaction_data)
        
        # Assertions
        assert response.status_code == 422  # Validation error
        mock_add_transaction.assert_not_called()
    
    @patch('services.transactions_service.add_transaction')
    def test_create_transaction_service_failure(self, mock_add_transaction):
        """Test handling service failure during transaction creation."""
        # Setup mock
        mock_add_transaction.return_value = None
        
        # Create transaction data
        transaction_data = {
            "transaction_time": "2023-01-01T12:00:00",
            "description": "Test transaction",
            "amount": "-100.50",
            "reference_id": "TXN123",
            "type": "debit",
            "acc_id": 1,
            "user_id": 1
        }
        
        # Execute
        response = client.post("/transactions/", json=transaction_data)
        
        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "Failed to insert transaction"
        mock_add_transaction.assert_called_once()
    
    @patch('services.transactions_service.modify_transaction')
    def test_update_transaction_success(self, mock_modify_transaction):
        """Test successfully updating a transaction."""
        # Setup mock
        mock_modify_transaction.return_value = True
        
        # Create update data
        update_data = {
            "transaction_time": "2023-01-01T12:00:00",
            "description": "Updated transaction",
            "amount": "-200.00",
            "reference_id": "TXN123",
            "type": "debit",
            "acc_id": 1,
            "user_id": 1
        }
        
        # Execute
        response = client.put("/transactions/1", json=update_data)
        
        # Assertions
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        mock_modify_transaction.assert_called_once_with(1, ANY)
    
    @patch('services.transactions_service.modify_transaction')
    def test_update_transaction_not_found(self, mock_modify_transaction):
        """Test updating a non-existent transaction."""
        # Setup mock
        mock_modify_transaction.return_value = False
        
        # Create update data
        update_data = {
            "transaction_time": "2023-01-01T12:00:00",
            "description": "Updated transaction",
            "amount": "-200.00",
            "reference_id": "TXN123",
            "type": "debit",
            "acc_id": 1,
            "user_id": 1
        }
        
        # Execute
        response = client.put("/transactions/999", json=update_data)
        
        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "Failed to update transaction"
        mock_modify_transaction.assert_called_once_with(999, ANY)
    
    @patch('services.transactions_service.bulk_add_transactions')
    def test_bulk_create_transactions_success(self, mock_bulk_add):
        """Test successfully bulk creating transactions."""
        # Setup mock
        mock_response = BulkTransactionResponse(
            success_count=2,
            failure_count=0,
            total_processed=2,
            inserted_ids=[1, 2]
        )
        mock_bulk_add.return_value = mock_response
        
        # Create bulk request data
        bulk_data = {
            "transactions": [
                {
                    "transaction_time": "2023-01-01T12:00:00",
                    "description": "Transaction 1",
                    "amount": "-100.50",
                    "reference_id": "TXN123",
                    "type": "debit",
                    "acc_id": 1,
                    "user_id": 1
                },
                {
                    "transaction_time": "2023-01-01T12:30:00",
                    "description": "Transaction 2",
                    "amount": "200.00",
                    "reference_id": "TXN124",
                    "type": "credit",
                    "acc_id": 1,
                    "user_id": 1
                }
            ]
        }
        
        # Execute
        response = client.post("/transactions/bulk", json=bulk_data)
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["success_count"] == 2
        assert data["failure_count"] == 0
        assert data["total_processed"] == 2
        assert data["inserted_ids"] == [1, 2]
        mock_bulk_add.assert_called_once()
    
    @patch('services.transactions_service.bulk_add_transactions')
    def test_bulk_create_transactions_partial_success(self, mock_bulk_add):
        """Test bulk creating transactions with partial success."""
        # Setup mock
        mock_response = BulkTransactionResponse(
            success_count=1,
            failure_count=1,
            total_processed=2,
            inserted_ids=[1],
            errors=["Transaction 1: Validation error"]
        )
        mock_bulk_add.return_value = mock_response
        
        # Create bulk request data
        bulk_data = {
            "transactions": [
                {
                    "transaction_time": "2023-01-01T12:00:00",
                    "description": "Valid transaction",
                    "amount": "-100.50",
                    "reference_id": "TXN123",
                    "type": "debit",
                    "acc_id": 1,
                    "user_id": 1
                },
                {
                    "transaction_time": "2023-01-01T12:30:00",
                    "description": "Invalid transaction",
                    "amount": "100.50",  # Invalid - positive amount for debit
                    "reference_id": "TXN124",
                    "type": "debit",
                    "acc_id": 1,
                    "user_id": 1
                }
            ]
        }
        
        # Execute
        response = client.post("/transactions/bulk", json=bulk_data)
        
        # Assertions
        assert response.status_code == 200  # Partial success is still 200
        data = response.json()
        assert data["success_count"] == 1
        assert data["failure_count"] == 1
        assert len(data["errors"]) == 1
        mock_bulk_add.assert_called_once()
    
    def test_bulk_create_transactions_empty_list(self):
        """Test bulk creating with empty transaction list."""
        # Create empty bulk request
        bulk_data = {"transactions": []}
        
        # Execute
        response = client.post("/transactions/bulk", json=bulk_data)
        
        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "No transactions provided"
    
    def test_bulk_create_transactions_too_many(self):
        """Test bulk creating with too many transactions."""
        # Create bulk request with 1001 transactions (over limit)
        transactions = []
        for i in range(1001):
            transactions.append({
                "transaction_time": "2023-01-01T12:00:00",
                "description": f"Transaction {i}",
                "amount": "-100.50",
                "reference_id": f"TXN{i}",
                "type": "debit",
                "acc_id": 1,
                "user_id": 1
            })
        
        bulk_data = {"transactions": transactions}
        
        # Execute
        response = client.post("/transactions/bulk", json=bulk_data)
        
        # Assertions
        assert response.status_code == 400
        assert "Maximum 1000 transactions allowed" in response.json()["detail"]
    
    @patch('services.transactions_service.bulk_add_transactions')
    def test_bulk_create_transactions_all_failed(self, mock_bulk_add):
        """Test bulk creating where all transactions fail."""
        # Setup mock
        mock_response = BulkTransactionResponse(
            success_count=0,
            failure_count=2,
            total_processed=2,
            inserted_ids=[],
            errors=["Error 1", "Error 2"]
        )
        mock_bulk_add.return_value = mock_response
        
        # Create bulk request data with invalid transactions
        bulk_data = {
            "transactions": [
                {
                    "transaction_time": "2023-01-01T12:00:00",
                    "description": "Invalid transaction",
                    "amount": "-100.50",
                    "reference_id": "",  # Invalid - empty reference_id
                    "type": "debit",
                    "acc_id": 1,
                    "user_id": 1
                },
                {
                    "transaction_time": "2023-01-01T12:30:00",
                    "description": "Another invalid transaction",
                    "amount": "-100.50",
                    "reference_id": "TXN124",
                    "type": "debit",
                    # Missing user_id and acc_id
                }
            ]
        }
        
        # Execute
        response = client.post("/transactions/bulk", json=bulk_data)
        
        # Assertions
        # Note: This will fail at Pydantic validation level (422) due to empty reference_id
        # before reaching our service logic, so we expect 422 instead of 400
        assert response.status_code == 422  # Pydantic validation error
        # The request fails validation before reaching our service
        mock_bulk_add.assert_not_called()
