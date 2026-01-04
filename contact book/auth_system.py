#!/usr/bin/env python3
"""
Complete Authentication System for SmartConnect
Provides signup, login, and session management with bcrypt password hashing
"""

import sqlite3
import bcrypt
import secrets
from typing import Tuple, Optional, Dict
from datetime import datetime, timedelta


class AuthenticationSystem:
    """Complete authentication system with bcrypt password hashing."""
    
    def __init__(self, db_path: str = "contacts.db"):
        """Initialize authentication system."""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize authentication tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if users table exists and get its columns
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            table_exists = cursor.fetchone() is not None
            
            if table_exists:
                # Get existing columns
                cursor.execute("PRAGMA table_info(users)")
                existing_columns = {row[1] for row in cursor.fetchall()}
                
                # Add missing columns if needed
                if 'name' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN name TEXT")
                if 'email' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN email TEXT UNIQUE")
                if 'password_hash' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
                if 'role' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
                if 'status' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active'")
                if 'created_at' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                if 'last_login' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
                if 'failed_login_attempts' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0")
                if 'suspension_end' not in existing_columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN suspension_end TIMESTAMP")
                
                conn.commit()
            else:
                # Create users table from scratch
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT DEFAULT 'user' CHECK(role IN ('user', 'admin')),
                        status TEXT DEFAULT 'active' CHECK(status IN ('active', 'banned', 'suspended')),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        failed_login_attempts INTEGER DEFAULT 0,
                        suspension_end TIMESTAMP
                    )
                ''')
            
            # Create user_sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Create activity log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auth_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
                )
            ''')
            
            conn.commit()
            
            # Create default admin if none exists
            cursor.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
            if cursor.fetchone()[0] == 0:
                self._create_default_admin(cursor)
                conn.commit()
    
    def _create_default_admin(self, cursor) -> None:
        """Create default admin account."""
        password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        
        # Check if username column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'username' in columns:
            cursor.execute('''
                INSERT INTO users (name, username, email, password_hash, role)
                VALUES (?, ?, ?, ?, ?)
            ''', ("Administrator", "admin", "admin@smartconnect.com", password_hash, "admin"))
        else:
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', ("Administrator", "admin@smartconnect.com", password_hash, "admin"))
    
    def signup(self, name: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user account.
        
        Args:
            name: User's full name
            email: User's email address
            password: Plain text password (will be hashed)
            
        Returns:
            Tuple of (success, message)
        """
        # Validate input
        if not name or not email or not password:
            return False, "All fields are required"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if '@' not in email:
            return False, "Invalid email address"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if email already exists
                cursor.execute('SELECT COUNT(*) FROM users WHERE email = ?', (email,))
                if cursor.fetchone()[0] > 0:
                    return False, "Email already registered"
                
                # Hash password with bcrypt
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                # Check if username column exists
                cursor.execute("PRAGMA table_info(users)")
                columns = {row[1] for row in cursor.fetchall()}
                
                # Insert new user with username field if it exists
                if 'username' in columns:
                    # Use email as username for compatibility
                    cursor.execute('''
                        INSERT INTO users (name, username, email, password_hash, role)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, email, email, password_hash, 'user'))
                else:
                    cursor.execute('''
                        INSERT INTO users (name, email, password_hash, role)
                        VALUES (?, ?, ?, ?)
                    ''', (name, email, password_hash, 'user'))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                # Log activity
                self._log_activity(cursor, user_id, "SIGNUP", f"New user registered: {email}")
                conn.commit()
                
                return True, "Account created successfully! Please login."
                
        except sqlite3.Error as e:
            return False, f"Registration failed: {str(e)}"
    
    def login(self, email: str, password: str, ip_address: str = None) -> Tuple[bool, str, Optional[str], Optional[Dict]]:
        """
        Authenticate user and create session.
        
        Args:
            email: User's email
            password: User's password
            ip_address: Client IP address
            
        Returns:
            Tuple of (success, message, session_token, user_data)
        """
        if not email or not password:
            return False, "Email and password are required", None, None
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user
                cursor.execute('''
                    SELECT id, name, email, password_hash, role, status, 
                           suspension_end, failed_login_attempts
                    FROM users WHERE email = ?
                ''', (email,))
                
                user = cursor.fetchone()
                
                if not user:
                    self._log_activity(cursor, None, "LOGIN_FAILED", f"Unknown email: {email}", ip_address)
                    conn.commit()
                    return False, "Invalid email or password", None, None
                
                user_id, name, email_db, password_hash, role, status, suspension_end, failed_attempts = user
                
                # Check account status
                if status == 'banned':
                    self._log_activity(cursor, user_id, "LOGIN_BLOCKED", "Banned user attempted login", ip_address)
                    conn.commit()
                    return False, "Account is banned. Contact administrator.", None, None
                
                if status == 'suspended':
                    if suspension_end and datetime.fromisoformat(suspension_end) > datetime.now():
                        self._log_activity(cursor, user_id, "LOGIN_BLOCKED", "Suspended user attempted login", ip_address)
                        conn.commit()
                        return False, f"Account suspended until {suspension_end}", None, None
                
                # Check for account lockout (5 failed attempts)
                if failed_attempts >= 5:
                    self._log_activity(cursor, user_id, "LOGIN_BLOCKED", "Locked account attempted login", ip_address)
                    conn.commit()
                    return False, "Account locked due to too many failed attempts. Contact administrator.", None, None
                
                # Verify password
                if not bcrypt.checkpw(password.encode('utf-8'), password_hash):
                    # Increment failed attempts
                    cursor.execute('''
                        UPDATE users SET failed_login_attempts = failed_login_attempts + 1
                        WHERE id = ?
                    ''', (user_id,))
                    conn.commit()
                    
                    self._log_activity(cursor, user_id, "LOGIN_FAILED", "Invalid password", ip_address)
                    conn.commit()
                    return False, "Invalid email or password", None, None
                
                # Successful login - reset failed attempts
                cursor.execute('''
                    UPDATE users SET failed_login_attempts = 0, last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user_id,))
                
                # Create session token
                session_token = secrets.token_urlsafe(32)
                expires_at = datetime.now() + timedelta(days=7)  # 7 day session
                
                cursor.execute('''
                    INSERT INTO user_sessions (user_id, session_token, expires_at, ip_address)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, session_token, expires_at.isoformat(), ip_address))
                
                conn.commit()
                
                # Log successful login
                self._log_activity(cursor, user_id, "LOGIN_SUCCESS", f"User logged in: {email}", ip_address)
                conn.commit()
                
                # Return user data
                user_data = {
                    'id': user_id,
                    'name': name,
                    'email': email_db,
                    'role': role,
                    'status': status
                }
                
                return True, f"Welcome back, {name}!", session_token, user_data
                
        except Exception as e:
            return False, f"Login failed: {str(e)}", None, None
    
    def validate_session(self, session_token: str) -> Tuple[bool, Optional[Dict]]:
        """
        Validate session token and return user data.
        
        Args:
            session_token: Session token to validate
            
        Returns:
            Tuple of (is_valid, user_data)
        """
        if not session_token:
            return False, None
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT s.user_id, s.expires_at, u.name, u.email, u.role, u.status
                    FROM user_sessions s
                    JOIN users u ON s.user_id = u.id
                    WHERE s.session_token = ? AND s.is_active = 1
                ''', (session_token,))
                
                result = cursor.fetchone()
                
                if not result:
                    return False, None
                
                user_id, expires_at, name, email, role, status = result
                
                # Check expiration
                if datetime.fromisoformat(expires_at) < datetime.now():
                    # Deactivate expired session
                    cursor.execute('''
                        UPDATE user_sessions SET is_active = 0
                        WHERE session_token = ?
                    ''', (session_token,))
                    conn.commit()
                    return False, None
                
                # Check user status
                if status != 'active':
                    return False, None
                
                user_data = {
                    'id': user_id,
                    'name': name,
                    'email': email,
                    'role': role,
                    'status': status
                }
                
                return True, user_data
                
        except Exception:
            return False, None
    
    def logout(self, session_token: str) -> bool:
        """
        Logout user by invalidating session token.
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            True if successful
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user_id before deactivating
                cursor.execute('SELECT user_id FROM user_sessions WHERE session_token = ?', (session_token,))
                result = cursor.fetchone()
                
                if result:
                    user_id = result[0]
                    
                    # Deactivate session
                    cursor.execute('''
                        UPDATE user_sessions SET is_active = 0
                        WHERE session_token = ?
                    ''', (session_token,))
                    
                    self._log_activity(cursor, user_id, "LOGOUT", "User logged out")
                    conn.commit()
                
                return True
                
        except Exception:
            return False
    
    def _log_activity(self, cursor, user_id: Optional[int], action: str, 
                     details: str = None, ip_address: str = None) -> None:
        """Log authentication activity."""
        try:
            cursor.execute('''
                INSERT INTO auth_activity (user_id, action, details, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (user_id, action, details, ip_address))
        except Exception:
            pass  # Don't fail operations if logging fails
    
    def is_admin(self, session_token: str) -> bool:
        """Check if session belongs to an admin user."""
        is_valid, user_data = self.validate_session(session_token)
        return is_valid and user_data and user_data.get('role') == 'admin'
