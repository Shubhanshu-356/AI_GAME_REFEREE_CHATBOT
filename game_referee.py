"""
AI Game Referee using Google ADK
This is the agent that understands user intent and generates responses.

Architecture (as required by PDF):
1. Intent Understanding: AI parses what user wants to do
2. Game Logic: Tools execute the actual game rules
3. Response Generation: AI creates natural language output
"""

from google import genai
from google.genai import types
from game_tools import FUNCTION_MAP, get_game_state


class GameReferee:
    """
    AI Game Referee Agent using Google ADK.
    Simplified version that works reliably.
    """
    
    def __init__(self, api_key: str):
        """Initialize the AI referee"""
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"  # More stable model
        
        # System prompt
        self.system_prompt = """You are an AI Game Referee for Rock-Paper-Scissors-Plus.

GAME RULES (explain in ≤5 lines when starting):
• Best of 3 rounds - win 2+ rounds to win
• Valid moves: rock, paper, scissors, bomb
• Bomb beats all moves (bomb vs bomb = draw)
• Each player can use bomb ONCE per game
• Invalid input wastes the round

YOUR JOB:
1. For each user move, determine if it's valid
2. Generate a bot move
3. Determine who wins the round
4. Update scores
5. Provide clear feedback

OUTPUT FORMAT (after each round):
Round X/3
Your move: [move]
Bot's move: [move]
Result: [who won and why]
Score: You X - Bot Y

After 3 rounds, clearly show: "You WIN!" or "Bot WINS!" or "It's a DRAW!"
Be friendly and concise."""
        
    def start_game(self) -> str:
        """Start a new game"""
        # Reset game using tools
        from game_tools import reset_game
        reset_game()
        
        # Generate welcome message
        prompt = "Start a new Rock-Paper-Scissors-Plus game. Explain the rules in 5 lines or less and ask for the first move."
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=0.7
            )
        )
        
        return response.text
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and play a round"""
        from game_tools import validate_move, get_bot_move, resolve_round, update_game_state
        
        # Get current game state
        state = get_game_state()
        
        # Check if game is over
        if state['game_over']:
            return "Game is already over! Type 'quit' to exit or restart."
        
        # Validate user move
        validation = validate_move(user_input, is_user=True)
        
        if not validation['valid']:
            # Invalid move - waste the round
            update_game_state(
                user_move=user_input,
                bot_move=None,
                round_winner="invalid",
                invalid_input=True
            )
            
            state = get_game_state()
            
            # Build response
            response = f"""Round {state['current_round']}/3
Your move: {user_input} (INVALID)
Bot's move: -
Result: Invalid move! This round is wasted.
{validation['reason']}

Score: You {state['user_score']} - Bot {state['bot_score']}"""
            
            # Check if game ended
            if state['game_over']:
                response += self._get_final_result(state)
            
            return response
        
        # Get bot's move
        bot_move = get_bot_move()
        
        # Resolve round
        result = resolve_round(validation['move'], bot_move)
        
        # Update state
        update_game_state(
            user_move=validation['move'],
            bot_move=bot_move,
            round_winner=result['winner'],
            invalid_input=False
        )
        
        # Get updated state
        state = get_game_state()
        
        # Build response
        winner_text = self._get_winner_text(result['winner'], validation['move'], bot_move)
        
        response = f"""Round {state['current_round']}/3
Your move: {validation['move']}
Bot's move: {bot_move}
Result: {winner_text}

Score: You {state['user_score']} - Bot {state['bot_score']}"""
        
        # Check if game ended
        if state['game_over']:
            response += self._get_final_result(state)
        
        return response
    
    def _get_winner_text(self, winner: str, user_move: str, bot_move: str) -> str:
        """Generate descriptive text for round winner"""
        if winner == "draw":
            return "It's a draw! Both played the same move."
        elif winner == "user":
            if user_move == "bomb":
                return "You win! Bomb destroys everything!"
            elif user_move == "rock":
                return "You win! Rock crushes scissors."
            elif user_move == "paper":
                return "You win! Paper covers rock."
            elif user_move == "scissors":
                return "You win! Scissors cuts paper."
        else:  # bot wins
            if bot_move == "bomb":
                return "Bot wins! Bomb destroys everything!"
            elif bot_move == "rock":
                return "Bot wins. Rock crushes scissors."
            elif bot_move == "paper":
                return "Bot wins. Paper covers rock."
            elif bot_move == "scissors":
                return "Bot wins. Scissors cuts paper."
        return f"{winner} wins!"
    
    def _get_final_result(self, state: dict) -> str:
        """Generate final game result"""
        result = "\n\n" + "="*50 + "\n"
        result += "GAME OVER!\n"
        result += "="*50 + "\n"
        
        if state['user_score'] > state['bot_score']:
            result += "🎉 You WIN! 🎉\n"
        elif state['bot_score'] > state['user_score']:
            result += "😔 Bot WINS! 😔\n"
        else:
            result += "🤝 It's a DRAW! 🤝\n"
        
        result += f"Final Score: You {state['user_score']} - Bot {state['bot_score']}\n"
        result += "="*50
        
        return result