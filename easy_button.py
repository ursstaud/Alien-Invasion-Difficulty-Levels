import pygame.font

class EasyButton:
	"""creating a class for the button for the game to start playing"""
	def __init__(self, ai_game, msg):
		"""initialize button attributes"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect() #establishing the screen as a rectangle to get dimensions 
		#ultimately for placement

		#set the dimensions and properties of the button
		self.width, self.height = 200, 50
		self.easy_button_color = (34, 139, 34) 
		self.easy_text_color =(255, 255, 255)
		self.font = pygame.font.SysFont(None, 48) #default font, size 48

		#build the button's rect object and center it
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.midleft = self.screen_rect.midleft #setting the center button attribute to the center of the screen attribute

		#the button message needs to be prepped only once
		self._prep_msg(msg) #renders the string you want to display as an image

		#speed settings
		self.ship_speed = 4.0
		self.bullet_speed = 5.0
		self.alien_speed = 1.0


	def _prep_msg(self, msg):
		"""turn the message into a rendered image and center text on the button"""
		self.easy_msg_image = self.font.render(msg, True, self.easy_text_color, self.easy_button_color)
		self.easy_msg_image_rect = self.easy_msg_image.get_rect()
		self.easy_msg_image_rect.midleft = self.rect.midleft


	def draw_easy_button(self):
		"""draw blank button then draw message"""
		self.screen.fill(self.easy_button_color, self.rect) #draws the rectangular portion of the button
		self.screen.blit(self.easy_msg_image, self.easy_msg_image_rect) 
		#draw the text image to the screen, passing it an image and the rect object associated with that image


