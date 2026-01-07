"""
Game Tools for Rock-Paper-Scissors-Plus
All game logic lives in these tools.
State must NOT live only in prompts - it lives here.
"""

import random
from typing import Dict, Any
from game_state import GameState


# Global game state - persists across tool calls
# This satisfies "State must persist across turns" requirement
game_state = GameState()


def validate_move(move: str, is_user: bool) -> Dict[str, Any]:
    """
    Tool 1: Validates if a move is legal according to game rules.
    
    Requirements satisfied:
    - Validates user input (PDF requirement)
    - Checks bomb usage constraint (PDF requirement)
    
    Args:
        move: The move to validate (rock/paper/scissors/bomb)
        is_user: True if validating user move, False for bot
    
    Returns:
        Dictionary with:
            - valid: bool (is the move legal?)
            - reason: str (why valid or invalid)
            - move: str (normalized move name, if valid)
    """
    valid_moves = ["rock", "paper", "scissors", "bomb"]
    move = move.lower().strip()
    
    # Check if move is in valid list
    if move not in valid_moves:
        return {
            "valid": False,
            "reason": f"Invalid move '{move}'. Valid moves: rock, paper, scissors, bomb"
        }
    
    # Check bomb usage constraint
    if move == "bomb":
        if is_user and game_state.user_bomb_used:
            return {
                "valid": False,
                "reason": "You already used your bomb this game"
            }
        if not is_user and game_state.bot_bomb_used:
            return {
                "valid": False,
                "reason": "Bot already used bomb"
            }
    
    return {
        "valid": True,
        "reason": "Move is valid",
        "move": move
    }


def resolve_round(user_move: str, bot_move: str) -> Dict[str, Any]:
    """
    Tool 2: Determines the winner of a round based on game rules.
    
    Requirements satisfied:
    - Decides round outcome (PDF requirement)
    - Implements all game rules including bomb logic
    
    Args:
        user_move: User's move
        bot_move: Bot's move
    
    Returns:
        Dictionary with:
            - winner: str ("user", "bot", or "draw")
            - user_move: str
            - bot_move: str
    """
    # Bomb logic (bomb beats all)
    if user_move == "bomb" and bot_move == "bomb":
        result = "draw"
    elif user_move == "bomb":
        result = "user"
    elif bot_move == "bomb":
        result = "bot"
    # Standard Rock-Paper-Scissors logic
    elif user_move == bot_move:
        result = "draw"
    elif (
        (user_move == "rock" and bot_move == "scissors") or
        (user_move == "scissors" and bot_move == "paper") or
        (user_move == "paper" and bot_move == "rock")
    ):
        result = "user"
    else:
        result = "bot"
    
    return {
        "winner": result,
        "user_move": user_move,
        "bot_move": bot_move
    }


def update_game_state(
    user_move: str = None,
    bot_move: str = None,
    round_winner: str = None,
    invalid_input: bool = False
) -> Dict[str, Any]:
    """
    Tool 3: Updates the game state after a round.
    
    Requirements satisfied:
    - Tracks round count (PDF requirement)
    - Tracks score (PDF requirement)
    - Handles invalid input (wastes round - PDF requirement)
    - Ends game after 3 rounds (PDF requirement)
    
    Args:
        user_move: User's move this round
        bot_move: Bot's move this round
        round_winner: Winner of round ("user", "bot", "draw")
        invalid_input: Whether user provided invalid input
    
    Returns:
        Updated game state as dictionary
    """
    global game_state
    
    # Increment round counter
    game_state.current_round += 1
    
    # Store moves
    game_state.last_user_move = user_move
    game_state.last_bot_move = bot_move
    
    # Update scores (invalid input wastes the round)
    if not invalid_input:
        if round_winner == "user":
            game_state.user_score += 1
            game_state.last_round_result = "user"
        elif round_winner == "bot":
            game_state.bot_score += 1
            game_state.last_round_result = "bot"
        else:
            game_state.last_round_result = "draw"
        
        # Mark bomb as used
        if user_move == "bomb":
            game_state.user_bomb_used = True
        if bot_move == "bomb":
            game_state.bot_bomb_used = True
    else:
        game_state.last_round_result = "invalid"
    
    # Check if game should end (after 3 rounds)
    if game_state.current_round >= 3:
        game_state.game_over = True
    
    return game_state.to_dict()


def get_game_state() -> Dict[str, Any]:
    """
    Tool 4: Returns current game state.
    
    Requirements satisfied:
    - Allows checking state without modifying it
    
    Returns:
        Current game state as dictionary
    """
    return game_state.to_dict()


def get_bot_move() -> str:
    """
    Tool 5: Generates bot's move for the current round.
    
    Requirements satisfied:
    - Bot plays against user (PDF requirement)
    - Bot has strategy and uses bomb
    
    Returns:
        Bot's chosen move (string)
    """
    available_moves = ["rock", "paper", "scissors"]
    
    # Bot uses bomb strategically (if available and in round 2 or 3)
    if not game_state.bot_bomb_used and game_state.current_round >= 1:
        # 30% chance to use bomb when available
        if random.random() < 0.3:
            return "bomb"
    
    # Otherwise, random choice from standard moves
    return random.choice(available_moves)


def reset_game() -> Dict[str, Any]:
    """
    Tool 6: Resets the game state for a new game.
    
    Requirements satisfied:
    - Allows playing multiple games
    
    Returns:
        Reset game state as dictionary
    """
    global game_state
    game_state.reset()
    return game_state.to_dict()


# ADK Tool Definitions
# These tell Google ADK about our tools so the AI can use them
TOOLS = [
    {
        "function_declarations": [
            {
                "name": "validate_move",
                "description": "Validates if a player's move is legal according to game rules. Checks if move is valid and if bomb can be used.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "move": {
                            "type": "string",
                            "description": "The move to validate (rock, paper, scissors, or bomb)"
                        },
                        "is_user": {
                            "type": "boolean",
                            "description": "True if validating user move, False for bot"
                        }
                    },
                    "required": ["move", "is_user"]
                }
            },
            {
                "name": "resolve_round",
                "description": "Determines the winner of a round based on both players' moves using game rules.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_move": {
                            "type": "string",
                            "description": "User's move for this round"
                        },
                        "bot_move": {
                            "type": "string",
                            "description": "Bot's move for this round"
                        }
                    },
                    "required": ["user_move", "bot_move"]
                }
            },
            {
                "name": "update_game_state",
                "description": "Updates the game state after a round completes. Tracks scores, rounds, and handles invalid input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_move": {
                            "type": "string",
                            "description": "User's move this round"
                        },
                        "bot_move": {
                            "type": "string",
                            "description": "Bot's move this round"
                        },
                        "round_winner": {
                            "type": "string",
                            "description": "Winner of the round: 'user', 'bot', or 'draw'"
                        },
                        "invalid_input": {
                            "type": "boolean",
                            "description": "Whether the round was wasted due to invalid input"
                        }
                    },
                    "required": ["round_winner"]
                }
            },
            {
                "name": "get_game_state",
                "description": "Retrieves the current game state including scores, round number, and bomb usage.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_bot_move",
                "description": "Generates the bot's move for the current round using strategy.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "reset_game",
                "description": "Resets the game state to start a new game.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    }
]

# Function mapping for execution
# Maps function names to actual Python functions
FUNCTION_MAP = {
    "validate_move": validate_move,
    "resolve_round": resolve_round,
    "update_game_state": update_game_state,
    "get_game_state": get_game_state,
    "get_bot_move": get_bot_move,
    "reset_game": reset_game
}