"""Tests for User model validation and functionality."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from models.user import User, UserCreate, UserAuth, UserPasswordUpdateRequest


class TestUserModel:
    """Test cases for User model."""
    
    def test_valid_user_creation(self):
        """Test creating a valid user."""
        user_data = {
            "user_id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": "hashed_password",
            "created_at": datetime.now(),
            "is_active": True
        }
        
        user = User(**user_data)
        assert user.user_id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active is True
    
    def test_user_with_defaults(self):
        """Test user creation with default values."""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password"
        )
        
        assert user.is_active is True
        assert user.last_login is None
        assert user.created_at is None
    
    def test_user_empty_username_fails(self):
        """Test that empty username fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            User(
                user_id=1,
                username="",
                email="test@example.com",
                password_hash="hashed_password"
            )
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_user_missing_required_fields_fails(self):
        """Test that missing required fields fail validation."""
        with pytest.raises(ValidationError):
            User(user_id=1)


class TestUserCreateModel:
    """Test cases for UserCreate model."""
    
    def test_valid_user_create(self):
        """Test creating a valid user creation request."""
        user_create = UserCreate(
            username="newuser",
            email="new@example.com",
            password="password123"
        )
        
        assert user_create.username == "newuser"
        assert user_create.email == "new@example.com"
        assert user_create.password == "password123"
    
    def test_user_create_empty_username_fails(self):
        """Test that empty username fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="",
                email="new@example.com",
                password="password123"
            )
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_user_create_missing_fields_fails(self):
        """Test that missing required fields fail validation."""
        with pytest.raises(ValidationError):
            UserCreate(username="newuser")


class TestUserAuthModel:
    """Test cases for UserAuth model."""
    
    def test_valid_user_auth(self):
        """Test creating a valid user authentication request."""
        user_auth = UserAuth(
            username_or_email="testuser",
            password="password123"
        )
        
        assert user_auth.username_or_email == "testuser"
        assert user_auth.password == "password123"
    
    def test_user_auth_with_email(self):
        """Test user auth with email instead of username."""
        user_auth = UserAuth(
            username_or_email="test@example.com",
            password="password123"
        )
        
        assert user_auth.username_or_email == "test@example.com"
    
    def test_user_auth_missing_fields_fails(self):
        """Test that missing required fields fail validation."""
        with pytest.raises(ValidationError):
            UserAuth(username_or_email="testuser")


class TestUserPasswordUpdateRequestModel:
    """Test cases for UserPasswordUpdateRequest model."""
    
    def test_valid_password_update(self):
        """Test creating a valid password update request."""
        password_update = UserPasswordUpdateRequest(password="newpassword123")
        
        assert password_update.password == "newpassword123"
    
    def test_password_update_missing_field_fails(self):
        """Test that missing password fails validation."""
        with pytest.raises(ValidationError):
            UserPasswordUpdateRequest()