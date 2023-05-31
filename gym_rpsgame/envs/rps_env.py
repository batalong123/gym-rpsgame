import gym 
from gym import spaces
import numpy as np
from .rps_view import RPSGame
from .agentbot import agents
import sys




class RockPaperScissorsEnv(gym.Env):

	metadata = {'render.modes': ['console', 'human']}

	def __init__(self, opponentplayer='statistical'):

		self.action_space = spaces.Discrete(3)
		self.observation_space = spaces.Box(low=-20, high=20, shape=(3, ),
			dtype=np.int)

		self.game = RPSGame()

		self.opponentplayer = opponentplayer

		self.preview_player_choice = np.random.choice([0, 1, 2])# this variable 

		self.viewer = ['rock', 'paper', 'scissor']
		self.step_count = None  
		self.step_score = None

	def reset(self):

		self.game.reset_game()
		self.player_choice = None  
		self.bot_choice = None
		self.step_score = []
		self.step_count = np.random.choice([5, 10, 20])

		return np.array([np.random.choice([0, 1, 2]), self.step_count, sum(self.step_score)])

	def step(self, action):

		if action not in [0, 1, 2]: print("action must be in [0, 1, 2]!"); sys.exit(1) 

		self.player_choice = action

		if self.opponentplayer in list(agents.keys()):
			agent = agents[self.opponentplayer]
			self.bot_choice = agent(self.preview_player_choice, self.step_count)
			self.preview_player_choice = self.player_choice

		else:

			print('\n======================= Agent Bot Error ============================')
			print(f'Valid opponentplayer must be {agents.keys()}.\n')
			sys.exit(1)

		self.reward = None
		self.done = False
		self.winner = ' '

		if self.player_choice == self.bot_choice:
			self.reward = 0
			self.winner = 'Draw'

		elif self.player_choice - self.bot_choice == 1 or self.player_choice - self.bot_choice == -2:
			self.reward = 1
			self.winner = 'Player'
		else:
			self.reward = -1
			self.winner = 'Bot'

		self.game.play_game(self.player_choice, self.bot_choice)
		self.game.info_game(self.winner)

		info = {'Player':self.viewer[self.player_choice], 'Bot':self.viewer[self.bot_choice], 'Winner':self.winner}

		self.done = (self.step_count == 0)
		self.step_score.append(self.reward)
		observation = np.array([self.bot_choice, self.step_count, sum(self.step_score)])
		self.step_count -= 1
		
		return observation, self.reward, self.done, info

	def render(self, mode='human'):

		if mode == 'human':
			return self.game.update(mode)

		else:

			if self.bot_choice == 0:
				bot_choice_str = 'rock'
			elif self.bot_choice == 1:
				bot_choice_str = 'paper'
			else:
				bot_choice_str = 'scissors'

			if self.player_choice == 0:
				player_choice_str = 'rock'
			elif self.player_choice == 1:
				player_choice_str = 'paper'
			else:
				player_choice_str = 'scissors'

			print(f"Bot's choice: {bot_choice_str}.")
			print(f"Player's choice: {player_choice_str}.")

	def close(self):
		self.game.quit_game()



		