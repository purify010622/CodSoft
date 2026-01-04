"""
Search Engine for the SmartConnect Contact Management System.

This module provides the ContactSearchEngine class that handles intelligent search
and filtering operations with real-time capabilities and flexible sorting options.
"""

from datetime import datetime
from typing import List
from models import Contact
from contact_manager import ContactManager


class ContactSearchEngine:
    """
    Intelligent search and filtering engine for contact management.
    
    Provides real-time search capabilities with case-insensitive matching,
    flexible sorting options, and comprehensive filtering across multiple fields.
    """
    
    def __init__(self, contact_manager: ContactManager):
        """
        Initialize ContactSearchEngine with ContactManager dependency.
        
        Args:
            contact_manager: ContactManager instance for data access
        """
        self.contact_manager = contact_manager
    
    def search_by_name(self, query: str) -> List[Contact]:
        """
        Search contacts by name with case-insensitive matching.
        
        Args:
            query: Search query string for name matching
            
        Returns:
            List of Contact objects matching the name query
        """
        if not query or not query.strip():
            return []
        
        query_lower = query.strip().lower()
        all_contacts = self.contact_manager.get_all_contacts()
        
        return [
            contact for contact in all_contacts
            if query_lower in contact.name.lower()
        ]
    
    def search_by_phone(self, query: str) -> List[Contact]:
        """
        Search contacts by phone number with partial matching.
        
        Args:
            query: Search query string for phone matching
            
        Returns:
            List of Contact objects matching the phone query
        """
        if not query or not query.strip():
            return []
        
        query_clean = query.strip()
        all_contacts = self.contact_manager.get_all_contacts()
        
        return [
            contact for contact in all_contacts
            if query_clean in contact.phone
        ]
    
    def search_combined(self, query: str) -> List[Contact]:
        """
        Search contacts by name or phone number with case-insensitive matching.
        
        This is the main search method that provides comprehensive search
        across both name and phone fields, matching the requirements for
        real-time search functionality.
        
        Args:
            query: Search query string
            
        Returns:
            List of Contact objects matching either name or phone query
        """
        if not query or not query.strip():
            return self.contact_manager.get_all_contacts()
        
        query_lower = query.strip().lower()
        all_contacts = self.contact_manager.get_all_contacts()
        
        matching_contacts = []
        for contact in all_contacts:
            # Case-insensitive name matching
            if query_lower in contact.name.lower():
                matching_contacts.append(contact)
            # Phone number matching (exact substring)
            elif query.strip() in contact.phone:
                matching_contacts.append(contact)
        
        return matching_contacts
    
    def sort_contacts(self, contacts: List[Contact], sort_by: str) -> List[Contact]:
        """
        Sort contacts according to specified criteria.
        
        Args:
            contacts: List of Contact objects to sort
            sort_by: Sorting criteria ("name" for alphabetical, "recent" for creation date)
            
        Returns:
            List of Contact objects sorted according to criteria
        """
        if not contacts:
            return []
        
        if sort_by == "recent":
            # Sort by creation date, newest first
            return sorted(
                contacts,
                key=lambda c: c.created_at or datetime.min,
                reverse=True
            )
        else:
            # Default: sort alphabetically by name (case-insensitive)
            return sorted(
                contacts,
                key=lambda c: c.name.lower()
            )
    
    def search_and_sort(self, query: str, sort_by: str = "name") -> List[Contact]:
        """
        Combined search and sort operation for complete functionality.
        
        This method provides the complete search and sort functionality
        required by the system, handling both empty queries (return all)
        and filtered results with proper sorting.
        
        Args:
            query: Search query string (empty returns all contacts)
            sort_by: Sorting criteria ("name" for alphabetical, "recent" for creation date)
            
        Returns:
            List of Contact objects matching query and sorted by criteria
        """
        # Get search results (or all contacts if query is empty)
        if not query or not query.strip():
            contacts = self.contact_manager.get_all_contacts()
        else:
            contacts = self.search_combined(query)
        
        # Apply sorting
        return self.sort_contacts(contacts, sort_by)
    
    def reset_search(self, sort_by: str = "name") -> List[Contact]:
        """
        Reset search to show all contacts with specified sorting.
        
        This method handles the search reset behavior required by the system,
        restoring the full contact list when search is cleared.
        
        Args:
            sort_by: Sorting criteria for the full contact list
            
        Returns:
            List of all Contact objects sorted by criteria
        """
        all_contacts = self.contact_manager.get_all_contacts()
        return self.sort_contacts(all_contacts, sort_by)