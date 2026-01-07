"""
Game State Management for Rock-Paper-Scissors-Plus
Tracks all game state: rounds, scores, bomb usage, etc.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GameState:
    """
    Complete game state for Rock-Paper-Scissors-Plus.
    
    This stores all information needed to track the game across turns.
    State persists outside of prompts (requirement from PDF).
    """
    # Round tracking
    current_round: int = 0  # 0-3
    
    # Scores
    user_score: int = 0
    bot_score: int = 0
    
    # Bomb usage tracking (each player can use once)
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    
    # Game status
    game_over: bool = False
    
    # Last round info (for displaying results)
    last_user_move: Optional[str] = None
    last_bot_move: Optional[str] = None
    last_round_result: Optional[str] = None  # "user", "bot", "draw", or "invalid"
    
    def to_dict(self) -> dict:
        """
        Convert state to dictionary for tool usage.
        ADK tools work with dictionaries.
        
        Returns:
            Dictionary representation of game state
        """
        return {
            "current_round": self.current_round,
            "user_score": self.user_score,
            "bot_score": self.bot_score,
            "user_bomb_used": self.user_bomb_used,
            "bot_bomb_used": self.bot_bomb_used,
            "game_over": self.game_over,
            "last_user_move": self.last_user_move,
            "last_bot_move": self.last_bot_move,
            "last_round_result": self.last_round_result
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GameState':
        """
        Create GameState from dictionary.
        
        Args:
            data: Dictionary with game state data
            
        Returns:
            GameState object
        """
        return cls(**data)
    
    def reset(self) -> None:
        """Reset all state for a new game"""
        self.current_round = 0
        self.user_score = 0
        self.bot_score = 0
        self.user_bomb_used = False
        self.bot_bomb_used = False
        self.game_over = False
        self.last_user_move = None
        self.last_bot_move = None
        self.last_round_result = None