from flask import Blueprint, request, jsonify
from utils.database import get_db
import uuid
from datetime import datetime
from middleware.auth import verify_token

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    """
    Login/Register Endpoint
    Syncs Firebase user data with local MongoDB
    """
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name') or email.split('@')[0] if email else 'Guest'
        uid = data.get('uid')
        photo_url = data.get('photo_url') or f"https://api.dicebear.com/7.x/avataaars/svg?seed={name}"

        if not uid:
             return jsonify({'error': 'UID required'}), 400

        db = get_db()
        
        # Check if user exists by UID
        user = db.users.find_one({'firebase_uid': uid})
        
        if not user:
            # Create new user
            user = {
                'firebase_uid': uid,
                'email': email,
                'username': name,
                'photo_url': photo_url,
                'created_at': datetime.utcnow(),
                'last_login': datetime.utcnow(),
                # Consistent stats structure
                'stats': {
                    'wins': 0,
                    'losses': 0,
                    'ties': 0, # Note: socket_handler uses 'ties', mock used 'draws'. Standardizing on 'ties'
                    'total_games': 0,
                    'win_rate': 0.0
                }
            }
            db.users.insert_one(user)
        else:
            # Update existing user details (Sync)
            updates = {
                'last_login': datetime.utcnow()
            }
            if name: updates['username'] = name
            if photo_url: updates['photo_url'] = photo_url
            
            db.users.update_one({'firebase_uid': uid}, {'$set': updates})
            # Fetch updated user
            user = db.users.find_one({'firebase_uid': uid})
        
        # Prepare response
        return jsonify({
            'success': True, 
            'user': {
                'uid': user['firebase_uid'],
                'email': user.get('email'),
                'username': user.get('username'),
                'photo_url': user.get('photo_url'),
                'stats': user.get('stats', {})
            }
        }), 200

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['GET'])
@verify_token
def get_profile():
    """
    Get current user profile
    """
    try:
        # request.user is set by verify_token middleware
        uid = request.user['uid']
        
        db = get_db()
        user = db.users.find_one({'firebase_uid': uid})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Helper to handle ObjectId serialization if needed (though find_one returns dict)
        if '_id' in user:
            user['_id'] = str(user['_id'])
            
        return jsonify(user), 200
        
    except Exception as e:
        print(f"Profile error: {e}")
        return jsonify({'error': str(e)}), 500
