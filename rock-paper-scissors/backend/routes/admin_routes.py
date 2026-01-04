"""
Admin routes - AdminDashboard
Handle admin panel functionality
"""
from flask import Blueprint, request, jsonify
from utils.database import get_db
from middleware.auth import verify_token, admin_required
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__)

@bp.route('/users', methods=['GET'])
@verify_token
@admin_required
def get_all_users():
    """Get all users - AdminDashboard"""
    db = get_db()
    
    # Get pagination
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    skip = (page - 1) * limit
    
    # Get filters
    status = request.args.get('status')  # active, banned, suspended
    search = request.args.get('search')  # Search by username or email
    
    # Build query
    query = {}
    if status:
        query['status'] = status
    if search:
        query['$or'] = [
            {'username': {'$regex': search, '$options': 'i'}},
            {'email': {'$regex': search, '$options': 'i'}}
        ]
    
    # Get users
    users = list(db.users.find(query).skip(skip).limit(limit))
    total = db.users.count_documents(query)
    
    # Remove sensitive data
    for user in users:
        user.pop('_id')
    
    return jsonify({
        'users': users,
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    }), 200

@bp.route('/user/<user_id>/ban', methods=['PUT'])
@verify_token
@admin_required
def ban_user(user_id):
    """Ban a user - AdminDashboard"""
    db = get_db()
    data = request.json
    reason = data.get('reason', 'No reason provided')
    
    # Update user status
    result = db.users.update_one(
        {'firebase_uid': user_id},
        {
            '$set': {
                'status': 'banned',
                'ban_reason': reason,
                'banned_at': datetime.utcnow(),
                'banned_by': request.user['uid']
            }
        }
    )
    
    if result.modified_count == 0:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'message': 'User banned successfully'}), 200

@bp.route('/user/<user_id>/unban', methods=['PUT'])
@verify_token
@admin_required
def unban_user(user_id):
    """Unban a user - AdminDashboard"""
    db = get_db()
    
    result = db.users.update_one(
        {'firebase_uid': user_id},
        {
            '$set': {'status': 'active'},
            '$unset': {'ban_reason': '', 'banned_at': '', 'banned_by': ''}
        }
    )
    
    if result.modified_count == 0:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'message': 'User unbanned successfully'}), 200

@bp.route('/analytics', methods=['GET'])
@verify_token
@admin_required
def get_analytics():
    """Get system analytics - AdminDashboard"""
    db = get_db()
    
    # Total users
    total_users = db.users.count_documents({})
    active_users = db.users.count_documents({'status': 'active'})
    banned_users = db.users.count_documents({'status': 'banned'})
    
    # Total games
    total_games = db.games.count_documents({})
    active_games = db.games.count_documents({'status': 'active'})
    finished_games = db.games.count_documents({'status': 'finished'})
    
    # Games by mode
    games_by_mode = {}
    for mode in ['quick_play', 'best_of_3', 'best_of_5', 'best_of_7', 'endless']:
        games_by_mode[mode] = db.games.count_documents({'mode': mode})
    
    # Recent activity (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    new_users_today = db.users.count_documents({'created_at': {'$gte': yesterday}})
    games_today = db.games.count_documents({'created_at': {'$gte': yesterday}})
    
    # Top players
    top_players = list(db.leaderboard.find().sort('win_rate', -1).limit(5))
    for player in top_players:
        player.pop('_id')
    
    return jsonify({
        'users': {
            'total': total_users,
            'active': active_users,
            'banned': banned_users,
            'new_today': new_users_today
        },
        'games': {
            'total': total_games,
            'active': active_games,
            'finished': finished_games,
            'today': games_today,
            'by_mode': games_by_mode
        },
        'top_players': top_players
    }), 200

@bp.route('/games', methods=['GET'])
@verify_token
@admin_required
def get_all_games():
    """Get all games with filters - AdminDashboard"""
    db = get_db()
    
    # Get pagination
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    skip = (page - 1) * limit
    
    # Get filters
    status = request.args.get('status')
    mode = request.args.get('mode')
    
    # Build query
    query = {}
    if status:
        query['status'] = status
    if mode:
        query['mode'] = mode
    
    # Get games
    games = list(db.games.find(query).sort('created_at', -1).skip(skip).limit(limit))
    total = db.games.count_documents(query)
    
    for game in games:
        game.pop('_id')
    
    return jsonify({
        'games': games,
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    }), 200

@bp.route('/reports', methods=['GET'])
@verify_token
@admin_required
def get_reports():
    """Get user reports - AdminDashboard"""
    db = get_db()
    
    # Get pagination
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    skip = (page - 1) * limit
    
    # Get reports
    reports = list(db.reports.find().sort('created_at', -1).skip(skip).limit(limit))
    total = db.reports.count_documents({})
    
    for report in reports:
        report.pop('_id')
    
    return jsonify({
        'reports': reports,
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    }), 200
