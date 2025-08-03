#!/usr/bin/env python3
"""
🐍 Reverse Snake Game - Retro Edition

A unique twist on the classic Snake game where eating numbered food
makes the snake switch between moving head-first and tail-first!

Author: Created with Windsurf AI
Version: 1.0
Requires: pygame>=2.1.0
"""

import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors - Retro Palette
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 128, 0)
DARK_GRAY = (64, 64, 64)

class Snake:
    """Snake class handling movement, growth, and direction switching mechanics."""
    
    def __init__(self):
        """Initialize snake in the center of the screen."""
        # Start with a small snake in the center
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.body = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.direction = (1, 0)  # Moving right initially
        self.grow_next = False
        self.moving_backwards = False  # Flag for permanent direction switch
        
    def move(self):
        """Move the snake one step in the current direction."""
        # Always move the head (index 0) in the current direction
        # The body orientation is handled by the eat_food method
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        self.body.insert(0, new_head)
        if not self.grow_next:
            self.body.pop()
        else:
            self.grow_next = False
    
    def change_direction(self, new_direction):
        """Change snake direction, preventing 180-degree turns."""
        # Prevent moving directly backwards
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            # Always use the direction as-is, the body reversal handles the rest
            self.direction = new_direction
    
    def check_collision(self):
        """Check if snake has collided with walls or itself."""
        # Always check collision for head (index 0) since that's always the moving part
        head = self.body[0]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        
        # Check self collision
        if head in self.body[1:]:
            return True
        
        return False
    
    def eat_food(self, food_number):
        """Handle eating food: switch direction and grow snake.
        
        Args:
            food_number (int): Value of the food eaten (affects score)
        """
        # Switch movement direction permanently
        self.moving_backwards = not self.moving_backwards
        
        # When switching direction, reverse the body list so head becomes tail
        # This creates the visual effect of the snake "flipping around"
        self.body.reverse()
        # Also reverse the direction vector
        self.direction = (-self.direction[0], -self.direction[1])
        
        # Grow the snake
        self.grow_next = True

class Food:
    """Food class handling food generation and positioning."""
    
    def __init__(self):
        """Initialize food with random position and number."""
        self.position = self.generate_position()
        self.number = random.randint(1, 9)
    
    def generate_position(self):
        """Generate a random position on the game grid."""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def respawn(self, snake_body):
        """Respawn food in a position not occupied by the snake.
        
        Args:
            snake_body (list): List of snake body segment positions
        """
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break
        self.number = random.randint(1, 9)

