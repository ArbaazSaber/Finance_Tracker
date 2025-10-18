"""Tests for Transaction model validation and functionality."""

import pytest
from datetime import datetime
from decimal import Decimal
from pydantic import ValidationError

from models.transaction import Transaction, TransactionType, TransactionUpsert, BulkTransactionRequest, BulkTransactionResponse


class TestTransactionTypeEnum:
    """Test cases for TransactionType enum."""
    
    def test_transaction_type_values(self):
        """Test that transaction type enum has correct values."""
        assert TransactionType.DEBIT.value == "debit"
        assert TransactionType.CREDIT.value == "credit"
    
    def test_transaction_type_string_comparison(self):
        """Test that enum can be compared to strings."""
        assert TransactionType.DEBIT == "debit"
        assert TransactionType.CREDIT == "credit"


class TestTransactionModel:
    """Test cases for Transaction model."""
    
    def test_valid_debit_transaction(self):
        """Test creating a valid debit transaction."""
        transaction = Transaction(
            transaction_time=datetime.now(),
            description="Test purchase",
            amount=Decimal("-100.50"),
            reference_id="TXN123",
            type=TransactionType.DEBIT,
            acc_id=1,
            user_id=1
        )
        
        assert transaction.amount == Decimal("-100.50")
        assert transaction.type == TransactionType.DEBIT
        assert transaction.reference_id == "TXN123"
        assert transaction.acc_id == 1
        assert transaction.user_id == 1
    
    def test_valid_credit_transaction(self):
        """Test creating a valid credit transaction."""
        transaction = Transaction(
            transaction_time=datetime.now(),
            description="Test deposit",
            amount=Decimal("500.00"),
            reference_id="TXN124",
            type=TransactionType.CREDIT,
            acc_id=1,
            user_id=1
        )
        
        assert transaction.amount == Decimal("500.00")
        assert transaction.type == TransactionType.CREDIT
        assert transaction.reference_id == "TXN124"
    
    def test_transaction_with_optional_fields(self):
        """Test transaction with optional fields."""
        transaction = Transaction(
            transaction_time=datetime.now(),
            description="Test transaction",
            old_description="Original description",
            amount=Decimal("-50.00"),
            reference_id="TXN125",
            type=TransactionType.DEBIT,
            tag_id=1,
            acc_id=1,
            user_id=1
        )
        
        assert transaction.old_description == "Original description"
        assert transaction.tag_id == 1
    
    def test_transaction_missing_reference_id_fails(self):
        """Test that missing reference_id fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            Transaction(
                transaction_time=datetime.now(),
                amount=Decimal("-100.50"),
                type=TransactionType.DEBIT,
                acc_id=1,
                user_id=1
            )
        
        assert "reference_id" in str(exc_info.value)
    
    def test_transaction_empty_reference_id_fails(self):
        """Test that empty reference_id fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            Transaction(
                transaction_time=datetime.now(),
                amount=Decimal("-100.50"),
                reference_id="",
                type=TransactionType.DEBIT,
                acc_id=1,
                user_id=1
            )
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_transaction_missing_required_fields_fails(self):
        """Test that missing required fields fail validation."""
        with pytest.raises(ValidationError):
            Transaction(amount=Decimal("-100.50"))
    
    def test_transaction_validation_function(self):
        """Test the validate_amount_sign method."""
        # Valid debit transaction
        debit_transaction = Transaction(
            transaction_time=datetime.now(),
            amount=Decimal("-100.50"),
            reference_id="TXN123",
            type=TransactionType.DEBIT,
            acc_id=1,
            user_id=1
        )
        
        # Should not raise exception
        validated = debit_transaction.validate_amount_sign()
        assert validated == debit_transaction
        
        # Valid credit transaction
        credit_transaction = Transaction(
            transaction_time=datetime.now(),
            amount=Decimal("100.50"),
            reference_id="TXN124",
            type=TransactionType.CREDIT,
            acc_id=1,
            user_id=1
        )
        
        # Should not raise exception
        validated = credit_transaction.validate_amount_sign()
        assert validated == credit_transaction
    
    def test_invalid_debit_amount_validation(self):
        """Test validation fails for positive debit amount."""
        transaction = Transaction(
            transaction_time=datetime.now(),
            amount=Decimal("100.50"),  # Positive amount for debit
            reference_id="TXN123",
            type=TransactionType.DEBIT,
            acc_id=1,
            user_id=1
        )
        
        with pytest.raises(ValueError) as exc_info:
            transaction.validate_amount_sign()
        
        assert "Debit transactions must have negative amounts" in str(exc_info.value)
    
    def test_invalid_credit_amount_validation(self):
        """Test validation fails for non-positive credit amount."""
        transaction = Transaction(
            transaction_time=datetime.now(),
            amount=Decimal("-100.50"),  # Negative amount for credit
            reference_id="TXN124",
            type=TransactionType.CREDIT,
            acc_id=1,
            user_id=1
        )
        
        with pytest.raises(ValueError) as exc_info:
            transaction.validate_amount_sign()
        
        assert "Credit transactions must have positive amounts" in str(exc_info.value)


