#!/usr/bin/env python3
"""
Admin Middleware for protecting admin routes and operations
"""

from functools import wraps
from typing import Callable, Any
from auth_system import AuthenticationSystem


class AdminMiddleware:
    """Middleware for protecting admin-only operations."""
    
    def __init__(self, auth_system: AuthenticationSystem):
        """Initialize middleware with authentication system."""
        self.auth_system = auth_system
    
    def require_admin(self, func: Callable) -> Callable:
        """
        Decorator to require admin privileges for a function.
        
        Usage:
            @admin_middleware.require_admin
            def admin_only_function(session_token, ...):
                # This function requires admin access
                pass
        """
        @wraps(func)
        def wrapper(session_token: str, *args, **kwargs) -> Any:
            # Validate session
            is_valid, user_data = self.auth_system.validate_session(session_token)
            
            if not is_valid:
                return False, "Invalid or expired session", None
            
            # Check admin role
            if user_data.get('role') != 'admin':
                return False, "Admin privileges required", None
            
            # Call original function
            return func(session_token, user_data, *args, **kwargs)
        
        return wrapper
    
    def validate_admin_access(self, session_token: str) -> tuple[bool, str]:
        """
        Validate that session has admin access.
        
        Args:
            session_token: Session token to validate
            
        Returns:
            Tuple of (has_access, message)
        """
        is_valid, user_data = self.auth_system.validate_session(session_token)
        
        if not is_valid:
            return False, "Invalid or expired session"
        
        if user_data.get('role') != 'admin':
            return False, "Admin privileges required"
        
        return True, "Access granted"