class Game:
    """Main game class handling game loop, rendering, and user input."""
    
    def __init__(self):
        """Initialize the game window and game objects."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Reverse Snake - Retro Edition")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = 0
        
        # Fonts for retro feel
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game border
        self.border_thickness = 2
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        self.snake.move()
        
        # Check if snake ate food (always check head since it's always the active end)
        if self.snake.body[0] == self.food.position:
            self.snake.eat_food(self.food.number)
            self.score += self.food.number
            self.food.respawn(self.snake.body)
        
        # Check collision
        if self.snake.check_collision():
            return False
        
        return True
    
    def draw(self):
        # Fill background with dark pattern
        self.screen.fill(BLACK)
        
        # Draw retro grid pattern
        for x in range(0, WINDOW_WIDTH, CELL_SIZE * 4):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE * 4):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y), 1)
        
        # Draw game border
        pygame.draw.rect(self.screen, WHITE, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), self.border_thickness)
        
        # Draw snake with retro style
        for i, segment in enumerate(self.snake.body):
            x, y = segment
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if i == 0:  # Head
                # Change head color when moving backwards
                head_color = CYAN if self.snake.moving_backwards else GREEN
                pygame.draw.rect(self.screen, head_color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)
                
                # Add eyes to the head for character
                eye_size = 3
                eye1_pos = (x * CELL_SIZE + 5, y * CELL_SIZE + 5)
                eye2_pos = (x * CELL_SIZE + CELL_SIZE - 8, y * CELL_SIZE + 5)
                pygame.draw.circle(self.screen, BLACK, eye1_pos, eye_size)
                pygame.draw.circle(self.screen, BLACK, eye2_pos, eye_size)
            else:  # Body
                # Gradient body effect
                body_color = DARK_GREEN if i % 2 == 0 else GREEN
                pygame.draw.rect(self.screen, body_color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
        
        # Draw food with retro glow effect
        food_x, food_y = self.food.position
        food_rect = pygame.Rect(food_x * CELL_SIZE, food_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        # Pulsing food effect
        import math
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.3 + 0.7
        food_color = (int(255 * pulse), int(100 * pulse), int(100 * pulse))
        
        pygame.draw.rect(self.screen, food_color, food_rect)
        pygame.draw.rect(self.screen, YELLOW, food_rect, 2)
        
        # Draw number on food with better styling
        number_text = self.font_medium.render(str(self.food.number), True, WHITE)
        text_rect = number_text.get_rect(center=food_rect.center)
        # Add text shadow
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        shadow_text = self.font_medium.render(str(self.food.number), True, BLACK)
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(number_text, text_rect)
        
        # Draw retro-style HUD
        # Score with glow effect
        score_text = self.font_large.render(f"SCORE: {self.score:04d}", True, YELLOW)
        score_shadow = self.font_large.render(f"SCORE: {self.score:04d}", True, BLACK)
        self.screen.blit(score_shadow, (12, 12))
        self.screen.blit(score_text, (10, 10))
        
        # High score
        if self.score > self.high_score:
            self.high_score = self.score
        high_score_text = self.font_small.render(f"HIGH: {self.high_score:04d}", True, WHITE)
        self.screen.blit(high_score_text, (10, 60))
        
        # Show movement direction status with retro styling
        if self.snake.moving_backwards:
            status_text = self.font_small.render("◄ REVERSE MODE ►", True, CYAN)
            mode_bg = pygame.Rect(WINDOW_WIDTH - 180, 10, 170, 25)
            pygame.draw.rect(self.screen, BLUE, mode_bg)
            pygame.draw.rect(self.screen, CYAN, mode_bg, 2)
            self.screen.blit(status_text, (WINDOW_WIDTH - 175, 15))
        else:
            status_text = self.font_small.render("► FORWARD MODE ◄", True, GREEN)
            mode_bg = pygame.Rect(WINDOW_WIDTH - 180, 10, 170, 25)
            pygame.draw.rect(self.screen, DARK_GREEN, mode_bg)
            pygame.draw.rect(self.screen, GREEN, mode_bg, 2)
            self.screen.blit(status_text, (WINDOW_WIDTH - 175, 15))
        
        # Draw retro instructions
        instruction_text = self.font_small.render("🎮 ARROWS: Move | 🍎 EAT: Switch Direction | ⚡ SPACE: Restart", True, WHITE)
        self.screen.blit(instruction_text, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
    
    def game_over_screen(self):
        # Retro game over screen with effects
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Animated "GAME OVER" text
        import math
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 0.3 + 0.7
        game_over_color = (int(255 * pulse), int(50 * pulse), int(50 * pulse))
        
        game_over_font = pygame.font.Font(None, 84)
        game_over_text = game_over_font.render("GAME OVER", True, game_over_color)
        game_over_shadow = game_over_font.render("GAME OVER", True, BLACK)
        
        # Score display
        score_text = self.font_large.render(f"FINAL SCORE: {self.score:04d}", True, YELLOW)
        high_text = self.font_medium.render(f"HIGH SCORE: {self.high_score:04d}", True, WHITE)
        
        # Instructions
        restart_text = self.font_small.render("PRESS SPACE TO RESTART | ESC TO QUIT", True, CYAN)
        
        # Center everything
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        game_over_shadow_rect = game_over_rect.copy()
        game_over_shadow_rect.x += 3
        game_over_shadow_rect.y += 3
        
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        high_rect = high_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
        
        # Draw with retro border
        border_rect = pygame.Rect(WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 120, 500, 200)
        pygame.draw.rect(self.screen, DARK_GRAY, border_rect)
        pygame.draw.rect(self.screen, WHITE, border_rect, 3)
        
        self.screen.blit(game_over_shadow, game_over_shadow_rect)
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(high_text, high_rect)
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        game_active = True
        
        while running:
            if game_active:
                running = self.handle_events()
                if running:
                    game_active = self.update()
                    self.draw()
            else:
                # Game over state
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # Restart game
                            self.snake = Snake()
                            self.food = Food()
                            self.score = 0
                            game_active = True
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                
                self.game_over_screen()
            
            self.clock.tick(10)  # 10 FPS for classic snake feel
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
