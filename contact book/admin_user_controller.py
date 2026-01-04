#!/usr/bin/env python3
"""
Admin User Management Controller
Handles all admin operations for user management
"""

import sqlite3
import bcrypt
import secrets
import string
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from admin_middleware import AdminMiddleware
from auth_system import AuthenticationSystem


class AdminUserController:
    """Controller for admin user management operations."""
    
    def __init__(self, auth_system: AuthenticationSystem):
        """Initialize controller."""
        self.auth_system = auth_system
        self.middleware = AdminMiddleware(auth_system)
        self.db_path = auth_system.db_path
    
    @property
    def require_admin(self):
        """Get admin decorator."""
        return self.middleware.require_admin
    
    def get_all_users(self, session_token: str) -> Tuple[bool, str, Optional[List[Dict]]]:
        """Get all users (admin only)."""
        @self.require_admin
        def _get_users(session_token, user_data):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        SELECT id, name, email, role, status, created_at, 
                               last_login, failed_login_attempts, suspension_end
                        FROM users
                        ORDER BY created_at DESC
                    ''')
                    
                    users = []
                    for row in cursor.fetchall():
                        users.append({
                            'id': row[0],
                            'name': row[1],
                            'email': row[2],
                            'role': row[3],
                            'status': row[4],
                            'created_at': row[5],
                            'last_login': row[6],
                            'failed_login_attempts': row[7],
                            'suspension_end': row[8]
                        })
                    
                    return True, "Users retrieved successfully", users
                    
            except Exception as e:
                return False, f"Failed to retrieve users: {str(e)}", None
        
        return _get_users(session_token)
    
    def create_user(self, session_token: str, name: str, email: str, 
                   password: str, role: str = 'user') -> Tuple[bool, str]:
        """Create new user (admin only)."""
        @self.require_admin
        def _create_user(session_token, user_data):
            # Validate input
            if not name or not email or not password:
                return False, "All fields are required"
            
            if role not in ['user', 'admin']:
                return False, "Invalid role. Must be 'user' or 'admin'"
            
            if len(password) < 8:
                return False, "Password must be at least 8 characters"
            
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Check if email exists
                    cursor.execute('SELECT COUNT(*) FROM users WHERE email = ?', (email,))
                    if cursor.fetchone()[0] > 0:
                        return False, "Email already exists"
                    
                    # Hash password
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    
                    # Create user
                    cursor.execute('''
                        INSERT INTO users (name, email, password_hash, role, status)
                        VALUES (?, ?, ?, ?, 'active')
                    ''', (name, email, password_hash, role))
                    
                    new_user_id = cursor.lastrowid
                    conn.commit()
                    
                    # Log activity
                    cursor.execute('''
                        INSERT INTO auth_activity (user_id, action, details)
                        VALUES (?, ?, ?)
                    ''', (user_data['id'], "USER_CREATED", 
                          f"Admin created user: {email} with role {role}"))
                    conn.commit()
                    
                    return True, f"User '{name}' created successfully"
                    
            except Exception as e:
                return False, f"Failed to create user: {str(e)}"
        
        return _create_user(session_token)
    
    def delete_user(self, session_token: str, user_id: int) -> Tuple[bool, str]:
        """Delete user permanently (admin only)."""
        @self.require_admin
        def _delete_user(session_token, user_data):
            # Prevent self-deletion
            if user_id == user_data['id']:
                return False, "Cannot delete your own account"
            
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Get user info
                    cursor.execute('SELECT name, email, role FROM users WHERE id = ?', (user_id,))
                    target_user = cursor.fetchone()
                    
                    if not target_user:
                        return False, "User not found"
                    
                    name, email, role = target_user
                    
                    # Prevent deleting last admin
                    if role == 'admin':
                        cursor.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
                        if cursor.fetchone()[0] <= 1:
                            return False, "Cannot delete the last admin account"
                    
                    # Delete user (CASCADE will handle sessions)
                    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                    conn.commit()
                    
                    # Log activity
                    cursor.execute('''
                        INSERT INTO auth_activity (user_id, action, details)
                        VALUES (?, ?, ?)
                    ''', (user_data['id'], "USER_DELETED", 
                          f"Admin deleted user: {email} ({name})"))
                    conn.commit()
                    
                    return True, f"User '{name}' deleted successfully"
                    
            except Exception as e:
                return False, f"Failed to delete user: {str(e)}"
        
        return _delete_user(session_token)
    
    def ban_user(self, session_token: str, user_id: int, reason: str = "") -> Tuple[bool, str]:
        """Ban user account (admin only)."""
        @self.require_admin
        def _ban_user(session_token, user_data):
            # Prevent self-ban
            if user_id == user_data['id']:
                return False, "Cannot ban your own account"
            
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Get user info
                    cursor.execute('SELECT name, email FROM users WHERE id = ?', (user_id,))
                    target_user = cursor.fetchone()
                    
                    if not target_user:
                        return False, "User not found"
                    
                    name, email = target_user
                    
                    # Ban user
                    cursor.execute('''
                        UPDATE users SET status = 'banned'
                        WHERE id = ?
                    ''', (user_id,))
                    
                    # Terminate all active sessions
                    cursor.execute('''
                        UPDATE user_sessions SET is_active = 0
                        WHERE user_id = ?
                    ''', (user_id,))
                    
                    conn.commit()
                    
                    # Log activity
                    details = f"Admin banned user: {email} ({name})"
                    if reason:
                        details += f" - Reason: {reason}"
                    
                    cursor.execute('''
                        INSERT INTO auth_activity (user_id, action, details)
                        VALUES (?, ?, ?)
                    ''', (user_data['id'], "USER_BANNED", details))
                    conn.commit()
                    
                    return True, f"User '{name}' has been banned"
                    
            except Exception as e:
                return False, f"Failed to ban user: {str(e)}"
        
        return _ban_user(session_token)
    
    def suspend_user(self, session_token: str, user_id: int, 
                    days: int, reason: str = "") -> Tuple[bool, str]:
        """Suspend user for specified days (admin only)."""
        @self.require_admin
        def _suspend_user(session_token, user_data):
            # Prevent self-suspension
            if user_id == user_data['id']:
                return False, "Cannot suspend your own account"
            
            if days <= 0:
                return False, "Suspension days must be positive"
            
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Get user info
                    cursor.execute('SELECT name, email FROM users WHERE id = ?', (user_id,))
                    target_user = cursor.fetchone()
                    
                    if not target_user:
                        return False, "User not found"
                    
                    name, email = target_user
                    
                    # Calculate suspension end
                    suspension_end = datetime.now() + timedelta(days=days)
                    
                    # Suspend user
                    cursor.execute('''
                        UPDATE users SET status = 'suspended', suspension_end = ?
                        WHERE id = ?
                    ''', (suspension_end.isoformat(), user_id))
                    
                    # Terminate active sessions
                    cursor.execute('''
                        UPDATE user_sessions SET is_active = 0
                        WHERE user_id = ?
                    ''', (user_id,))
                    
                    conn.commit()
                    
                    # Log activity
                    details = f"Admin suspended user: {email} ({name}) for {days} days"
                    if reason:
                        details += f" - Reason: {reason}"
                    
                    cursor.execute('''
                        INSERT INTO auth_activity (user_id, action, details)
                        VALUES (?, ?, ?)
                    ''', (user_data['id'], "USER_SUSPENDED", details))
                    conn.commit()
                    
                    return True, f"User '{name}' suspended for {days} days"
                    
            except Exception as e:
                return False, f"Failed to suspend user: {str(e)}"
        
        return _suspend_user(session_token)
    
    def reactivate_user(self, session_token: str, user_id: int) -> Tuple[bool, str]:
        """Reactivate banned/suspended user (admin only)."""
        @self.require_admin
        def _reactivate_user(session_token, user_data):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Get user info
                    cursor.execute('SELECT name, email, status FROM users WHERE id = ?', (user_id,))
                    target_user = cursor.fetchone()
                    
                    if not target_user:
                        return False, "User not found"
                    
                    name, email, status = target_user
                    
                    if status == 'active':
                        return False, f"User '{name}' is already active"
                    
                    # Reactivate user
                    cursor.execute('''
                        UPDATE users SET status = 'active', suspension_end = NULL
                        WHERE id = ?
                    ''', (user_id,))
                    conn.commit()
                    
                    # Log activity
                    cursor.execute('''
                        INSERT INTO auth_activity (user_id, action, details)
                        VALUES (?, ?, ?)
                    ''', (user_data['id'], "USER_REACTIVATED", 
                          f"Admin reactivated user: {email} ({name}) from {status} status"))
                    conn.commit()
                    
                    return True, f"User '{name}' has been reactivated"
                    
            except Exception as e:
                return False, f"Failed to reactivate user: {str(e)}"
        
        return _reactivate_user(session_token)
    
    def reset_password(self, session_token: str, user_id: int) -> Tuple[bool, str, Optional[str]]:
        """Reset user password and return temporary password (admin only)."""
        @self.require_admin
        def _reset_password(session_token, user_data):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Get user info
                    cursor.execute('SELECT name, email FROM users WHERE id = ?', (user_id,))
                    target_user = cursor.fetchone()
                    
                    if not target_user:
                        return False, "User not found", None
                    
                    name, email = target_user
                    
                    # Generate temporary password
                    temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) 
                                          for _ in range(12))
                    
                    # Hash password
                    password_hash = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt())
                    
                    # Update password and reset failed attempts
                    cursor.execute('''
                        UPDATE users SET password_hash = ?, failed_login_attempts = 0
                        WHERE id = ?
                    ''', (password_hash, user_id))
                    conn.commit()
                    
                    # Log activity
                    cursor.execute('''
                        INSERT INTO auth_activity (user_id, action, details)
                        VALUES (?, ?, ?)
                    ''', (user_data['id'], "PASSWORD_RESET", 
                          f"Admin reset password for user: {email} ({name})"))
                    conn.commit()
                    
                    return True, f"Password reset for '{name}'", temp_password
                    
            except Exception as e:
                return False, f"Failed to reset password: {str(e)}", None
        
        return _reset_password(session_token)
    
    def get_user_statistics(self, session_token: str) -> Tuple[bool, str, Optional[Dict]]:
        """Get user statistics (admin only)."""
        @self.require_admin
        def _get_stats(session_token, user_data):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    stats = {}
                    
                    # Total users
                    cursor.execute('SELECT COUNT(*) FROM users')
                    stats['total_users'] = cursor.fetchone()[0]
                    
                    # Active users
                    cursor.execute('SELECT COUNT(*) FROM users WHERE status = "active"')
                    stats['active_users'] = cursor.fetchone()[0]
                    
                    # Banned users
                    cursor.execute('SELECT COUNT(*) FROM users WHERE status = "banned"')
                    stats['banned_users'] = cursor.fetchone()[0]
                    
                    # Suspended users
                    cursor.execute('SELECT COUNT(*) FROM users WHERE status = "suspended"')
                    stats['suspended_users'] = cursor.fetchone()[0]
                    
                    # Admin users
                    cursor.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
                    stats['admin_users'] = cursor.fetchone()[0]
                    
                    # Active sessions
                    cursor.execute('SELECT COUNT(*) FROM user_sessions WHERE is_active = 1')
                    stats['active_sessions'] = cursor.fetchone()[0]
                    
                    return True, "Statistics retrieved", stats
                    
            except Exception as e:
                return False, f"Failed to get statistics: {str(e)}", None
        
        return _get_stats(session_token)
