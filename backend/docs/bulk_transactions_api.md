# Bulk Transaction Insert API

## Overview

The bulk transaction insert functionality allows you to insert multiple transactions in a single API call, improving performance and reducing network overhead.

## Endpoint

**POST** `/transactions/bulk`

## Request Body

```json
{
  "transactions": [
    {
      "transaction_time": "2023-10-18T10:00:00Z",
      "description": "Payment to vendor",
      "amount": -150.00,
      "reference_id": "TXN001",
      "type": "debit",
      "acc_id": 1,
      "user_id": 1,
      "category_id": 5,
      "tag_id": 2
    },
    {
      "transaction_time": "2023-10-18T11:00:00Z", 
      "description": "Salary credit",
      "amount": 3000.00,
      "reference_id": "TXN002",
      "type": "credit",
      "acc_id": 1,
      "user_id": 1,
      "category_id": 1
    }
  ]
}
```

## Response Body

```json
{
  "success_count": 2,
  "failure_count": 0,
  "total_processed": 2,
  "inserted_ids": [101, 102],
  "errors": null
}
```

## Response Fields

- `success_count`: Number of transactions successfully inserted
- `failure_count`: Number of transactions that failed to insert
- `total_processed`: Total number of transactions in the request
- `inserted_ids`: Array of generated transaction IDs for successful inserts
- `errors`: Array of error messages (null if no errors)

## Validation Rules

Each transaction must include:
- `transaction_time`: Valid datetime
- `amount`: Decimal value (required)
- `user_id`: Valid user ID (required)
- `acc_id`: Valid account ID (required)

Optional fields:
- `description`: Transaction description
- `old_description`: Original description
- `reference_id`: External reference
- `type`: Transaction type
- `category_id`: Category assignment
- `tag_id`: Tag assignment

## Limits

- Maximum 1000 transactions per bulk request
- Transactions are processed in batches of 1000 for optimal performance

## Error Handling

- Returns 400 if no transactions provided
- Returns 400 if exceeding 1000 transaction limit
- Returns 400 if all transactions fail validation
- Partial failures return 200 with error details in response

## Performance Benefits

- Uses PostgreSQL's `execute_batch` for efficient bulk operations
- Reduces network round trips
- Optimized for high-volume transaction imports
- Transactional safety with rollback on errors

## Example cURL Request

```bash
curl -X POST "http://localhost:8000/transactions/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {
        "transaction_time": "2023-10-18T10:00:00Z",
        "description": "Coffee purchase", 
        "amount": -4.50,
        "acc_id": 1,
        "user_id": 1
      }
    ]
  }'
```