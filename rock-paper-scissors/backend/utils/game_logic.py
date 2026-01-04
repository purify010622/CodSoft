"""
Core game logic for Rock Paper Scissors
Determines winners and validates moves
"""

VALID_MOVES = ['rock', 'paper', 'scissors']

def determine_winner(player1_move, player2_move):
    """
    Determine the winner of a round
    
    Args:
        player1_move: Player 1's move (rock/paper/scissors)
        player2_move: Player 2's move (rock/paper/scissors)
    
    Returns:
        str: 'player1', 'player2', or 'tie'
    """
    if player1_move == player2_move:
        return 'tie'
    
    winning_combinations = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    
    if winning_combinations[player1_move] == player2_move:
        return 'player1'
    else:
        return 'player2'

def validate_move(move):
    """
    Validate if a move is valid
    
    Args:
        move: The move to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    return move.lower() in VALID_MOVES

def get_computer_move():
    """
    Generate a random move for the computer
    
    Returns:
        str: Random move (rock/paper/scissors)
    """
    import random
    return random.choice(VALID_MOVES)

def calculate_game_result(rounds, mode='best_of'):
    """
    Calculate the final game result based on rounds
    
    Args:
        rounds: List of round results
        mode: Game mode ('best_of' or 'endless')
    
    Returns:
        dict: Game result with winner and scores
    """
    player1_score = sum(1 for r in rounds if r['winner'] == 'player1')
    player2_score = sum(1 for r in rounds if r['winner'] == 'player2')
    ties = sum(1 for r in rounds if r['winner'] == 'tie')
    
    if player1_score > player2_score:
        winner = 'player1'
    elif player2_score > player1_score:
        winner = 'player2'
    else:
        winner = 'tie'
    
    return {
        'winner': winner,
        'player1_score': player1_score,
        'player2_score': player2_score,
        'ties': ties,
        'total_rounds': len(rounds)
    }
