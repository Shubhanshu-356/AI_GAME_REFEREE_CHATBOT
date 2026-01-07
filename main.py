"""
Main CLI interface for Rock-Paper-Scissors-Plus
Simple conversational loop as required by PDF
FIXED: Play again option now works correctly
"""

import os
from dotenv import load_dotenv
from game_referee import GameReferee


def print_header():
    """Print game header"""
    print("=" * 60)
    print("🎮  ROCK-PAPER-SCISSORS-PLUS AI REFEREE  🎮")
    print("=" * 60)
    print()


def main():
    """
    Main game loop.
    
    Requirements satisfied:
    - Simple conversational loop (PDF requirement)
    - CLI interface (PDF requirement)
    - No long-running server (PDF requirement)
    """
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Check if API key exists
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found!")
        print()
        print("Please create a .env file with your API key:")
        print("GOOGLE_API_KEY=your_key_here")
        print()
        print("Get your key from: https://aistudio.google.com/apikey")
        return
    
    # Print header
    print_header()
    
    # Initialize AI referee
    try:
        referee = GameReferee(api_key)
    except Exception as e:
        print(f"❌ Error initializing game: {e}")
        return
    
    # Start game
    print(referee.start_game())
    print()
    
    # Main game loop
    while True:
        # Get user input
        user_input = input("Your move: ").strip()
        
        # Handle empty input
        if not user_input:
            print("Please enter a move!")
            print()
            continue
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            print()
            print("Thanks for playing! Goodbye! 👋")
            print()
            break
        
        # Process user input through AI referee
        print()
        try:
            response = referee.process_user_input(user_input)
            print(response)
            print()
            
            # FIXED: Check if game ended properly
            # Look for "GAME OVER!" which appears in all end scenarios
            if "GAME OVER!" in response:
                # Ask if they want to play again
                play_again = input("Play again? (yes/no): ").strip().lower()
                print()
                
                if play_again in ['yes', 'y', 'yeah', 'yep', 'sure']:
                    # Start new game
                    print("=" * 60)
                    print(referee.start_game())
                    print()
                else:
                    print("Thanks for playing! Goodbye! 👋")
                    print()
                    break
                    
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print()
            print()
            print("Game interrupted. Goodbye! 👋")
            print()
            break
        except Exception as e:
            # Handle any errors
            print(f"❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")
            print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Goodbye! 👋")
        print()
    except Exception as e:
        print(f"❌ Fatal error: {e}")