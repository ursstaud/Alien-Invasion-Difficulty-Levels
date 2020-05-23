import pygame.font


class MediumButton:
	"""creating a class for the button for the game to start playing"""
	def __init__(self, ai_game, msg):
		"""initialize button attributes"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect() #establishing the screen as a rectangle to get dimensions 
		#ultimately for placement

		#set the dimensions and properties of the button
		self.width, self.height = 250, 50
		self.medium_button_color = (255,255,0) #lime green rgb
		self.medium_text_color =(0, 0, 0)
		self.font = pygame.font.SysFont(None, 48) #default font, size 48

		#build the button's rect object and center it
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center #setting the center button attribute to the center of the screen attribute

		#the button message needs to be prepped only once
		self._prep_msg(msg) #renders the string you want to display as an image

		#speed settings
		self.ship_speed = 5.0
		self.bullet_speed = 6.0
		self.alien_speed = 2.0


	def _prep_msg(self, msg):
		"""turn the message into a rendered image and center text on the button"""
		self.medium_msg_image = self.font.render(msg, True, self.medium_text_color, self.medium_button_color)
		self.medium_msg_image_rect = self.medium_msg_image.get_rect()
		self.medium_msg_image_rect.center = self.rect.center


	def draw_medium_button(self):
		"""draw blank button then draw message"""
		self.screen.fill(self.medium_button_color, self.rect) #draws the rectangular portion of the button
		self.screen.blit(self.medium_msg_image, self.medium_msg_image_rect) 
		#draw the text image to the screen, passing it an image and the rect object associated with that image

