"""
Contact Manager for the SmartConnect Contact Management System.

This module provides the ContactManager class that serves as the core business logic
layer, coordinating contact operations between the GUI and database layers.
"""

import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from models import Contact
from database import ContactDatabase
from validation import ContactValidator


class ContactManager:
    """
    Core business logic layer for contact management operations.
    
    Coordinates between the GUI layer and database layer, providing high-level
    contact operations with validation, error handling, and business rules.
    """
    
    def __init__(self, database: ContactDatabase, auth_manager=None):
        """
        Initialize ContactManager with database connection.
        
        Args:
            database: ContactDatabase instance for data persistence
            auth_manager: Optional AuthManager instance for permission checking
        """
        self.database = database
        self.validator = ContactValidator()
        self.auth_manager = auth_manager
    
    def _check_authentication(self) -> bool:
        """Check if user is authenticated."""
        if self.auth_manager:
            return self.auth_manager.is_authenticated()
        return True  # Allow operations if no auth manager (backward compatibility)
    
    def _log_activity(self, action: str, details: str = None) -> None:
        """Log user activity if auth manager is available."""
        if self.auth_manager and self.auth_manager.is_authenticated():
            user_id = self.auth_manager.get_current_user_id()
            if user_id:
                self.auth_manager._log_user_activity(user_id, action, details)
    
    def create_contact(self, contact_data: Dict[str, str]) -> Tuple[bool, str]:
        """
        Create a new contact with validation.
        
        Args:
            contact_data: Dictionary containing contact field values
            
        Returns:
            Tuple[bool, str]: (success, message) - success status and result message
        """
        try:
            # Check authentication
            if not self._check_authentication():
                return False, "Authentication required to create contacts"
            
            # Create contact object from provided data
            contact = Contact(
                name=contact_data.get('name', '').strip(),
                phone=contact_data.get('phone', '').strip(),
                email=contact_data.get('email', '').strip(),
                address=contact_data.get('address', '').strip(),
                company=contact_data.get('company', '').strip(),
                job_title=contact_data.get('job_title', '').strip(),
                category=contact_data.get('category', 'Friends').strip()
            )
            
            # Validate contact data
            is_valid, validation_errors = self.validator.is_valid_contact(contact)
            if not is_valid:
                error_message = "Validation failed: " + "; ".join(validation_errors)
                return False, error_message
            
            # Save to database
            contact_id = self.database.add_contact(contact)
            
            # Log activity
            self._log_activity("CONTACT_CREATED", f"Created contact: {contact.name} (ID: {contact_id})")
            
            return True, f"Contact created successfully with ID {contact_id}"
            
        except Exception as e:
            return False, f"Failed to create contact: {str(e)}"
    
    def update_contact(self, contact_id: int, contact_data: Dict[str, str]) -> Tuple[bool, str]:
        """
        Update an existing contact with validation.
        
        Args:
            contact_id: ID of the contact to update
            contact_data: Dictionary containing updated contact field values
            
        Returns:
            Tuple[bool, str]: (success, message) - success status and result message
        """
        try:
            # Check authentication
            if not self._check_authentication():
                return False, "Authentication required to update contacts"
            
            # Check if contact exists
            existing_contact = self.database.get_contact(contact_id)
            if not existing_contact:
                return False, f"Contact with ID {contact_id} not found"
            
            # Create updated contact object, preserving existing values for unspecified fields
            updated_contact = Contact(
                id=contact_id,
                name=contact_data.get('name', existing_contact.name).strip(),
                phone=contact_data.get('phone', existing_contact.phone).strip(),
                email=contact_data.get('email', existing_contact.email).strip(),
                address=contact_data.get('address', existing_contact.address).strip(),
                company=contact_data.get('company', existing_contact.company).strip(),
                job_title=contact_data.get('job_title', existing_contact.job_title).strip(),
                category=contact_data.get('category', existing_contact.category).strip(),
                created_at=existing_contact.created_at  # Preserve original creation time
            )
            
            # Validate updated contact data
            is_valid, validation_errors = self.validator.is_valid_contact(updated_contact)
            if not is_valid:
                error_message = "Validation failed: " + "; ".join(validation_errors)
                return False, error_message
            
            # Update in database
            success = self.database.update_contact(updated_contact)
            if success:
                # Log activity
                self._log_activity("CONTACT_UPDATED", f"Updated contact: {updated_contact.name} (ID: {contact_id})")
                return True, "Contact updated successfully"
            else:
                return False, f"Contact with ID {contact_id} not found"
                
        except Exception as e:
            return False, f"Failed to update contact: {str(e)}"
    
    def delete_contact(self, contact_id: int) -> Tuple[bool, str]:
        """
        Delete a contact with proper error handling.
        
        Args:
            contact_id: ID of the contact to delete
            
        Returns:
            Tuple[bool, str]: (success, message) - success status and result message
        """
        try:
            # Check authentication
            if not self._check_authentication():
                return False, "Authentication required to delete contacts"
            
            # Check if contact exists before deletion
            existing_contact = self.database.get_contact(contact_id)
            if not existing_contact:
                return False, f"Contact with ID {contact_id} not found"
            
            # Perform deletion
            success = self.database.delete_contact(contact_id)
            if success:
                # Log activity
                self._log_activity("CONTACT_DELETED", f"Deleted contact: {existing_contact.name} (ID: {contact_id})")
                return True, f"Contact '{existing_contact.name}' deleted successfully"
            else:
                return False, f"Failed to delete contact with ID {contact_id}"
                
        except Exception as e:
            return False, f"Failed to delete contact: {str(e)}"
    
    def get_contact(self, contact_id: int) -> Optional[Contact]:
        """
        Retrieve a specific contact by ID.
        
        Args:
            contact_id: ID of the contact to retrieve
            
        Returns:
            Contact object if found, None otherwise
        """
        try:
            return self.database.get_contact(contact_id)
        except Exception:
            return None
    
    def get_all_contacts(self, sort_by: str = "name") -> List[Contact]:
        """
        Retrieve all contacts with optional sorting.
        
        Args:
            sort_by: Sorting criteria ("name" for alphabetical, "recent" for creation date)
            
        Returns:
            List of Contact objects sorted according to criteria
        """
        try:
            contacts = self.database.get_all_contacts()
            
            if sort_by == "recent":
                # Sort by creation date, newest first
                contacts.sort(key=lambda c: c.created_at or datetime.min, reverse=True)
            else:
                # Default: sort alphabetically by name
                contacts.sort(key=lambda c: c.name.lower())
            
            return contacts
        except Exception:
            return []
    
    def search_contacts(self, query: str) -> List[Contact]:
        """
        Search contacts by name or phone number.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Contact objects
        """
        try:
            if not query or not query.strip():
                return self.get_all_contacts()
            
            return self.database.search_contacts(query.strip())
        except Exception:
            return []
    
    def export_contacts_csv(self, file_path: str) -> Tuple[bool, str]:
        """
        Export all contacts to a CSV file.
        
        Args:
            file_path: Path where the CSV file should be saved
            
        Returns:
            Tuple[bool, str]: (success, message) - success status and result message
        """
        try:
            contacts = self.get_all_contacts()
            
            if not contacts:
                return False, "No contacts to export"
            
            # Define CSV headers
            headers = [
                'ID', 'Name', 'Phone', 'Email', 'Address', 
                'Company', 'Job Title', 'Category', 'Created At', 'Updated At'
            ]
            
            # Write CSV file
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                writer.writerow(headers)
                
                # Write contact data
                for contact in contacts:
                    writer.writerow([
                        contact.id,
                        contact.name,
                        contact.phone,
                        contact.email,
                        contact.address,
                        contact.company,
                        contact.job_title,
                        contact.category,
                        contact.created_at.isoformat() if contact.created_at else '',
                        contact.updated_at.isoformat() if contact.updated_at else ''
                    ])
            
            return True, f"Successfully exported {len(contacts)} contacts to {file_path}"
            
        except Exception as e:
            return False, f"Failed to export contacts: {str(e)}"
    
    def get_contact_count(self) -> int:
        """
        Get the total number of contacts in the database.
        
        Returns:
            int: Total number of contacts
        """
        try:
            contacts = self.database.get_all_contacts()
            return len(contacts)
        except Exception:
            return 0
    
    def validate_contact_data(self, contact_data: Dict[str, str]) -> Tuple[bool, List[str]]:
        """
        Validate contact data without creating a contact.
        
        Args:
            contact_data: Dictionary containing contact field values
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        try:
            # Create temporary contact object for validation
            contact = Contact(
                name=contact_data.get('name', '').strip(),
                phone=contact_data.get('phone', '').strip(),
                email=contact_data.get('email', '').strip(),
                address=contact_data.get('address', '').strip(),
                company=contact_data.get('company', '').strip(),
                job_title=contact_data.get('job_title', '').strip(),
                category=contact_data.get('category', 'Friends').strip()
            )
            
            return self.validator.is_valid_contact(contact)
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]