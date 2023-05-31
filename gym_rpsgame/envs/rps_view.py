import pygame
import random
import numpy as np
import os 
from PIL import Image

image_path = 'images/'
font_path = 'fonts/'

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGE_JPG1 = os.path.join(DIR_PATH, image_path+'rock.png')
IMAGE_JPG2 = os.path.join(DIR_PATH, image_path+'paper.png')
IMAGE_JPG3 = os.path.join(DIR_PATH, image_path+'scissor.png')
IMAGE_JPG4 = os.path.join(DIR_PATH, image_path+'reduceRPS.png')
FONT_TTF = os.path.join(DIR_PATH, font_path+'dancing.ttf')


class ToolsGame(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		self.rock = pygame.image.load(IMAGE_JPG1).convert_alpha()
		self.paper = pygame.image.load(IMAGE_JPG2).convert_alpha()
		self.scissor = pygame.image.load(IMAGE_JPG3).convert_alpha()
		self.rps = pygame.image.load(IMAGE_JPG4).convert_alpha()

		self.rect_rock = self.rock.get_rect()
		self.rect_paper = self.paper.get_rect()
		self.rect_scissor = self.scissor.get_rect()
		self.rect_rps = self.rps.get_rect()

	def update(self):
		pass


class RPSGame():
	def __init__(self, name='RPS-Game', screen_size=(800,650), enable_render=True):

		pygame.init()
		pygame.display.set_caption(name)
		self.clock = pygame.time.Clock()
		self.screen_size = screen_size
		self.fps = 30
		self.gif = 0
		self.images = []

		self.__game_over = False
		self.__enable_render = enable_render
		self.font = pygame.font.Font(None, 25)

		if self.__enable_render is True:
			self.screen = pygame.display.set_mode(screen_size)
			self.background = pygame.Surface(self.screen.get_size()).convert()
			self.background.fill((255, 255, 255)) # color background

			self.board = pygame.Surface(self.screen.get_size()).convert_alpha()
			self.board.fill((10,60,50)) # color board

			self.tool = ToolsGame()
			self.dict_rps = {0:'rock', 1:'paper', 2:'scissor'}
			self.player_choice, self.bot_choice = ' ', ' '

			self.winner = ' '
			self.count = 0

			#self.update()


	def quit_game(self):
		try:
			self.__game_over = True
			if self.__enable_render is True:
				pygame.display.quit()
				pygame.quit()
		except Exception:
			pass


	def __controller_update(self):
		if not self.__game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.__game_over = True
					self.quit_game()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.__game_over = True
						pygame.quit()
					if event.key == pygame.K_w:
						self.gif = 150


	def __view_update(self, mode="human"):

		if not self.__game_over:

			self.screen.blit(self.background, (0,0))
			self.screen.blit(self.board, (0,0))
			
			self.__draw_tools()

			#Player section
			if self.player_choice == 'rock':
				self.screen.blit(self.tool.rock, (250-self.tool.rect_rock[0]-5, 
		 			275-self.tool.rect_rock[1]-5))
		

			if self.player_choice == 'paper':
				self.screen.blit(self.tool.paper, (250-self.tool.rect_paper[0]-5, 
		 			275-self.tool.rect_paper[1]-5))

			if self.player_choice == 'scissor':
				self.screen.blit(self.tool.scissor, (250-self.tool.rect_scissor[0]-5, 
		 			275-self.tool.rect_scissor[1]-5))

			#Bot section
			if self.bot_choice == 'rock':
				self.screen.blit(self.tool.rock, 
					(500-self.tool.rect_rock[0]-5, 
						275-self.tool.rect_rock[1]-5))
				

			if  self.bot_choice == 'paper':
				self.screen.blit(self.tool.paper, 
					(500-self.tool.rect_paper[0]-5, 
						275-self.tool.rect_paper[1]-5))

			if self.bot_choice == 'scissor':
				self.screen.blit(self.tool.scissor, 
					(500-self.tool.rect_scissor[0]-5, 
						275-self.tool.rect_scissor[1]-5))


		if mode == "human" and not(self.__game_over):
			pygame.display.update()
			return np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface())))


	def reset_game(self):
		self.dict_rps = {0:'rock', 1:'paper', 2:'scissor'}
		self.player_choice, self.bot_choice = None, None
		#if not(self.__game_over):
			#pygame.display.update()

	def info_game(self, winner):
		self.winner = winner


	def display_message(self, message, y_pos):

		shadow = self.font.render(message, True, (0, 0, 0))
		text = self.font.render(message, True, (255, 255, 255))
		text_position = [60, y_pos]
		text_position[0] += 5
		text_position[1] += 5
		self.screen.blit(shadow, text_position)
		self.screen.blit(text, text_position)

	def play(self):

		self.update()

	def play_game(self, player, bot):
		self.player_choice =  self.dict_rps[player]
		self.bot_choice = self.dict_rps[bot]
		self.count += 1

	def update(self, mode="human"):
		try:
			img_output = self.__view_update(mode)
			self.__controller_update()
		except Exception as e:
			self.__game_over = True
			self.quit_game()
			raise e
		else:
			return img_output

	def __draw_tools(self):

		x_screen = (self.screen_size[0] - self.tool.rect_rps[0])//4 + 65 
		y_screen = 50 - self.tool.rect_rps[1]

		self.screen.blit(self.tool.rps, (x_screen, y_screen))
		pygame.draw.rect(self.screen, 'white', (225, 250, 100, 100), 1)
		pygame.draw.rect(self.screen, 'white', (475, 250, 100, 100), 1)

		#text player
		Player = self.font.render('Player', True, (255, 255, 255))
		Bot = self.font.render('Bot', True, (255, 255, 255))
		versus  = self.font.render('VS', True, (255, 0, 0))
		text_position1 = [251, 355]
		text_position2 = [514, 355]
		text_position3 = [391, 300]

		
		self.screen.blit(Player, text_position1)
		self.screen.blit(Bot, text_position2)
		self.screen.blit(versus, text_position3)

		self.display_message(f'Game: #{self.count}', 425)
		self.display_message(f"Player's choice: {self.player_choice}", 475)
		self.display_message(f"Bot's choice: {self.bot_choice}", 450)
		self.display_message(f"Winner: {self.winner}", 500)

		fontObj = pygame.font.Font(FONT_TTF, 32)
		obj = fontObj.render('Rock-Paper-Scissor game', True, (0, 0, 0))
		self.screen.blit(obj, (250, 600))

	def make_gif(self):
		if self.gif > 0:
			strFormat = 'RGBA'
			raw_str = pygame.image.tostring(self.screen, strFormat, False)
			image = Image.frombytes(strFormat, self.screen.get_size(), raw_str)
			self.images.append(image)
			self.gif -= 1  
			if self.gif == 0: 
				self.images[0].save('Rock-Paper-Scissor.gif', 
					save_all=True, append_images = self.images[1:],
					optimize=True, duration=200//self.fps,
					loop=0)
				self.images=[]




if __name__ == "__main__":

	game = RPSGame()

	while True:

		player = np.random.choice([0,1,2])
		bot = np.random.choice([0,1,2])



		game.play_game(player, bot)
		game.play()
		



