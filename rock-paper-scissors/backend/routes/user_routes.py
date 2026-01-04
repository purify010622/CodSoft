"""
User routes - ProfilePage and SettingsPage
Handle user profile, settings, and friend management
"""
from flask import Blueprint, request, jsonify
from utils.database import get_db
from middleware.auth import verify_token
from datetime import datetime

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['GET'])
@verify_token
def get_profile():
    """Get user profile - ProfilePage"""
    db = get_db()
    user_id = request.args.get('user_id', request.user['uid'])
    
    user = db.users.find_one({'firebase_uid': user_id})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.pop('_id')
    return jsonify({'user': user}), 200

@bp.route('/profile', methods=['PUT'])
@verify_token
def update_profile():
    """Update user profile - SettingsPage"""
    db = get_db()
    user_id = request.user['uid']
    data = request.json
    
    # Fields that can be updated
    allowed_fields = ['display_name', 'bio', 'profile_picture', 'username']
    update_data = {}
    
    for field in allowed_fields:
        if field in data:
            # Check username uniqueness
            if field == 'username':
                existing = db.users.find_one({'username': data[field], 'firebase_uid': {'$ne': user_id}})
                if existing:
                    return jsonify({'error': 'Username already taken'}), 400
            update_data[field] = data[field]
    
    if update_data:
        update_data['updated_at'] = datetime.utcnow()
        db.users.update_one({'firebase_uid': user_id}, {'$set': update_data})
    
    return jsonify({'message': 'Profile updated successfully'}), 200

@bp.route('/stats', methods=['GET'])
@verify_token
def get_stats():
    """Get user statistics with filters - ProfilePage"""
    db = get_db()
    user_id = request.args.get('user_id', request.user['uid'])
    filter_type = request.args.get('filter', 'all')  # all, daily, weekly, monthly
    
    user = db.users.find_one({'firebase_uid': user_id})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get filtered game history
    from datetime import timedelta
    query = {'players': user_id, 'status': 'finished'}
    
    if filter_type == 'daily':
        query['created_at'] = {'$gte': datetime.utcnow() - timedelta(days=1)}
    elif filter_type == 'weekly':
        query['created_at'] = {'$gte': datetime.utcnow() - timedelta(weeks=1)}
    elif filter_type == 'monthly':
        query['created_at'] = {'$gte': datetime.utcnow() - timedelta(days=30)}
    
    games = list(db.games.find(query))
    
    # Calculate filtered stats
    filtered_stats = calculate_stats(games, user_id)
    
    return jsonify({
        'overall_stats': user['stats'],
        'filtered_stats': filtered_stats,
        'filter': filter_type
    }), 200

@bp.route('/friend-request', methods=['POST'])
@verify_token
def send_friend_request():
    """Send friend request - ProfilePage"""
    db = get_db()
    user_id = request.user['uid']
    data = request.json
    friend_username = data.get('username')
    
    # Find friend
    friend = db.users.find_one({'username': friend_username})
    if not friend:
        return jsonify({'error': 'User not found'}), 404
    
    friend_id = friend['firebase_uid']
    
    # Check if already friends
    existing = db.friends.find_one({
        'user_id': user_id,
        'friend_id': friend_id
    })
    if existing:
        return jsonify({'error': 'Already friends or request pending'}), 400
    
    # Create friend request
    friend_request = {
        'user_id': user_id,
        'friend_id': friend_id,
        'status': 'pending',
        'created_at': datetime.utcnow()
    }
    
    db.friends.insert_one(friend_request)
    
    return jsonify({'message': 'Friend request sent'}), 201

@bp.route('/friends', methods=['GET'])
@verify_token
def get_friends():
    """Get user's friends list - ProfilePage"""
    db = get_db()
    user_id = request.user['uid']
    
    # Get accepted friends
    friends = list(db.friends.find({
        'user_id': user_id,
        'status': 'accepted'
    }))
    
    # Get friend details
    friend_ids = [f['friend_id'] for f in friends]
    friend_users = list(db.users.find({'firebase_uid': {'$in': friend_ids}}))
    
    # Remove sensitive data
    for user in friend_users:
        user.pop('_id')
        user.pop('email', None)
    
    return jsonify({'friends': friend_users}), 200

@bp.route('/friend-requests', methods=['GET'])
@verify_token
def get_friend_requests():
    """Get pending friend requests - SettingsPage"""
    db = get_db()
    user_id = request.user['uid']
    
    # Get pending requests
    requests = list(db.friends.find({
        'friend_id': user_id,
        'status': 'pending'
    }))
    
    # Get requester details
    requester_ids = [r['user_id'] for r in requests]
    requesters = list(db.users.find({'firebase_uid': {'$in': requester_ids}}))
    
    for user in requesters:
        user.pop('_id')
    
    return jsonify({'requests': requesters}), 200

@bp.route('/friend-request/<request_id>/accept', methods=['PUT'])
@verify_token
def accept_friend_request(request_id):
    """Accept friend request - SettingsPage"""
    db = get_db()
    user_id = request.user['uid']
    
    # Update request status
    result = db.friends.update_one(
        {'_id': request_id, 'friend_id': user_id},
        {'$set': {'status': 'accepted', 'updated_at': datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        return jsonify({'error': 'Request not found'}), 404
    
    return jsonify({'message': 'Friend request accepted'}), 200

def calculate_stats(games, user_id):
    """Calculate statistics from games"""
    total_games = len(games)
    wins = 0
    losses = 0
    ties = 0
    
    for game in games:
        scores = game['scores']
        if scores['player1'] > scores['player2']:
            wins += 1
        elif scores['player1'] < scores['player2']:
            losses += 1
        else:
            ties += 1
    
    win_rate = (wins / total_games * 100) if total_games > 0 else 0
    
    return {
        'total_games': total_games,
        'wins': wins,
        'losses': losses,
        'ties': ties,
        'win_rate': round(win_rate, 2)
    }
