"""
Authentication middleware - HYBRID MODE
Uses JWT decoding (without signature verification) to extract UID
This allows Real Firebase Frontend to talk to Mock Backend
"""
from functools import wraps
from flask import request, jsonify
import jwt

def verify_token(f):
    """
    Decorator to verify Token
    Accepts valid JWTs and extracts UID
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            # Decode JWT without verification (since we lack private key to verify, 
            # and public key fetch is complex for this demo)
            # Warning: This is insecure for production but functional for demo
            
            # If it's a simple string (Guest/Demo), handle it
            if not token.count('.') == 2:
                # Assume it's a raw UID from demo mode
                request.user = {'uid': token, 'email': 'demo@example.com'}
            else:
                # It's a JWT from Firebase
                decoded = jwt.decode(token, options={"verify_signature": False})
                request.user = {
                    'uid': decoded['sub'],
                    'email': decoded.get('email')
                }
                
            return f(*args, **kwargs)
            
        except Exception as e:
            print(f"Token decode error: {e}")
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Admin check skipped for demo
        return f(*args, **kwargs)
    return decorated_function
