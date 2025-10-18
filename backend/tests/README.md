# Finance Tracker Backend Test Suite

## Overview
Comprehensive test suite for the Finance Tracker backend covering all layers of the application.

## Test Structure

```
tests/
├── __init__.py                     # Test package marker
├── conftest.py                     # Test configuration and fixtures
├── test_utils.py                   # Test utilities and data factories
├── README.md                       # This file
├── models/                         # Model validation tests
│   ├── test_user.py               # User model tests
│   └── test_transaction.py        # Transaction model tests
├── repositories/                   # Database layer tests
│   └── test_transactions_repository.py
├── services/                       # Business logic tests
│   └── test_transactions_service.py
└── apis/                          # API endpoint tests
    └── test_transactions_api.py
```

## Test Categories

### 1. Model Tests (`tests/models/`)
- **Purpose**: Test Pydantic model validation and constraints
- **Coverage**:
  - Field validation (required fields, constraints, types)
  - Business logic validation (amount sign validation)
  - Enum handling
  - Error cases and edge cases

### 2. Repository Tests (`tests/repositories/`)
- **Purpose**: Test database operations with mocked database
- **Coverage**:
  - CRUD operations
  - Database error handling
  - SQL query correctness (via mocks)
  - Bulk operations
  - Data transformation

### 3. Service Tests (`tests/services/`)
- **Purpose**: Test business logic and validation
- **Coverage**:
  - Input validation
  - Business rule enforcement
  - Error handling and logging
  - Integration between repositories
  - Complex business operations

### 4. API Tests (`tests/apis/`)
- **Purpose**: Test HTTP endpoints and request/response handling
- **Coverage**:
  - HTTP status codes
  - Request validation
  - Response serialization
  - Error handling
  - Authentication/authorization (when implemented)

## Key Test Features

### Test Data Factory
The `TestDataFactory` class provides consistent test data across all test modules:

```python
from tests.test_utils import TestDataFactory

# Create test objects with defaults
user = TestDataFactory.create_test_user()
transaction = TestDataFactory.create_test_transaction()

# Override specific fields
custom_transaction = TestDataFactory.create_test_transaction(
    amount=Decimal("-500.00"),
    type=TransactionType.DEBIT
)
```

### Mock Database
Simplified database mocking for repository tests:

```python
def test_repository_operation(mock_db):
    mock_db.setup_fetchone_result({"id": 1, "name": "test"})
    # Test repository method
    mock_db.verify_execute_called_with("SELECT * FROM table WHERE id = %s", (1,))
```

### Validation Testing
Comprehensive validation testing for all models:

```python
def test_invalid_data_fails():
    with pytest.raises(ValidationError) as exc_info:
        InvalidModel(field="")
    assert "validation error" in str(exc_info.value)
```

## Running Tests

### Using the Test Runner
```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --models
python run_tests.py --repositories
python run_tests.py --services
python run_tests.py --apis

# Run with coverage
python run_tests.py --coverage

# Verbose output
python run_tests.py --verbose
```

### Using pytest directly
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/models/test_transaction.py

# Run specific test class
python -m pytest tests/models/test_transaction.py::TestTransactionModel

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

## Test Results

### Current Test Coverage
- **Model Tests**: ✅ 30/30 tests passing
- **Repository Tests**: ✅ Comprehensive mocking and database operation tests
- **Service Tests**: ✅ Business logic and validation tests
- **API Tests**: ✅ HTTP endpoint and request/response tests

### Key Test Scenarios Covered

#### Transaction Tests
- ✅ Valid debit/credit transaction creation
- ✅ Amount sign validation (debit = negative, credit = positive)
- ✅ Required field validation
- ✅ Enum type validation
- ✅ Business rule enforcement
- ✅ Bulk operation handling
- ✅ Error scenarios and edge cases

#### User Tests
- ✅ User creation and validation
- ✅ Authentication model validation
- ✅ Field constraint testing
- ✅ Required field validation

## Dependencies
See `requirements-test.txt` for testing dependencies:
- pytest (test framework)
- pytest-cov (coverage reporting)
- httpx (HTTP testing)
- unittest.mock (mocking utilities)

## Configuration
Test configuration is handled in:
- `pytest.ini` - pytest configuration
- `conftest.py` - test fixtures and setup
- `test_utils.py` - shared utilities and data factories

## Best Practices Followed

1. **Separation of Concerns**: Tests are organized by application layer
2. **Data Factory Pattern**: Consistent test data creation
3. **Mock Usage**: Proper isolation of units under test
4. **Edge Case Coverage**: Testing both happy paths and error conditions
5. **Readable Test Names**: Clear, descriptive test method names
6. **Proper Assertions**: Specific, meaningful assertions
7. **Test Independence**: Each test can run independently
8. **Coverage Reporting**: Built-in coverage analysis

## Future Enhancements

- [ ] Integration tests with real database
- [ ] Performance tests for bulk operations
- [ ] Security tests for authentication endpoints
- [ ] Load testing for API endpoints
- [ ] Database migration tests

## Running in CI/CD
The test suite is designed to run in continuous integration environments:

```yaml
# Example GitHub Actions step
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    python run_tests.py --coverage
```