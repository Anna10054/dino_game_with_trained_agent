import numpy as np
import gymnasium as gym
from gymnasium import spaces
import pygame
import random
import os
import numpy as np


# Constants
DINO_X = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
DINO_WIDTH, DINO_HEIGHT = 45, 45
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 35, 50     
SECOND_OBSTACLE_WIDTH, SECOND_OBSTACLE_HEIGHT = 35, 50  # New cactus attributes
GROUND_HEIGHT = 300
FONT_SIZE = 24
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60

class DinoGame(gym.Env):
    def __init__(self):
        super(DinoGame, self).__init__()
        self.state = None
        self.reward = 0
        self.action_space = spaces.Discrete(2)  # 0: Do nothing, 1: Jump
        self.observation_space = spaces.Box(low=0, high=SCREEN_WIDTH, shape=(7,), dtype=np.float32)  # Add second obstacle data
        
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Google Dino Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Dino initial state
        self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
        self.dino_velocity = 0
        self.is_jumping = False
        self.obstacle_x = SCREEN_WIDTH
        self.obstacle_speed = -7     
        self.score = 0

        # Second cactus initial state
        self.second_obstacle_x = SCREEN_WIDTH + random.randint(400, 600)  # Appears after a while
        self.second_obstacle_y = GROUND_HEIGHT - SECOND_OBSTACLE_HEIGHT  # Set to ground level
        self.second_obstacle_speed = -7

        # Return state that includes both ground obstacle and second cactus
        self.state = np.array([
            self.dino_y,
            self.dino_velocity,
            self.is_jumping,
            self.obstacle_x,
            self.obstacle_speed,
            self.second_obstacle_x,
            self.second_obstacle_speed
        ], dtype=np.float32)
        return self.state, {}

    def step(self, action):
        """ Takes in the self (DinoGame environment) and an action (int) to take a step in the environment.
            self: DinoGame environment
            action: int action to take in the environment, where action == 0 is do nothing and action ==  1 is jump
        """
        # Dino jumping logic
        if action == 1 and not self.is_jumping:
            self.is_jumping = True
            self.dino_velocity = -18
        
        if self.is_jumping:
            self.dino_y += self.dino_velocity
            self.dino_velocity += 1
            if self.dino_y >= GROUND_HEIGHT - DINO_HEIGHT:
                self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
                self.is_jumping = False
        

        # Update ground obstacle (cactus)
        self.obstacle_x += self.obstacle_speed
        if self.obstacle_x < 0:
            self.score += 1 
            self.obstacle_x = SCREEN_WIDTH + random.randint(0, 300)  # Reset at random position     

        # Update second cactus
        self.second_obstacle_x += self.second_obstacle_speed
        if self.second_obstacle_x < 0:
            self.score += 1
            self.second_obstacle_x = SCREEN_WIDTH + random.randint(400, 600)  # Reset at random position

        # Collision with ground obstacle
        done = False
        if self.obstacle_x - (DINO_X + DINO_WIDTH) < 0 and self.dino_y + DINO_HEIGHT > GROUND_HEIGHT - OBSTACLE_HEIGHT:
            done = True

        # Collision with second cactus (now on the ground)
        if self.second_obstacle_x - (DINO_X + DINO_WIDTH) < 0 and self.dino_y + DINO_HEIGHT > self.second_obstacle_y:
            done = True

        # Update state and reward
        self.state = np.array([
            self.dino_y,
            self.dino_velocity,
            self.is_jumping,
            self.obstacle_x,
            self.obstacle_speed,
            self.second_obstacle_x,
            self.second_obstacle_speed
        ], dtype=np.float32)
        reward = 1 if not done else -100
        return self.state, reward, done, False, {}

    def render(self, mode="human"):
        self.screen.fill(WHITE)

        # Draw ground
        pygame.draw.line(self.screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

        # Draw Dino
        self.dino_image = pygame.image.load('dino.jpg')
        self.dino_image = pygame.transform.scale(self.dino_image, (DINO_WIDTH, DINO_HEIGHT))
        self.screen.blit(self.dino_image, (DINO_X, self.dino_y))

        # Draw ground obstacle (cactus)
        self.cactus_image = pygame.image.load('cactus.png')
        self.cactus_image = pygame.transform.scale(self.cactus_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.screen.blit(self.cactus_image, (self.obstacle_x, GROUND_HEIGHT - OBSTACLE_HEIGHT))

        # Draw second cactus (on the ground)
        self.second_cactus_image = pygame.image.load('cactus.png')  # You can use the same cactus image or a different one
        self.second_cactus_image = pygame.transform.scale(self.second_cactus_image, (SECOND_OBSTACLE_WIDTH, SECOND_OBSTACLE_HEIGHT))
        self.screen.blit(self.second_cactus_image, (self.second_obstacle_x, self.second_obstacle_y))

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        return self.screen

    def close(self):
        pygame.quit()

# Register the environment
