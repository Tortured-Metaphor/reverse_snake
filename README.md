# 🐍 Reverse Snake - Retro Edition

A unique twist on the classic Snake game where eating numbered food makes the snake switch between moving head-first and tail-first! The snake visually flips around each time it eats, creating a challenging and dynamic gameplay experience.

## 🎮 How to Play

### Objective
Control the snake to eat numbered food items. Each time you eat food:
- Your snake reverses direction (head becomes tail, tail becomes head)
- The snake grows longer
- Your score increases by the food's number value

### Controls
- **Arrow Keys**: Move the snake (↑ ↓ ← →)
- **Space**: Restart game (when game over)
- **Escape**: Quit game

### Game Mechanics
- **Forward Mode**: Snake moves normally (green head)
- **Reverse Mode**: Snake moves tail-first (cyan head)
- Each food item has a number (1-9) that adds to your score
- Avoid hitting walls or your own body
- The snake alternates between forward and reverse modes with each food eaten

## 🚀 Installation & Setup

### Prerequisites
- Python 3.6 or higher
- pygame library

### Install Dependencies
```bash
pip install pygame
```

### Run the Game
```bash
python3 reverse_snake.py
```

Or make it executable and run directly:
```bash
chmod +x reverse_snake.py
./reverse_snake.py
```

## 🎯 Features

- **Retro-style graphics** with neon colors and grid patterns
- **Visual mode indicator** showing forward/reverse state
- **Pulsing food effects** with numbered values
- **High score tracking** during session
- **Smooth animations** at classic 10 FPS gameplay
- **Game over screen** with restart functionality

## 🎨 Visual Elements

- **Green head**: Normal forward movement
- **Cyan head**: Reverse movement mode  
- **Pulsing red food**: Numbered food items (1-9)
- **Grid background**: Retro aesthetic
- **Mode indicator**: Shows current movement direction

## 🏆 Scoring

Your score increases by the number value on each food item you eat (1-9 points). Try to achieve the highest score possible while managing the constantly switching movement direction!

## 🛠 Technical Details

- Built with Python and Pygame
- 800x600 window resolution
- 20px cell size grid
- 10 FPS classic snake gameplay speed
- Object-oriented design with Snake, Food, and Game classes
