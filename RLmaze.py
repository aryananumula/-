import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
import os, time

ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

class Agent(object):
    def __init__(self, states, alpha=0.15, random_factor=0.2):
        self.state_history = [((0, 0), 0)]
        self.alpha = alpha
        self.random_factor = random_factor
        self.G = {}
        self.init_reward(states)

    def init_reward(self, states):
        for i, row in enumerate(states):
            for j, col in enumerate(row):
                self.G[(j, i)] = np.random.uniform(low=1.0, high=0.1)
    
    def choose_action(self, state, allowedMoves):
        maxG = -10e15
        next_move = None
        randomN = np.random.random()
        if randomN < self.random_factor:
            next_move = np.random.choice(allowedMoves)
        else:
            for action in allowedMoves:
                new_state = tuple([sum(x) for x in zip(state, ACTIONS[action])])
                if self.G[new_state] >= maxG:
                    next_move = action
                    maxG = self.G[new_state]

        return next_move

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])
            target += reward

        self.state_history = []

        self.random_factor -= 10e-5

np.random.seed(44398328)

class Maze(object):
    def __init__(self):
        self.maze = np.zeros((9, 9))
        self.maze[0, 0] = 2
        self.maze[1:9, 4] = 1
        self.maze[8, 5] = 1
        self.maze[6:8, 1] = 1
        self.maze[0, 1:3] = 1
        self.maze[0:2, 2] = 1
        self.maze[3, 2] = 1
        self.maze[2:4, 0] = 1
        self.maze[5, 1:5] = 1
        self.robot_position = (0, 0)
        self.steps = 0
        self.construct_allowed_states()

    def is_allowed_move(self, state, action):
        y, x = state
        y += ACTIONS[action][0]
        x += ACTIONS[action][1]
        if y < 0 or x < 0 or y > 8 or x > 8:
            return False

        if self.maze[y, x] == 0 or self.maze[y, x] == 2:
            return True
        else:
            return False

    def construct_allowed_states(self):
        allowed_states = {}
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if self.maze[(y,x)] != 1:
                    allowed_states[(y,x)] = []
                    for action in ACTIONS:
                        if self.is_allowed_move((y,x), action) & (action != 0):
                            allowed_states[(y,x)].append(action)
        self.allowed_states = allowed_states

    def update_maze(self, action):
        y, x = self.robot_position
        self.maze[y, x] = 0
        y += ACTIONS[action][0]
        x += ACTIONS[action][1]
        self.robot_position = (y, x)
        self.maze[y, x] = 2 # set new position
        self.steps += 1 # add steps

    def is_game_over(self):
        # check if robot in the final position
        if self.robot_position == (8, 8):
            return True
        else:
            return False

    def get_state_and_reward(self):
        return self.robot_position, self.give_reward()

    def give_reward(self):
        # if at end give 0 reward
        # if not at end give -1 reward
        if self.robot_position == (8, 8):
            return 0
        else: 
            return -1

maze = Maze()
robot = Agent(maze.maze, alpha=0.1, random_factor=0.5)
moveHistory = []
x = 5000
for i in range(x+1): #training loop
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
        print("---------------------")
        print(str(maze.maze).replace("1. ", "⬜").replace("2. ", "🤖").replace("0. ", "  ").replace("1.", "🟥").replace("2.", "🤖").replace("0.", "  ").replace("[[", " [")[0:-1])
        print("---------------------")
        time.sleep(0.1)

print(maze.steps)
plt.semilogy
(moveHistory)
plt.show()
