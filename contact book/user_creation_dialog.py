#!/usr/bin/env python3
"""
User Creation Dialog with Comprehensive Validation for SmartConnect Admin Panel.

This module provides a user creation dialog with comprehensive input validation,
error handling, and security checks.
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Tuple
from error_handler import InputValidator, ValidationError, ErrorHandler
from security_config import SecurityConfig


class UserCreationDialog:
    """
    Comprehensive user creation dialog with validation and error handling.
    """
    
    def __init__(self, parent, user_manager, auth_manager):
        """
        Initialize user creation dialog.
        
        Args:
            parent: Parent window
            user_manager: UserManager instance
            auth_manager: AuthManager instance
        """
        self.parent = parent
        self.user_manager = user_manager
        self.auth_manager = auth_manager
        self.error_handler = ErrorHandler("user_creation_errors.log")
        
        self.dialog = None
        self.result = None
        
        # Form variables
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.confirm_password_var = ctk.StringVar()
        self.full_name_var = ctk.StringVar()
        self.email_var = ctk.StringVar()
        self.department_var = ctk.StringVar()
        self.role_var = ctk.StringVar(value="user")
        
        # Validation labels
        self.validation_labels = {}
        
        # Form entries
        self.form_entries = {}
    
    def show(self) -> Optional[Dict]:
        """
        Show the user creation dialog.
        
        Returns:
            User data dictionary if successful, None if cancelled
        """
        try:
            self._create_dialog()
            self._create_interface()
            
            if self.dialog:
                self.dialog.transient(self.parent)
                self.dialog.grab_set()
                self.dialog.wait_window()
            
            return self.result
            
        except Exception as e:
            self.error_handler.handle_error(e, {"operation": "show_user_creation_dialog"})
            return None
    
    def _create_dialog(self):
        """Create the dialog window."""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Create New User")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        
        # Configure grid
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(0, weight=1)
    
    def _create_interface(self):
        """Create the dialog interface."""
        if not self.dialog:
            return
        
        # Main frame
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            main_frame,
            text="Create New User Account",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Form fields
        fields = [
            ("Username*", "username", self.username_var, True),
            ("Password*", "password", self.password_var, True),
            ("Confirm Password*", "confirm_password", self.confirm_password_var, True),
            ("Full Name", "full_name", self.full_name_var, False),
            ("Email", "email", self.email_var, False),
            ("Department", "department", self.department_var, False),
        ]
        
        row = 1
        for label_text, field_name, var, is_required in fields:
            # Field label
            label = ctk.CTkLabel(main_frame, text=label_text)
            label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)
            
            # Field entry
            if field_name in ["password", "confirm_password"]:
                entry = ctk.CTkEntry(main_frame, textvariable=var, show="*", width=250)
            else:
                entry = ctk.CTkEntry(main_frame, textvariable=var, width=250)
            
            entry.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=5)
            self.form_entries[field_name] = entry
            
            # Validation label
            validation_label = ctk.CTkLabel(
                main_frame,
                text="",
                text_color="red",
                font=ctk.CTkFont(size=10)
            )
            validation_label.grid(row=row, column=2, sticky="w", padx=5, pady=5)
            self.validation_labels[field_name] = validation_label
            
            # Bind validation events
            if is_required or field_name in ["email", "full_name"]:
                var.trace_add("write", lambda *args, field=field_name: self._validate_field(field))
            
            row += 1
        
        # Role selection
        role_label = ctk.CTkLabel(main_frame, text="Role*")
        role_label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)
        
        role_menu = ctk.CTkOptionMenu(
            main_frame,
            values=["user", "admin"],
            variable=self.role_var,
            width=250
        )
        role_menu.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=5)
        row += 1
        
        # Password requirements info
        req_frame = ctk.CTkFrame(main_frame)
        req_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=0, pady=20)
        req_frame.grid_columnconfigure(0, weight=1)
        
        req_title = ctk.CTkLabel(
            req_frame,
            text="Password Requirements:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        req_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        
        requirements = [
            f"• At least {SecurityConfig.PASSWORD_MIN_LENGTH} characters long",
            "• At least one uppercase letter",
            "• At least one lowercase letter", 
            "• At least one digit",
            "• At least one special character (!@#$%^&*(),.?\":{}|<>)",
            "• Cannot be a common password"
        ]
        
        for i, req in enumerate(requirements, 1):
            req_label = ctk.CTkLabel(
                req_frame,
                text=req,
                font=ctk.CTkFont(size=10),
                justify="left"
            )
            req_label.grid(row=i, column=0, sticky="w", padx=25, pady=2)
        
        row += 1
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=0, pady=20)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel,
            fg_color="gray",
            width=100
        )
        cancel_btn.pack(side="left", padx=15, pady=15)
        
        # Create button
        create_btn = ctk.CTkButton(
            button_frame,
            text="Create User",
            command=self._create_user,
            width=120
        )
        create_btn.pack(side="right", padx=15, pady=15)
    
    def _validate_field(self, field_name: str) -> bool:
        """
        Validate individual field and show error message.
        
        Args:
            field_name: Name of field to validate
            
        Returns:
            True if field is valid, False otherwise
        """
        try:
            validation_label = self.validation_labels.get(field_name)
            if not validation_label:
                return True
            
            # Clear previous validation message
            validation_label.configure(text="")
            
            # Get field value
            if field_name == "username":
                value = self.username_var.get()
                is_valid, errors = InputValidator.validate_username(value)
            elif field_name == "email":
                value = self.email_var.get()
                is_valid, errors = InputValidator.validate_email(value)
            elif field_name == "full_name":
                value = self.full_name_var.get()
                is_valid, errors = InputValidator.validate_full_name(value)
            elif field_name == "password":
                value = self.password_var.get()
                is_valid, errors = SecurityConfig.validate_password_strength(value)
            elif field_name == "confirm_password":
                password = self.password_var.get()
                confirm = self.confirm_password_var.get()
                if confirm and password != confirm:
                    is_valid, errors = False, ["Passwords do not match"]
                else:
                    is_valid, errors = True, []
            else:
                return True
            
            # Show validation error
            if not is_valid and errors:
                validation_label.configure(text=errors[0])
                return False
            
            return True
            
        except Exception as e:
            self.error_handler.handle_error(e, {"field": field_name})
            return False
    
    def _validate_all_fields(self) -> Tuple[bool, Dict]:
        """
        Validate all form fields.
        
        Returns:
            Tuple of (is_valid, user_data)
        """
        try:
            # Validate required fields
            username = self.username_var.get().strip()
            password = self.password_var.get()
            confirm_password = self.confirm_password_var.get()
            
            if not username:
                raise ValidationError("Username is required", "username")
            
            if not password:
                raise ValidationError("Password is required", "password")
            
            if not confirm_password:
                raise ValidationError("Password confirmation is required", "confirm_password")
            
            # Validate individual fields
            fields_to_validate = ["username", "password", "confirm_password", "email", "full_name"]
            for field in fields_to_validate:
                if not self._validate_field(field):
                    return False, {}
            
            # Check password match
            if password != confirm_password:
                raise ValidationError("Passwords do not match", "confirm_password")
            
            # Prepare user data
            user_data = {
                "username": username,
                "password": password,
                "role": self.role_var.get(),
                "full_name": self.full_name_var.get().strip() or None,
                "email": self.email_var.get().strip() or None,
                "department": self.department_var.get().strip() or None
            }
            
            return True, user_data
            
        except ValidationError as e:
            # Show validation error on specific field
            if e.field and e.field in self.validation_labels:
                self.validation_labels[e.field].configure(text=e.message)
            else:
                messagebox.showerror("Validation Error", e.message)
            return False, {}
        except Exception as e:
            self.error_handler.handle_error(e, {"operation": "validate_all_fields"})
            return False, {}
    
    def _create_user(self):
        """Handle user creation."""
        try:
            # Validate all fields
            is_valid, user_data = self._validate_all_fields()
            if not is_valid:
                return
            
            # Create user through user manager
            success, message = self.user_manager.create_user_account(user_data)
            
            if success:
                messagebox.showinfo("Success", f"User '{user_data['username']}' created successfully!")
                self.result = user_data
                self._close()
            else:
                messagebox.showerror("Error", f"Failed to create user: {message}")
                
        except Exception as e:
            self.error_handler.handle_error(e, {"operation": "create_user"})
    
    def _cancel(self):
        """Handle cancellation."""
        self.result = None
        self._close()
    
    def _close(self):
        """Close the dialog."""
        if self.dialog:
            self.dialog.destroy()