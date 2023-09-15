import numpy as np
from environment import Maze
from agent import Agent
import matplotlib.pyplot as plt
from ast import literal_eval
import os, time

print("started")

maze = Maze()
robot = Agent(maze.maze, alpha=0.1, random_factor=0.5)
moveHistory = []
for i in range(5001):
    maze = Maze()
    while not maze.is_game_over():
        state, _ = maze.get_state_and_reward()
        action = robot.choose_action(state, maze.allowed_states[state])
        maze.update_maze(action)
        state, reward = maze.get_state_and_reward()
        robot.update_state_history(state, reward)
        if maze.steps >= 1000:
            break
    
    robot.learn()
    moveHistory.append(maze.steps)
    if i%1000 == 0:
        print(i)
        print(maze.steps)

maze = Maze()
while not maze.is_game_over():
        state, _ = maze.get_state_and_reward()
        action = robot.choose_action(state, maze.allowed_states[state])
        maze.update_maze(action)
        state, reward = maze.get_state_and_reward()
        robot.update_state_history(state, reward)
        os.system("clear")
        print("----------------")
        print(str(maze.maze).replace("1. ", "⬜").replace("2. ", "🤖").replace("0. ", "  ").replace("1.", "🟥").replace("2.", "🤖").replace("0.", "  ").replace("[[", " [")[0:-1])
        print("----------------")
        time.sleep(0.1)

print(maze.steps)
plt.semilogy
(moveHistory)
plt.show()