"""
Game routes
Handle game creation, moves, and history
"""
from flask import Blueprint, request, jsonify
from utils.database import get_db
from utils.game_logic import validate_move, get_computer_move, determine_winner
from middleware.auth import verify_token
from datetime import datetime
import uuid

bp = Blueprint('game', __name__)

@bp.route('/create', methods=['POST'])
@verify_token
def create_game():
    """Create a new game"""
    db = get_db()
    data = request.json
    user_id = request.user['uid']
    
    game_mode = data.get('mode', 'quick_play')  # quick_play, best_of_3, best_of_5, best_of_7, endless
    opponent_type = data.get('opponent_type', 'computer')  # computer or user
    
    game = {
        'game_id': str(uuid.uuid4()),
        'mode': game_mode,
        'opponent_type': opponent_type,
        'players': [user_id] if opponent_type == 'computer' else [user_id, None],
        'status': 'active',
        'rounds': [],
        'current_round': 1,
        'scores': {
            'player1': 0,
            'player2': 0,
            'ties': 0
        },
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    db.games.insert_one(game)
    game.pop('_id')
    
    return jsonify({
        'message': 'Game created',
        'game': game
    }), 201

@bp.route('/move', methods=['POST'])
@verify_token
def make_move():
    """Submit a move in a game"""
    db = get_db()
    data = request.json
    user_id = request.user['uid']
    
    game_id = data.get('game_id')
    player_move = data.get('move', '').lower()
    
    # Validate move
    if not validate_move(player_move):
        return jsonify({'error': 'Invalid move'}), 400
    
    # Get game
    game = db.games.find_one({'game_id': game_id})
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    # Check if user is in game
    if user_id not in game['players']:
        return jsonify({'error': 'Not a player in this game'}), 403
    
    # Generate computer move if playing vs computer
    if game['opponent_type'] == 'computer':
        computer_move = get_computer_move()
        winner = determine_winner(player_move, computer_move)
        
        # Create round result
        round_result = {
            'round_number': game['current_round'],
            'player1_move': player_move,
            'player2_move': computer_move,
            'winner': winner,
            'timestamp': datetime.utcnow()
        }
        
        # Update scores
        if winner == 'player1':
            game['scores']['player1'] += 1
        elif winner == 'player2':
            game['scores']['player2'] += 1
        else:
            game['scores']['ties'] += 1
        
        # Add round to game
        game['rounds'].append(round_result)
        game['current_round'] += 1
        game['updated_at'] = datetime.utcnow()
        
        # Check if game is finished
        if should_end_game(game):
            game['status'] = 'finished'
            update_user_stats(db, user_id, game)
        
        # Update game in database
        db.games.update_one(
            {'game_id': game_id},
            {'$set': game}
        )
        
        game.pop('_id')
        
        return jsonify({
            'message': 'Move processed',
            'round_result': round_result,
            'game': game
        }), 200
    
    return jsonify({'error': 'Online multiplayer moves handled via Socket.IO'}), 400

@bp.route('/<game_id>', methods=['GET'])
@verify_token
def get_game(game_id):
    """Get game details"""
    db = get_db()
    game = db.games.find_one({'game_id': game_id})
    
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    game.pop('_id')
    return jsonify({'game': game}), 200

@bp.route('/history', methods=['GET'])
@verify_token
def get_history():
    """Get user's game history"""
    db = get_db()
    user_id = request.user['uid']
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    skip = (page - 1) * limit
    
    # Get games
    games = list(db.games.find(
        {'players': user_id, 'status': 'finished'}
    ).sort('created_at', -1).skip(skip).limit(limit))
    
    # Remove _id from results
    for game in games:
        game.pop('_id')
    
    total = db.games.count_documents({'players': user_id, 'status': 'finished'})
    
    return jsonify({
        'games': games,
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    }), 200

def should_end_game(game):
    """Check if game should end based on mode"""
    mode = game['mode']
    scores = game['scores']
    
    if mode == 'quick_play':
        return len(game['rounds']) >= 1
    elif mode == 'best_of_3':
        return scores['player1'] >= 2 or scores['player2'] >= 2
    elif mode == 'best_of_5':
        return scores['player1'] >= 3 or scores['player2'] >= 3
    elif mode == 'best_of_7':
        return scores['player1'] >= 4 or scores['player2'] >= 4
    elif mode == 'endless':
        return False  # Never ends automatically
    
    return False

def update_user_stats(db, user_id, game):
    """Update user statistics after game ends"""
    scores = game['scores']
    
    # Determine if user won
    user_won = scores['player1'] > scores['player2']
    user_lost = scores['player1'] < scores['player2']
    
    # Update user stats
    update_data = {
        '$inc': {
            'stats.total_games': 1,
            'stats.wins': 1 if user_won else 0,
            'stats.losses': 1 if user_lost else 0,
            'stats.ties': 1 if scores['player1'] == scores['player2'] else 0
        },
        '$set': {
            'updated_at': datetime.utcnow()
        }
    }
    
    db.users.update_one({'firebase_uid': user_id}, update_data)
    
    # Recalculate win rate
    user = db.users.find_one({'firebase_uid': user_id})
    if user:
        total_games = user['stats']['total_games']
        wins = user['stats']['wins']
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        
        db.users.update_one(
            {'firebase_uid': user_id},
            {'$set': {'stats.win_rate': round(win_rate, 2)}}
        )
        
        # Update leaderboard
        db.leaderboard.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'total_wins': wins,
                    'total_games': total_games,
                    'win_rate': round(win_rate, 2),
                    'updated_at': datetime.utcnow()
                }
            },
            upsert=True
        )
