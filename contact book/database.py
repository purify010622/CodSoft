"""
Database layer for the SmartConnect Contact Management System.

This module provides the ContactDatabase class that handles all database operations
using SQLite3 for persistent contact storage.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple
from models import Contact


class ContactDatabase:
    """
    Database access layer for contact management operations.
    
    Handles SQLite3 database connection, table creation, and all CRUD operations
    for contact data with proper error handling and transaction management.
    """
    
    def __init__(self, db_path: str = "contacts.db"):
        """
        Initialize database connection and create tables if they don't exist.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self.current_user_id = 1  # Default user ID
        self._connect()
        self.create_tables()
    
    def set_current_user(self, user_id: int):
        """Set the current user ID for filtering contacts."""
        self.current_user_id = user_id
    
    def _connect(self) -> None:
        """Establish database connection with proper error handling."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to connect to database: {e}")
    
    def create_tables(self) -> None:
        """
        Create the contacts table if it doesn't exist.
        
        Raises:
            RuntimeError: If table creation fails
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            company TEXT,
            job_title TEXT,
            category TEXT CHECK(category IN ('Family', 'Friends', 'Work')) DEFAULT 'Friends',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """
        
        try:
            cursor = self.connection.cursor()
            
            # Check if contacts table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'")
            table_exists = cursor.fetchone() is not None
            
            if table_exists:
                # Add user_id column if it doesn't exist
                cursor.execute("PRAGMA table_info(contacts)")
                columns = {row[1] for row in cursor.fetchall()}
                if 'user_id' not in columns:
                    cursor.execute("ALTER TABLE contacts ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
                    print("Added user_id column to contacts table")
            else:
                # Create new table with user_id
                cursor.execute(create_table_sql)
            
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create tables: {e}")
    
    def add_contact(self, contact: Contact) -> int:
        """
        Add a new contact to the database.
        
        Args:
            contact: Contact object to add
            
        Returns:
            int: The ID of the newly created contact
            
        Raises:
            RuntimeError: If contact creation fails
        """
        if self.connection is None:
            raise RuntimeError("Database connection is closed")
            
        insert_sql = """
        INSERT INTO contacts (user_id, name, phone, email, address, company, job_title, category, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            cursor = self.connection.cursor()
            now = datetime.now().isoformat()
            cursor.execute(insert_sql, (
                self.current_user_id,
                contact.name,
                contact.phone,
                contact.email,
                contact.address,
                contact.company,
                contact.job_title,
                contact.category,
                now,
                now
            ))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Failed to add contact: {e}")
    
    def get_contact(self, contact_id: int) -> Optional[Contact]:
        """
        Retrieve a contact by ID.
        
        Args:
            contact_id: ID of the contact to retrieve
            
        Returns:
            Contact object if found, None otherwise
            
        Raises:
            RuntimeError: If database query fails
        """
        if self.connection is None:
            raise RuntimeError("Database connection is closed")
            
        select_sql = "SELECT * FROM contacts WHERE id = ?"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_sql, (contact_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_contact(row)
            return None
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to retrieve contact: {e}")
    
    def get_all_contacts(self) -> List[Contact]:
        """
        Retrieve all contacts from the database for the current user.
        
        Returns:
            List of Contact objects
            
        Raises:
            RuntimeError: If database query fails
        """
        if self.connection is None:
            raise RuntimeError("Database connection is closed")
            
        select_sql = "SELECT * FROM contacts WHERE user_id = ? ORDER BY name"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_sql, (self.current_user_id,))
            rows = cursor.fetchall()
            
            return [self._row_to_contact(row) for row in rows]
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to retrieve contacts: {e}")
    
    def update_contact(self, contact: Contact) -> bool:
        """
        Update an existing contact in the database.
        
        Args:
            contact: Contact object with updated data (must have valid id)
            
        Returns:
            bool: True if contact was updated, False if not found
            
        Raises:
            RuntimeError: If update operation fails
            ValueError: If contact has no ID
        """
        if contact.id is None:
            raise ValueError("Contact must have an ID to be updated")
        
        if self.connection is None:
            raise RuntimeError("Database connection is closed")
        
        update_sql = """
        UPDATE contacts 
        SET name = ?, phone = ?, email = ?, address = ?, company = ?, 
            job_title = ?, category = ?, updated_at = ?
        WHERE id = ?
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(update_sql, (
                contact.name,
                contact.phone,
                contact.email,
                contact.address,
                contact.company,
                contact.job_title,
                contact.category,
                datetime.now().isoformat(),
                contact.id
            ))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Failed to update contact: {e}")
    
    def delete_contact(self, contact_id: int) -> bool:
        """
        Delete a contact from the database.
        
        Args:
            contact_id: ID of the contact to delete
            
        Returns:
            bool: True if contact was deleted, False if not found
            
        Raises:
            RuntimeError: If delete operation fails
        """
        if self.connection is None:
            raise RuntimeError("Database connection is closed")
            
        delete_sql = "DELETE FROM contacts WHERE id = ?"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_sql, (contact_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Failed to delete contact: {e}")
    
    def search_contacts(self, query: str) -> List[Contact]:
        """
        Search contacts by name or phone number for the current user.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Contact objects
            
        Raises:
            RuntimeError: If search query fails
        """
        if self.connection is None:
            raise RuntimeError("Database connection is closed")
            
        search_sql = """
        SELECT * FROM contacts 
        WHERE user_id = ? AND (LOWER(name) LIKE LOWER(?) OR phone LIKE ?)
        ORDER BY name
        """
        
        try:
            cursor = self.connection.cursor()
            search_pattern = f"%{query}%"
            cursor.execute(search_sql, (self.current_user_id, search_pattern, search_pattern))
            rows = cursor.fetchall()
            
            return [self._row_to_contact(row) for row in rows]
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to search contacts: {e}")
    
    def close_connection(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def _row_to_contact(self, row: sqlite3.Row) -> Contact:
        """
        Convert a database row to a Contact object.
        
        Args:
            row: SQLite row object
            
        Returns:
            Contact object
        """
        # Parse datetime strings back to datetime objects
        created_at = datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        updated_at = datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        
        return Contact(
            id=row['id'],
            name=row['name'],
            phone=row['phone'] or "",
            email=row['email'] or "",
            address=row['address'] or "",
            company=row['company'] or "",
            job_title=row['job_title'] or "",
            category=row['category'] or "Friends",
            created_at=created_at,
            updated_at=updated_at
        )
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure connection is closed."""
        self.close_connection()