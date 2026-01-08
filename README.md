# Rock-Paper-Scissors-Plus: AI Referee

A command-line Rock-Paper-Scissors game featuring a strategic "Bomb" mechanic and an AI Referee powered by the **Google GenAI ADK**. 

This project demonstrates a clear separation of concerns: an AI agent handles natural language understanding (intent), while deterministic Python functions handle the game logic and state management.

## 🎮 How to Play

The game runs in your terminal. You play against a Bot for **3 rounds**.

### The Moves
* 🪨 **Rock:** Beats Scissors
* 📄 **Paper:** Beats Rock
* ✂️ **Scissors:** Beats Paper
* 💣 **Bomb:** Beats Everything (except another Bomb)

### The Rules
1.  **Best of 3:** The game ends automatically after 3 rounds.
2.  **Bomb Limit:** Each player (You and the Bot) can use the **Bomb** only **once** per game.
3.  **Bomb vs. Bomb:** If both players use a Bomb, it is a Draw.
4.  **Invalid Input:** If you type a move that isn't recognized, you **waste your turn** and lose the round.

---

## 🛠️ Installation & Setup

### Prerequisites
* **Python 3.10+**
* A **Google AI API Key** (Get one [here](https://aistudio.google.com/apikey))

### Quick Start
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Shubhanshu-356/AI_GAME_REFEREE_CHATBOT.git
    cd AI_GAME_REFEREE_CHATBOT
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    Create a `.env` file in the root directory and add your key:
    ```ini
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

4.  **Run the Game:**
    ```bash
    python main.py
    ```

---

## 🏗️ Technical Architecture

This project strictly separates **Intent Understanding** (AI) from **Game Logic** (Code).

### 1. The Agent (Intent)
Located in `game_referee.py`.
The AI listens to your input (e.g., "I choose rock" or "Deploy the bomb") and translates it into structured tool calls. It does **not** manage the score or rules itself.

### 2. The Tools (Logic)
Located in `game_tools.py`.
Six explicit Python functions handle the rules.
* `validate_move()`: Checks if the move is legal (and if you still have a Bomb).
* `resolve_round()`: Mathematically determines the winner.
* `update_game_state()`: Updates the global state.

### 3. State Management
Located in `game_state.py`.
The game state (scores, round number, bomb usage) is stored in a Python DataClass, **not** in the LLM's context window. This ensures the game cannot "hallucinate" the score.

---

## 📂 Project Structure

```text
rock-paper-scissors-ai/
├── main.py            # Entry point (Run this)
├── game_referee.py    # AI Agent & Prompt definitions
├── game_tools.py      # Core game logic & tools
├── game_state.py      # State data structure
├── .env               # API Key storage (Create this)
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
