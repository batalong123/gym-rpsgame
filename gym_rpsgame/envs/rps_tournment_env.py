import gym 
from gym import spaces
import numpy as np
from .rps_view_tournment import RPSTournment
import sys




class RockPaperScissorsTournmentEnv(gym.Env):

	metadata = {'render.modes': ['console', 'human']}

	def __init__(self):

		self.action_space = spaces.Discrete(3)
		self.observation_space = spaces.Box(low=-20, high=20, shape=(3, ),
			dtype=np.int)

		self.game = RPSTournment()

		self.viewer = ['rock', 'paper', 'scissor']
		self.step_count = None  
		self.step_score1 = None
		self.step_score2 = None
		self.game_score = {0: 0, 1: 0}
		self.episode = 1; self.winner = (0, 0)

	def reset(self):

		self.game.reset_game()
		self.player1_choice = None  
		self.player2_choice = None
		self.step_score1 = []; self.step_score2 = []
		self.step_count = np.random.choice([5, 10, 20])
		self.turn = 0
		obs1 = np.array([np.random.choice([0, 1, 2]), self.step_count, 0])
		obs2 = np.array([np.random.choice([0, 1, 2]), self.step_count, 0])

		return obs1, obs2

	def step(self, action):

		action1, action2 = tuple(action)

		if action1 not in [0, 1, 2] or action2 not in [0, 1, 2] : print("action must be in [0, 1, 2]!"); sys.exit(1) 

		self.player1_choice = int(action1)
		self.player2_choice = int(action2) 

		self.reward = None
		self.done = False
		self.turn += 1 

		if self.player1_choice == self.player2_choice:
			self.reward = 0
			self.step_score1.append(self.reward)
			self.step_score2.append(self.reward)

		elif self.player1_choice - self.player2_choice == 1 or self.player1_choice - self.player2_choice == -2:
			self.reward = 1
			self.winner = (self.winner[0]+1, self.winner[1])
			self.step_score1.append(self.reward)
			self.step_score2.append(-self.reward)
		else:
			self.reward = -1
			self.winner = (self.winner[0], self.winner[1]+1)
			self.step_score1.append(self.reward)
			self.step_score2.append(-self.reward)

		self.game.play_game(self.player1_choice, self.player2_choice, self.turn)
		

		info = {'player1':self.viewer[self.player1_choice], 'player2':self.viewer[self.player2_choice], 'Winner':self.winner}

		self.done = (self.step_count == 0)
		observation1 = np.array([self.player2_choice, self.step_count, sum(self.step_score1)])
		observation2 = np.array([self.player1_choice, self.step_count, sum(self.step_score2)])
		self.step_count -= 1

		if self.done:
			self.episode += 1

			if self.winner[0] - self.winner[1] > 0:
				self.game_score[0] +=1

			if self.winner[0] - self.winner[1] < 0:
				self.game_score[1] +=1
				
			self.game.info_game(self.game_score, self.episode)
			self.winner = (0, 0)

		
		return (observation1, observation2), self.reward, self.done, info

	def render(self, mode='human'):

		if mode == 'human':
			return self.game.update(mode)

		else:

			if self.player2_choice == 0:
				player2_choice_str = 'rock'
			elif self.player2_choice == 1:
				player2_choice_str = 'paper'
			else:
				player2_choice_str = 'scissors'

			if self.player1_choice == 0:
				player1_choice_str = 'rock'
			elif self.player1_choice == 1:
				player1_choice_str = 'paper'
			else:
				player1_choice_str = 'scissors'

			print(f"player2's choice: {player2_choice_str}.")
			print(f"player1's choice: {player1_choice_str}.")

	def close(self):
		self.game.quit_game()



		