This Project explaining
1. State:
The state represents the environment's current condition, which will be provided to the reinforcement learning agent (the model). It includes the following elements:
Dino's Y position (dino_y): The vertical position of the Dino in the game. It changes when the Dino is jumping or falling.
Dino's velocity (dino_velocity): The current velocity of the Dino in the Y direction (i.e., how fast it's moving up or down).
Is Dino jumping (is_jumping): A boolean value that tells whether the Dino is in the air (jumping) or on the ground.
Obstacle X position (obstacle_x): The horizontal position of the primary cactus (first obstacle).
Obstacle speed (obstacle_speed): The speed at which the primary cactus is moving to the left (increasing negative value).
Second obstacle X position (second_obstacle_x): The horizontal position of the second cactus (second obstacle).
Second obstacle speed (second_obstacle_speed): The speed at which the second cactus is moving to the left.

2. Action:
The action represents what the agent can do at each step of the game. The action space is defined as a discrete set of possible actions:

Action 0: Do nothing (Dino remains on the ground and doesn't jump).
Action 1: Jump (Dino jumps into the air).
The agent must decide whether to jump (action 1) to avoid obstacles or do nothing (action 0) depending on the current state of the game.

3. Reward:
The reward indicates how good or bad the agent's action was in a given state. Here's how it works:
Reward = 1: This reward is given if the agent successfully avoids obstacles and stays alive (i.e., not colliding with any cactus). The score increases when the obstacles move off the screen, and the reward is positive.
Reward = -100: This reward is given if the agent collides with an obstacle (either the primary cactus or the second cactus). This results in a negative reward, indicating a failed attempt to avoid the obstacle.

Instructions to Run Game
1. Make of a copy this repository
2. Run game.py


Instructions to Train RL (DQN) Agent
1. Make of a copy this repository
2. Run train_agent.py



 Contributions
Created at TUMO
Used Gymnasium, stable_baselines3
![game](https://github.com/user-attachments/assets/d095b8b0-9dd6-461a-b397-9030894e0f41)



