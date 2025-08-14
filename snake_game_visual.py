#!/usr/bin/env python3
"""
🐍✨ VISUAL SNAKE GAME ✨🐍
A stunning, colorful Snake game with amazing graphics!
Use WASD or Arrow Keys to control the snake.
"""

import os
import time
import random
import msvcrt
from enum import Enum

# ANSI Color codes for beautiful terminal colors
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class SnakeGame:
    def __init__(self, width=60, height=25):
        self.width = width
        self.height = height
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        self.frame_count = 0
        
        # Food colors for variety (initialize before placing food)
        self.food_colors = [
            f"{Colors.BRIGHT_RED}★{Colors.RESET}",
            f"{Colors.BRIGHT_YELLOW}⭐{Colors.RESET}",
            f"{Colors.BRIGHT_MAGENTA}✦{Colors.RESET}",
            f"{Colors.BRIGHT_CYAN}◆{Colors.RESET}",
        ]
        self.current_food_color = 0
        
        # Initialize snake in the center
        center_y, center_x = height // 2, width // 2
        self.snake = [(center_y, center_x), (center_y, center_x - 1), (center_y, center_x - 2)]
        self.direction = Direction.RIGHT
        
        # Place first food
        self.food = self.place_food()
        
        # Game speed (lower = faster)
        self.speed = 0.12
        
    def place_food(self):
        """Place food at a random location not occupied by the snake."""
        while True:
            food_pos = (random.randint(2, self.height - 3), 
                       random.randint(2, self.width - 3))
            if food_pos not in self.snake:
                self.current_food_color = random.randint(0, len(self.food_colors) - 1)
                return food_pos
    
    def move_snake(self):
        """Move the snake in the current direction."""
        if self.paused or self.game_over:
            return
            
        head_y, head_x = self.snake[0]
        dy, dx = self.direction.value
        new_head = (head_y + dy, head_x + dx)
        
        # Check wall collision
        if (new_head[0] <= 1 or new_head[0] >= self.height - 2 or
            new_head[1] <= 1 or new_head[1] >= self.width - 2):
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
            # Increase speed slightly
            if self.speed > 0.06:
                self.speed = max(0.06, self.speed - 0.003)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """Change snake direction, preventing reverse direction."""
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
        self.speed = 0.12
        self.frame_count = 0
        
        center_y, center_x = self.height // 2, self.width // 2
        self.snake = [(center_y, center_x), (center_y, center_x - 1), (center_y, center_x - 2)]
        self.direction = Direction.RIGHT
        self.food = self.place_food()

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_border(game):
    """Draw an animated, colorful border."""
    border_colors = [Colors.BRIGHT_BLUE, Colors.BRIGHT_CYAN, Colors.BRIGHT_MAGENTA]
    color = border_colors[(game.frame_count // 10) % len(border_colors)]
    
    border = f"{color}{'═' * game.width}{Colors.RESET}"
    print(f"{color}╔{border}╗{Colors.RESET}")
    
    for i in range(1, game.height - 1):
        print(f"{color}║{Colors.RESET}", end='')
        print(' ' * game.width, end='')
        print(f"{color}║{Colors.RESET}")
    
    print(f"{color}╚{border}╝{Colors.RESET}")

def draw_game(game):
    """Draw the game state with beautiful visuals."""
    clear_screen()
    game.frame_count += 1
    
    # Title with animation
    title_color = [Colors.BRIGHT_RED, Colors.BRIGHT_YELLOW, Colors.BRIGHT_GREEN, Colors.BRIGHT_CYAN, Colors.BRIGHT_MAGENTA]
    animated_title = ""
    title_text = "🐍 VISUAL SNAKE GAME 🐍"
    for i, char in enumerate(title_text):
        color = title_color[(game.frame_count + i) % len(title_color)]
        animated_title += f"{color}{char}{Colors.RESET}"
    
    print(f"{Colors.BOLD}{animated_title}{Colors.RESET}")
    print()
    
    # Create the game board
    board = [[' ' for _ in range(game.width)] for _ in range(game.height)]
    
    # Draw animated border
    border_chars = ['░', '▒', '▓', '█']
    border_char = border_chars[(game.frame_count // 5) % len(border_chars)]
    border_color = [Colors.BRIGHT_BLUE, Colors.BRIGHT_CYAN][game.frame_count // 8 % 2]
    
    for i in range(game.height):
        for j in range(game.width):
            if i == 0 or i == game.height - 1 or j == 0 or j == game.width - 1:
                board[i][j] = f"{border_color}{border_char}{Colors.RESET}"
    
    # Draw snake with gradient colors
    snake_colors = [
        f"{Colors.BRIGHT_GREEN}●{Colors.RESET}",  # Head
        f"{Colors.GREEN}●{Colors.RESET}",         # Neck
        f"{Colors.BRIGHT_GREEN}○{Colors.RESET}",  # Body
        f"{Colors.GREEN}○{Colors.RESET}",         # Body
    ]
    
    for i, (y, x) in enumerate(game.snake):
        if i == 0:  # Head with special animation
            head_chars = ['●', '◉', '●', '○']
            head_char = head_chars[(game.frame_count // 3) % len(head_chars)]
            board[y][x] = f"{Colors.BRIGHT_GREEN}{Colors.BOLD}{head_char}{Colors.RESET}"
        else:  # Body
            color_index = min(i - 1, len(snake_colors) - 1)
            board[y][x] = snake_colors[2 + (color_index % 2)]
    
    # Draw animated food
    food_y, food_x = game.food
    food_symbol = game.food_colors[game.current_food_color]
    # Make food pulse
    if game.frame_count % 6 < 3:
        food_symbol = f"{Colors.BOLD}{food_symbol}{Colors.RESET}"
    board[food_y][food_x] = food_symbol
    
    # Print the board
    for row in board:
        print(''.join(row))
    
    # Beautiful stats display
    print()
    stats_bg = Colors.BG_BLACK
    print(f"{stats_bg}{Colors.BRIGHT_WHITE}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
    
    score_text = f"🏆 SCORE: {Colors.BRIGHT_YELLOW}{game.score:04d}{Colors.RESET}"
    high_score_text = f"👑 HIGH: {Colors.BRIGHT_MAGENTA}{game.high_score:04d}{Colors.RESET}"
    length_text = f"📏 LENGTH: {Colors.BRIGHT_CYAN}{len(game.snake):02d}{Colors.RESET}"
    
    print(f"{stats_bg}{Colors.BRIGHT_WHITE}│ {score_text}    {high_score_text}    {length_text}      │{Colors.RESET}")
    print(f"{stats_bg}{Colors.BRIGHT_WHITE}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
    
    # Controls with colors
    print(f"\n{Colors.BRIGHT_WHITE}🎮 CONTROLS:{Colors.RESET}")
    print(f"  {Colors.BRIGHT_GREEN}W{Colors.RESET}↑  {Colors.BRIGHT_YELLOW}A{Colors.RESET}←  {Colors.BRIGHT_RED}S{Colors.RESET}↓  {Colors.BRIGHT_BLUE}D{Colors.RESET}→  "
          f"{Colors.BRIGHT_MAGENTA}P{Colors.RESET}⏸  {Colors.BRIGHT_CYAN}R{Colors.RESET}🔄  {Colors.BRIGHT_RED}Q{Colors.RESET}❌")
    
    # Game state messages with animations
    if game.paused:
        pause_msg = "⏸️  GAME PAUSED ⏸️"
        color = [Colors.BRIGHT_YELLOW, Colors.YELLOW][(game.frame_count // 8) % 2]
        print(f"\n{color}{Colors.BOLD}{pause_msg.center(60)}{Colors.RESET}")
        print(f"{Colors.BRIGHT_WHITE}Press P to continue{Colors.RESET}".center(60))
    
    if game.game_over:
        game_over_color = [Colors.BRIGHT_RED, Colors.RED][(game.frame_count // 5) % 2]
        print(f"\n{game_over_color}{Colors.BOLD}{'💀 GAME OVER! 💀'.center(60)}{Colors.RESET}")
        print(f"{Colors.BRIGHT_WHITE}Final Score: {Colors.BRIGHT_YELLOW}{game.score}{Colors.RESET}".center(60))
        print(f"{Colors.BRIGHT_GREEN}Press R to restart or Q to quit{Colors.RESET}".center(60))
        
        if game.score == game.high_score and game.score > 0:
            celebration = "🎉✨ NEW HIGH SCORE! ✨🎉"
            celebration_color = [Colors.BRIGHT_MAGENTA, Colors.BRIGHT_YELLOW, Colors.BRIGHT_GREEN]
            color = celebration_color[(game.frame_count // 4) % len(celebration_color)]
            print(f"\n{color}{Colors.BOLD}{celebration.center(60)}{Colors.RESET}")

def get_key_input():
    """Get keyboard input without blocking."""
    if msvcrt.kbhit():
        try:
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H': return 'w'
                elif key == b'P': return 's'
                elif key == b'K': return 'a'
                elif key == b'M': return 'd'
            else:
                return key.decode('utf-8').lower()
        except UnicodeDecodeError:
            return None
    return None

def show_intro():
    """Display a beautiful intro animation."""
    clear_screen()
    
    # Animated intro
    intro_frames = [
        f"{Colors.BRIGHT_RED}🐍",
        f"{Colors.BRIGHT_YELLOW}🐍✨",
        f"{Colors.BRIGHT_GREEN}🐍✨🎮",
        f"{Colors.BRIGHT_CYAN}🐍✨🎮✨",
        f"{Colors.BRIGHT_MAGENTA}🐍✨🎮✨🐍"
    ]
    
    for i in range(3):
        for frame in intro_frames:
            clear_screen()
            print(f"\n{Colors.BOLD}{Colors.BRIGHT_WHITE}{'═' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}{frame.center(60)}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}VISUAL SNAKE GAME{Colors.RESET}".center(60))
            print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}{'═' * 60}{Colors.RESET}")
            time.sleep(0.2)
    
    print(f"\n{Colors.BRIGHT_GREEN}🎯 Objective:{Colors.RESET} Eat the sparkling food to grow!")
    print(f"{Colors.BRIGHT_YELLOW}⚡ Warning:{Colors.RESET} Don't hit walls or yourself!")
    print(f"{Colors.BRIGHT_CYAN}🚀 Bonus:{Colors.RESET} Game speeds up as you improve!")
    
    print(f"\n{Colors.BRIGHT_MAGENTA}Starting in:{Colors.RESET}")
    for i in range(3, 0, -1):
        print(f"{Colors.BRIGHT_WHITE}{Colors.BOLD}{i}...{Colors.RESET}")
        time.sleep(1)
    print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}GO! 🚀{Colors.RESET}")
    time.sleep(0.5)

def main():
    """Main game function with enhanced visuals."""
    # Enable ANSI color support on Windows
    os.system('')
    
    show_intro()
    
    game = SnakeGame()
    last_move_time = time.time()
    
    while True:
        current_time = time.time()
        
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
        
        if current_time - last_move_time > game.speed:
            game.move_snake()
            last_move_time = current_time
        
        draw_game(game)
        time.sleep(0.03)  # Smooth animation

if __name__ == "__main__":
    try:
        main()
        clear_screen()
        print(f"\n{Colors.BRIGHT_MAGENTA}🎮 Thanks for playing Visual Snake! 🎮{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Hope you enjoyed the colorful experience! ✨{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}👋 See you next time! 👋{Colors.RESET}")
        
    except KeyboardInterrupt:
        clear_screen()
        print(f"{Colors.BRIGHT_RED}🐍 Game interrupted. Thanks for playing! 🐍{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}❌ An error occurred: {e}{Colors.RESET}")
    
    print(f"\n{Colors.BRIGHT_WHITE}Press any key to exit...{Colors.RESET}")
    try:
        msvcrt.getch()
    except:
        input()
