#!/usr/bin/env python3
"""
Terminal Snake Game - Windows Compatible
A classic Snake game that works perfectly on Windows!
Use WASD keys to control the snake.
"""

import os
import time
import random
import msvcrt
from enum import Enum

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class SnakeGame:
    def __init__(self, width=50, height=20):
        self.width = width
        self.height = height
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        
        # Initialize snake in the center
        center_y, center_x = height // 2, width // 2
        self.snake = [(center_y, center_x), (center_y, center_x - 1), (center_y, center_x - 2)]
        self.direction = Direction.RIGHT
        
        # Place first food
        self.food = self.place_food()
        
        # Game speed (lower = faster)
        self.speed = 0.15  # seconds between moves
        
    def place_food(self):
        """Place food at a random location not occupied by the snake."""
        while True:
            food_pos = (random.randint(1, self.height - 2), 
                       random.randint(1, self.width - 2))
            if food_pos not in self.snake:
                return food_pos
    
    def move_snake(self):
        """Move the snake in the current direction."""
        if self.paused or self.game_over:
            return
            
        head_y, head_x = self.snake[0]
        dy, dx = self.direction.value
        new_head = (head_y + dy, head_x + dx)
        
        # Check wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.height - 1 or
            new_head[1] <= 0 or new_head[1] >= self.width - 1):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.place_food()
            # Increase speed slightly (make game faster)
            if self.speed > 0.08:
                self.speed = max(0.08, self.speed - 0.005)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """Change snake direction, preventing reverse direction."""
        # Prevent moving directly backwards
        current_dy, current_dx = self.direction.value
        new_dy, new_dx = new_direction.value
        
        if (current_dy, current_dx) != (-new_dy, -new_dx):
            self.direction = new_direction
    
    def reset_game(self):
        """Reset the game to initial state."""
        if self.score > self.high_score:
            self.high_score = self.score
        
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = 0.15
        
        # Reset snake position
        center_y, center_x = self.height // 2, self.width // 2
        self.snake = [(center_y, center_x), (center_y, center_x - 1), (center_y, center_x - 2)]
        self.direction = Direction.RIGHT
        self.food = self.place_food()

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_game(game):
    """Draw the game state to the console."""
    clear_screen()
    
    # Create the game board
    board = [[' ' for _ in range(game.width)] for _ in range(game.height)]
    
    # Draw border
    for i in range(game.height):
        for j in range(game.width):
            if i == 0 or i == game.height - 1 or j == 0 or j == game.width - 1:
                board[i][j] = '█'
    
    # Draw snake
    for i, (y, x) in enumerate(game.snake):
        if i == 0:  # Head
            board[y][x] = '●'
        else:  # Body
            board[y][x] = '○'
    
    # Draw food
    food_y, food_x = game.food
    board[food_y][food_x] = '★'
    
    # Print the board
    for row in board:
        print(''.join(row))
    
    # Print score and info
    print(f"\n🐍 Score: {game.score}  🏆 High Score: {game.high_score}  📏 Length: {len(game.snake)}")
    print("─" * 70)
    print("🎮 Controls: W(Up) A(Left) S(Down) D(Right) | P(Pause) | R(Restart) | Q(Quit)")
    
    if game.paused:
        print("\n⏸️  PAUSED - Press P to continue")
    
    if game.game_over:
        print(f"\n💀 GAME OVER! Final Score: {game.score}")
        print("🔄 Press R to restart or Q to quit")
        if game.score == game.high_score and game.score > 0:
            print("🎉 NEW HIGH SCORE! Congratulations!")

def get_key_input():
    """Get keyboard input without blocking."""
    if msvcrt.kbhit():
        try:
            key = msvcrt.getch()
            # Handle special keys (like arrow keys)
            if key == b'\xe0':
                # Arrow key pressed, get the actual key code
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    return 'w'
                elif key == b'P':  # Down arrow
                    return 's'
                elif key == b'K':  # Left arrow
                    return 'a'
                elif key == b'M':  # Right arrow
                    return 'd'
            else:
                # Regular key
                return key.decode('utf-8').lower()
        except UnicodeDecodeError:
            return None
    return None

def main():
    """Main game function."""
    print("🐍✨ TERMINAL SNAKE GAME ✨🐍")
    print("=" * 50)
    print("Get ready to play the classic Snake game!")
    print("Eat the stars (★) to grow and increase your score!")
    print("Avoid hitting walls or yourself!")
    print("\nStarting in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("GO! 🚀")
    time.sleep(0.5)
    
    # Initialize game
    game = SnakeGame()
    last_move_time = time.time()
    
    # Game loop
    while True:
        current_time = time.time()
        
        # Handle input
        key = get_key_input()
        
        if key == 'q':
            break
        elif key == 'r':
            game.reset_game()
        elif key == 'p':
            game.paused = not game.paused
        elif key == 'w' and not game.game_over:
            game.change_direction(Direction.UP)
        elif key == 's' and not game.game_over:
            game.change_direction(Direction.DOWN)
        elif key == 'a' and not game.game_over:
            game.change_direction(Direction.LEFT)
        elif key == 'd' and not game.game_over:
            game.change_direction(Direction.RIGHT)
        
        # Move snake based on game speed
        if current_time - last_move_time > game.speed:
            game.move_snake()
            last_move_time = current_time
        
        # Draw everything
        draw_game(game)
        
        # Small delay to prevent excessive CPU usage
        time.sleep(0.05)

if __name__ == "__main__":
    try:
        main()
        print("\n🎮 Thanks for playing Snake! Hope you had an awesome time!")
        print("👋 See you next time!")
        
    except KeyboardInterrupt:
        clear_screen()
        print("🐍 Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please make sure you're running this on Windows with Python 3.6+")
    
    # Wait for user to press any key before closing
    print("\nPress any key to exit...")
    try:
        msvcrt.getch()
    except:
        input()  # Fallback for non-Windows systems
