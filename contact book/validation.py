"""
Validation engine for the SmartConnect Contact Management System.

This module provides the ContactValidator class that handles real-time input validation
using regex patterns for email, phone number, and name validation.
"""

import re
from typing import List, Tuple
from models import Contact


class ContactValidator:
    """
    Validation engine for contact data using regex patterns.
    
    Provides static methods for validating individual fields and comprehensive
    contact validation with detailed error reporting.
    """
    
    # Email validation pattern - supports standard email formats
    EMAIL_PATTERN = re.compile(r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$')
    
    # Phone validation pattern - flexible format supporting international numbers
    # Allows digits, spaces, hyphens, parentheses, and optional + prefix
    PHONE_PATTERN = re.compile(r'^[\+]?[0-9\s\-\(\)]{10,15}$')
    
    # Name validation pattern - allows letters, spaces, apostrophes, and hyphens
    NAME_PATTERN = re.compile(r'^[a-zA-Z\s\'\-]+$')
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format using regex pattern.
        
        Args:
            email: Email address string to validate
            
        Returns:
            bool: True if email format is valid, False otherwise
        """
        if not email:  # Empty email is considered valid (optional field)
            return True
        
        return bool(ContactValidator.EMAIL_PATTERN.match(email.strip()))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format using flexible regex pattern.
        
        Supports various formats including:
        - (555) 123-4567
        - 555-123-4567
        - 555 123 4567
        - 5551234567
        - +1 555 123 4567
        
        Args:
            phone: Phone number string to validate
            
        Returns:
            bool: True if phone format is valid, False otherwise
        """
        if not phone:  # Empty phone is considered valid (optional field)
            return True
        
        # Remove extra whitespace and check pattern
        cleaned_phone = phone.strip()
        if not cleaned_phone:  # If only whitespace, consider invalid
            return False
            
        return bool(ContactValidator.PHONE_PATTERN.match(cleaned_phone))
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Validate contact name format.
        
        Names must:
        - Not be empty or only whitespace
        - Contain only letters, spaces, apostrophes, and hyphens
        - Have at least one non-whitespace character
        
        Args:
            name: Name string to validate
            
        Returns:
            bool: True if name format is valid, False otherwise
        """
        if not name or not name.strip():
            return False
        
        cleaned_name = name.strip()
        return bool(ContactValidator.NAME_PATTERN.match(cleaned_name))
    
    @staticmethod
    def validate_category(category: str) -> bool:
        """
        Validate contact category.
        
        Args:
            category: Category string to validate
            
        Returns:
            bool: True if category is valid, False otherwise
        """
        valid_categories = {'Family', 'Friends', 'Work'}
        return category in valid_categories
    
    @staticmethod
    def get_validation_errors(contact: Contact) -> List[str]:
        """
        Perform comprehensive validation of a contact and return all errors.
        
        Args:
            contact: Contact object to validate
            
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        # Validate required name field
        if not ContactValidator.validate_name(contact.name):
            if not contact.name or not contact.name.strip():
                errors.append("Name is required and cannot be empty")
            else:
                errors.append("Name contains invalid characters (only letters, spaces, apostrophes, and hyphens allowed)")
        
        # Validate optional email field
        if contact.email and not ContactValidator.validate_email(contact.email):
            errors.append("Email format is invalid (example: user@domain.com)")
        
        # Validate optional phone field
        if contact.phone and not ContactValidator.validate_phone(contact.phone):
            errors.append("Phone number format is invalid (10-15 digits with optional formatting)")
        
        # Validate category
        if not ContactValidator.validate_category(contact.category):
            errors.append("Category must be one of: Family, Friends, Work")
        
        return errors
    
    @staticmethod
    def is_valid_contact(contact: Contact) -> Tuple[bool, List[str]]:
        """
        Check if a contact is valid and return validation status with errors.
        
        Args:
            contact: Contact object to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = ContactValidator.get_validation_errors(contact)
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_field(field_name: str, field_value: str) -> Tuple[bool, str]:
        """
        Validate a single field and return validation status with error message.
        
        Args:
            field_name: Name of the field to validate ('name', 'email', 'phone', 'category')
            field_value: Value to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if field_name == 'name':
            if ContactValidator.validate_name(field_value):
                return True, ""
            else:
                if not field_value or not field_value.strip():
                    return False, "Name is required and cannot be empty"
                else:
                    return False, "Name contains invalid characters"
        
        elif field_name == 'email':
            if ContactValidator.validate_email(field_value):
                return True, ""
            else:
                return False, "Email format is invalid"
        
        elif field_name == 'phone':
            if ContactValidator.validate_phone(field_value):
                return True, ""
            else:
                return False, "Phone number format is invalid"
        
        elif field_name == 'category':
            if ContactValidator.validate_category(field_value):
                return True, ""
            else:
                return False, "Category must be one of: Family, Friends, Work"
        
        else:
            return True, ""  # Unknown fields are considered valid