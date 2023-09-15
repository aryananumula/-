import numpy as np

ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
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