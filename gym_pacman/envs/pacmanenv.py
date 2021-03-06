
import gym
from gym import Env
from gym import spaces
from numpy.core.fromnumeric import shape
import numpy as np
import cv2
import sys
sys.path.append(r'/home/lpe/Desktop/Project_in_Artificial_Intelligence_PAC-MAN/pacman_game_env/gym_pacman/envs/Pacman_Game') 
sys.path.append(r'/home/lpe/Desktop/Project_in_Artificial_Intelligence_PAC-MAN/pacman_game_env/gym_pacman/envs') 
from Pacman_Game.run import *
from Pacman_Game.constants import PACMAN
import pygame

#from mss import mss

keyboard_keys = ["up","down","left","right"]

MAX_REWARD = 100
N_DISCRETE_ACTIONS = 4

BOUNDING_BOX = {'top': 170 , 'left': 100, 'width': 448, 'height': 500}
NUMBER_OF_CHANNELS = 3
REWARD_RANGE = (-20,20)

class PacmanEnv(Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(PacmanEnv, self).__init__()

        self.game = GameController()
        self.game.startGame()
        self.game.update()
        self.done = False

        self.reward_range = REWARD_RANGE

        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        shape = (BOUNDING_BOX['height'],BOUNDING_BOX['width'],NUMBER_OF_CHANNELS)
        
        self.observation_space = spaces.Box(low = 0, high = 255, shape = shape, dtype = np.uint8)
            

    def _next_observation(self):
        view = pygame.surfarray.array3d(self.game.screen)
        #  convert from (width, height, channel) to (height, width, channel)
        view = view.transpose([1, 0, 2])
        #view = cv2.cvtColor(view, cv2.COLOR_RGB2GRAY)
        return view[45:545, :]

    def _take_action(self, action):
        self.game.AI_direction = action        
        self.game.update()
            
    def step(self, action):
        if(self.game.pause.paused):
            self.game.pause.flip()
        # Execute one time step within the environment
        self._take_action(action)

        reward = self._get_reward()

        obs = self._next_observation()

        return obs, reward, self.done, {}
    def get_score(self):
        return self.game.score
        
    def reset(self):
        self.game.restartGame()

        return self._next_observation()

    def render(self, mode='human', close=False):
        view = pygame.surfarray.array3d(self.game.screen)
        #  convert from (width, height, channel) to (height, width, channel)
        view = view.transpose([1, 0, 2])

        #  convert from rgb to bgr
        return view[45:545, :]

    def _get_reward(self):
        self.done = False
        reward = 0 
        reward = -3  * self.game.pacman.distancePellets(self.game.pellets.pelletList)/360704 # the number comes from the biggest distance seen

        if self.game.events_AI == 0: # nothing or wall         
            reward += -0.5
        elif self.game.events_AI == 1: # Pellets
            reward += 2
        elif self.game.events_AI == 2: # super pellets
            reward += 5
        elif self.game.events_AI == 3: # ghost kill
            reward += 10
        elif self.game.events_AI == 4: # pacman dead
            reward += -10
        elif self.game.events_AI == 5: # gameover
            self.done = True
            reward += -20
        elif self.game.events_AI == 6: #  won
            self.done = True
            reward += 20
        elif self.game.events_AI == 7: #  fruit (not in game)
            reward += 7
        else:
            reward += -10
        return reward
    
