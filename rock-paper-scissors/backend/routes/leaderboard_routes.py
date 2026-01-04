"""
Leaderboard routes - LeaderboardPage
Handle leaderboard with filters and sorting
"""
from flask import Blueprint, request, jsonify
from utils.database import get_db
from datetime import datetime, timedelta

bp = Blueprint('leaderboard', __name__)

@bp.route('/', methods=['GET'])
def get_leaderboard():
    """Get leaderboard with filters - LeaderboardPage"""
    db = get_db()
    
    # Get query parameters
    filter_type = request.args.get('filter', 'all_time')  # all_time, monthly, weekly, daily
    sort_by = request.args.get('sort_by', 'win_rate')  # win_rate, total_wins, total_games
    limit = min(int(request.args.get('limit', 30)), 30)  # Max 30
    
    # Build query based on filter
    query = {}
    if filter_type != 'all_time':
        time_filter = get_time_filter(filter_type)
        query['updated_at'] = {'$gte': time_filter}
    
    # Build sort
    sort_field = sort_by
    sort_order = -1  # Descending
    
    # Get leaderboard data
    leaderboard = list(db.leaderboard.find(query).sort(sort_field, sort_order).limit(limit))
    
    # Enrich with user data
    for i, entry in enumerate(leaderboard):
        entry['rank'] = i + 1
        entry.pop('_id')
        
        # Get user details
        user = db.users.find_one({'firebase_uid': entry['user_id']})
        if user:
            entry['display_name'] = user.get('display_name', user.get('username'))
            entry['profile_picture'] = user.get('profile_picture', '')
    
    return jsonify({
        'leaderboard': leaderboard,
        'filter': filter_type,
        'sort_by': sort_by,
        'total': len(leaderboard)
    }), 200

def get_time_filter(filter_type):
    """Get datetime filter based on filter type"""
    now = datetime.utcnow()
    
    if filter_type == 'daily':
        return now - timedelta(days=1)
    elif filter_type == 'weekly':
        return now - timedelta(weeks=1)
    elif filter_type == 'monthly':
        return now - timedelta(days=30)
    
    return datetime.min
