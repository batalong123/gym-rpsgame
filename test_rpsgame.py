import time
import gym  
import gym_rpsgame

env = gym.make('rps-v0', opponentplayer='statistical')

game = {'win': 0, 'loose': 0, 'draw': 0}
for i in range(2000):

	done = False
	total_reward = 0
	obs = env.reset()
	while not done:

		action = env.action_space.sample()
		obs, reward, done, info = env.step(action)

		total_reward += reward

		if reward > 0: 
			game['win'] += 1 
		elif reward < 0: 
			game['loose'] += 1 
		else: 
			game['draw'] += 1

		env.render()
		env.game.make_gif()
		#time.sleep(1.0)
	print("========== Rock-Paper-Scissor ===========")
	print(f'episode#: {i+1}')
	print(f'Total reward: {total_reward}.')
	print(f'Last game: {info}.') 
	print(f'Last observation: {obs}.')
	print(f'Game: {game}\n')

env.close()


