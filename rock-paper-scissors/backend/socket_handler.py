"""
Socket.IO event handlers for real-time multiplayer
Handles online game matchmaking and gameplay
"""
from flask_socketio import emit, join_room, leave_room, disconnect
from flask import request
# from firebase_admin import auth # REMOVED FOR DEMO
from utils.database import get_db
from utils.game_logic import validate_move, determine_winner
from datetime import datetime
import uuid

# Store active games and waiting players
active_games = {}
waiting_players = []
connected_users = {}

def register_socket_handlers(socketio):
    """Register all Socket.IO event handlers"""
    
    @socketio.on('connect')
    def handle_connect(auth_data=None):
        """Handle client connection with auth"""
        token = None
        if auth_data and 'token' in auth_data:
            token = auth_data['token']
        elif request.headers.get('Authorization'):
            token = request.headers['Authorization'].split(' ')[1]
            
        if not token:
            print(f"Client rejected (no token): {request.sid}")
            return False
            
        try:
            # DEMO MODE: Trust the token as User ID
            # decoded_token = auth.verify_id_token(token)
            # user_id = decoded_token['uid']
            user_id = token # Token is UID in demo
            
            connected_users[request.sid] = user_id
            print(f"Client connected: {user_id} ({request.sid})")
            emit('connected', {'message': 'Connected to server'})
        except Exception as e:
            print(f"Client rejected (invalid token): {request.sid} - {e}")
            return False
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        sid = request.sid
        print(f"Client disconnected: {sid}")
        
        # Remove from waiting players
        if sid in waiting_players:
            waiting_players.remove(sid)
        
        # Handle active game disconnection
        if sid in connected_users:
            user_id = connected_users[sid]
            del connected_users[sid]
            
            # Find and end any active games
            for game_id, game_data in list(active_games.items()):
                if user_id in game_data['players']:
                    # Notify other player
                    other_player = [p for p in game_data['players'] if p != user_id][0]
                    emit('opponent_disconnected', {
                        'message': 'Opponent disconnected',
                        'game_id': game_id
                    }, room=game_data['room'])
                    
                    # Save game as abandoned
                    save_abandoned_game(game_id, game_data)
                    del active_games[game_id]
    
    @socketio.on('join_matchmaking')
    def handle_join_matchmaking(data):
        """Player joins matchmaking queue"""
        if request.sid not in connected_users:
            emit('error', {'message': 'Not authenticated'})
            return

        user_id = connected_users[request.sid]
        
        db = get_db()
        user = db.users.find_one({'firebase_uid': user_id})
        username = user['username'] if user else data.get('username', 'Unknown')
        
        mode = data.get('mode', 'quick_play')
        
        sid = request.sid
        
        # Check if there's a waiting player
        if waiting_players:
            # Match with waiting player
            opponent_sid = waiting_players.pop(0)
            opponent_id = connected_users.get(opponent_sid)
            
            if opponent_id:
                # Create game
                game_id = str(uuid.uuid4())
                room = f"game_{game_id}"
                
                # Join both players to room
                join_room(room, sid=sid)
                join_room(room, sid=opponent_sid)
                
                # Create game data
                game_data = {
                    'game_id': game_id,
                    'mode': mode,
                    'opponent_type': 'user',
                    'players': [user_id, opponent_id],
                    'player_sids': {user_id: sid, opponent_id: opponent_sid},
                    'room': room,
                    'status': 'active',
                    'rounds': [],
                    'current_round': 1,
                    'scores': {'player1': 0, 'player2': 0, 'ties': 0},
                    'pending_moves': {},
                    'created_at': datetime.utcnow()
                }
                
                active_games[game_id] = game_data
                
                # Notify both players
                emit('game_found', {
                    'game_id': game_id,
                    'opponent': opponent_id,
                    'player_number': 1
                }, room=sid)
                
                emit('game_found', {
                    'game_id': game_id,
                    'opponent': user_id,
                    'player_number': 2
                }, room=opponent_sid)
                
                print(f"Game created: {game_id} - {user_id} vs {opponent_id}")
            else:
                # Opponent disconnected, add to queue
                waiting_players.append(sid)
                emit('waiting_for_opponent', {'message': 'Searching for opponent...'})
        else:
            # No waiting players, add to queue
            waiting_players.append(sid)
            emit('waiting_for_opponent', {'message': 'Searching for opponent...'})
    
    @socketio.on('cancel_matchmaking')
    def handle_cancel_matchmaking():
        """Player cancels matchmaking"""
        sid = request.sid
        if sid in waiting_players:
            waiting_players.remove(sid)
        emit('matchmaking_cancelled', {'message': 'Matchmaking cancelled'})
    
    @socketio.on('submit_move')
    def handle_submit_move(data):
        """Player submits a move in online game"""
        if request.sid not in connected_users:
            return
            
        user_id = connected_users[request.sid]
        game_id = data.get('game_id')
        move = data.get('move', '').lower()
        
        # Validate move
        if not validate_move(move):
            emit('error', {'message': 'Invalid move'})
            return
        
        # Get game
        game_data = active_games.get(game_id)
        if not game_data:
            emit('error', {'message': 'Game not found'})
            return
        
        # Check if user is in game
        if user_id not in game_data['players']:
            emit('error', {'message': 'Not a player in this game'})
            return
        
        # Store move
        game_data['pending_moves'][user_id] = move
        
        # Notify player their move was received
        emit('move_submitted', {'message': 'Move submitted, waiting for opponent...'})
        
        # Check if both players have submitted moves
        if len(game_data['pending_moves']) == 2:
            # Process round
            player1_id = game_data['players'][0]
            player2_id = game_data['players'][1]
            
            player1_move = game_data['pending_moves'][player1_id]
            player2_move = game_data['pending_moves'][player2_id]
            
            # Determine winner
            winner = determine_winner(player1_move, player2_move)
            
            # Create round result
            round_result = {
                'round_number': game_data['current_round'],
                'player1_move': player1_move,
                'player2_move': player2_move,
                'winner': winner,
                'timestamp': datetime.utcnow()
            }
            
            # Update scores
            if winner == 'player1':
                game_data['scores']['player1'] += 1
            elif winner == 'player2':
                game_data['scores']['player2'] += 1
            else:
                game_data['scores']['ties'] += 1
            
            # Add round to game
            game_data['rounds'].append(round_result)
            game_data['current_round'] += 1
            game_data['pending_moves'] = {}
            
            # Check if game should end
            game_finished = should_end_game(game_data)
            if game_finished:
                game_data['status'] = 'finished'
            
            # Broadcast round result to both players
            emit('round_result', {
                'round_result': {
                    'round_number': round_result['round_number'],
                    'your_move': player1_move,
                    'opponent_move': player2_move,
                    'winner': winner,
                    'scores': game_data['scores']
                },
                'game_finished': game_finished
            }, room=game_data['player_sids'][player1_id])
            
            emit('round_result', {
                'round_result': {
                    'round_number': round_result['round_number'],
                    'your_move': player2_move,
                    'opponent_move': player1_move,
                    'winner': 'player1' if winner == 'player2' else ('player2' if winner == 'player1' else 'tie'),
                    'scores': game_data['scores']
                },
                'game_finished': game_finished
            }, room=game_data['player_sids'][player2_id])
            
            # If game finished, save to database
            if game_finished:
                save_game_to_db(game_id, game_data)
                del active_games[game_id]
                print(f"Game finished: {game_id}")
    
    @socketio.on('leave_game')
    def handle_leave_game(data):
        """Player leaves an active game"""
        if request.sid not in connected_users:
            return

        user_id = connected_users[request.sid]
        game_id = data.get('game_id')
        
        game_data = active_games.get(game_id)
        if game_data:
            # Notify other player
            emit('opponent_left', {
                'message': 'Opponent left the game'
            }, room=game_data['room'])
            
            # Save game as abandoned
            save_abandoned_game(game_id, game_data)
            
            # Clean up
            leave_room(game_data['room'])
            del active_games[game_id]