class TestTransactionUpsertModel:
    """Test cases for TransactionUpsert model."""
    
    def test_valid_transaction_upsert(self):
        """Test creating a valid transaction upsert."""
        upsert = TransactionUpsert(
            description="Updated description",
            amount=Decimal("-200.00"),
            type=TransactionType.DEBIT
        )
        
        assert upsert.description == "Updated description"
        assert upsert.amount == Decimal("-200.00")
        assert upsert.type == TransactionType.DEBIT
    
    def test_transaction_upsert_all_optional(self):
        """Test that all fields are optional in upsert."""
        upsert = TransactionUpsert()
        
        assert upsert.transaction_time is None
        assert upsert.description is None
        assert upsert.amount is None
        assert upsert.reference_id is None
        assert upsert.type is None
    
    def test_transaction_upsert_empty_reference_id_fails(self):
        """Test that empty reference_id fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            TransactionUpsert(reference_id="")
        
        assert "String should have at least 1 character" in str(exc_info.value)


class TestBulkTransactionRequest:
    """Test cases for BulkTransactionRequest model."""
    
    def test_valid_bulk_request(self):
        """Test creating a valid bulk transaction request."""
        transactions = [
            Transaction(
                transaction_time=datetime.now(),
                amount=Decimal("-100.50"),
                reference_id="TXN123",
                type=TransactionType.DEBIT,
                acc_id=1,
                user_id=1
            ),
            Transaction(
                transaction_time=datetime.now(),
                amount=Decimal("200.00"),
                reference_id="TXN124",
                type=TransactionType.CREDIT,
                acc_id=1,
                user_id=1
            )
        ]
        
        bulk_request = BulkTransactionRequest(transactions=transactions)
        
        assert len(bulk_request.transactions) == 2
        assert bulk_request.transactions[0].reference_id == "TXN123"
        assert bulk_request.transactions[1].reference_id == "TXN124"
    
    def test_empty_bulk_request(self):
        """Test creating an empty bulk request."""
        bulk_request = BulkTransactionRequest(transactions=[])
        
        assert len(bulk_request.transactions) == 0


class TestBulkTransactionResponse:
    """Test cases for BulkTransactionResponse model."""
    
    def test_valid_bulk_response(self):
        """Test creating a valid bulk transaction response."""
        response = BulkTransactionResponse(
            success_count=5,
            failure_count=2,
            total_processed=7,
            inserted_ids=[1, 2, 3, 4, 5],
            errors=["Error 1", "Error 2"]
        )
        
        assert response.success_count == 5
        assert response.failure_count == 2
        assert response.total_processed == 7
        assert len(response.inserted_ids) == 5
        assert len(response.errors) == 2
    
    def test_bulk_response_without_errors(self):
        """Test bulk response without errors."""
        response = BulkTransactionResponse(
            success_count=3,
            failure_count=0,
            total_processed=3,
            inserted_ids=[1, 2, 3]
        )
        
        assert response.errors is None
        assert response.failure_count == 0