def should_end_game(game_data):
    """Check if game should end based on mode"""
    mode = game_data['mode']
    scores = game_data['scores']
    
    if mode == 'quick_play':
        return len(game_data['rounds']) >= 1
    elif mode == 'best_of_3':
        return scores['player1'] >= 2 or scores['player2'] >= 2
    elif mode == 'best_of_5':
        return scores['player1'] >= 3 or scores['player2'] >= 3
    elif mode == 'best_of_7':
        return scores['player1'] >= 4 or scores['player2'] >= 4
    
    return False

def save_game_to_db(game_id, game_data):
    """Save completed game to database"""
    db = get_db()
    
    # Prepare game document
    game_doc = {
        'game_id': game_id,
        'mode': game_data['mode'],
        'opponent_type': 'user',
        'players': game_data['players'],
        'status': 'finished',
        'rounds': game_data['rounds'],
        'scores': game_data['scores'],
        'created_at': game_data['created_at'],
        'finished_at': datetime.utcnow()
    }
    
    db.games.insert_one(game_doc)
    
    # Update player stats
    for player_id in game_data['players']:
        update_player_stats(db, player_id, game_data)

def save_abandoned_game(game_id, game_data):
    """Save abandoned game to database"""
    db = get_db()
    
    game_doc = {
        'game_id': game_id,
        'mode': game_data['mode'],
        'opponent_type': 'user',
        'players': game_data['players'],
        'status': 'abandoned',
        'rounds': game_data['rounds'],
        'scores': game_data['scores'],
        'created_at': game_data['created_at'],
        'abandoned_at': datetime.utcnow()
    }
    
    db.games.insert_one(game_doc)

def update_player_stats(db, user_id, game_data):
    """Update player statistics after game"""
    player_index = game_data['players'].index(user_id)
    player_key = f'player{player_index + 1}'
    opponent_key = 'player2' if player_key == 'player1' else 'player1'
    
    player_score = game_data['scores'][player_key]
    opponent_score = game_data['scores'][opponent_key]
    
    won = player_score > opponent_score
    lost = player_score < opponent_score
    tied = player_score == opponent_score
    
    # Update user stats
    db.users.update_one(
        {'firebase_uid': user_id},
        {
            '$inc': {
                'stats.total_games': 1,
                'stats.wins': 1 if won else 0,
                'stats.losses': 1 if lost else 0,
                'stats.ties': 1 if tied else 0
            },
            '$set': {'updated_at': datetime.utcnow()}
        }
    )
    
    # Recalculate win rate
    user = db.users.find_one({'firebase_uid': user_id})
    if user:
        if 'stats' in user:
            total_games = user['stats'].get('total_games', 0)
            wins = user['stats'].get('wins', 0)
            win_rate = (wins / total_games * 100) if total_games > 0 else 0
        else:
            win_rate = 0
            wins = 0
            total_games = 0
            
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
