import sys
from time import sleep

import pygame

from settings_multi import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from easy_button import EasyButton
from medium_button import MediumButton
from hard_button import HardButton

class AlienInvasion:
	"""Overall class to mamage game assets and behaviors"""

	def __init__(self):
		"""initialize the game and create game resources"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width 
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		#create an instance of game stats to store game stats
		self.stats = GameStats(self) #want to makethis instance after
		#creating the game window but before defining other game elements (such as ship)

		self.ship=Ship(self)#create instance of ship, requires 1 argument, the ai_grame instance
		#the self argument refers to the current instance of the game
		#gives the ship access to the game's resources, includig the screen
		self.bullets = pygame.sprite.Group() #we want to do this because it will keep the bullets
		#fired on the screen on the screen before they leave the screen
		self.aliens = pygame.sprite.Group() #want to group because it will automatically draw all elements 
		#of a group to the screen
		self._create_fleet() #this creates a group to hold the fleet of aliens

		#make the play button
		self.easy_button = EasyButton(self, "Easy Mode")
		self.medium_button = MediumButton(self, "Medium Mode")
		self.hard_button = HardButton(self, "Hard Mode")


	def run_game(self):
		"""start the main loop for the game"""
		while True:
			self._check_events() #calls another method from within the class, simplifies the main method
			#note, using dot notation to call

			#identifying the steps that should only run if the game is active
			if self.stats.game_active:
				self.ship.update() #run the code from the instance of the ship so the ship can move
				self._update_bullets() #another helper method managing bullets yas
				self._update_aliens() #another helper method for updating the 
			
			self._update_screen() #another helper method for updating the screen, continuous updating until exit


	def _update_bullets(self):
		"""update position of bullets and get rid of old bullets"""
		self.bullets.update() #updates bullet location/movement, automatically calls update
			#for each sprite in the group
		#Get rid of bullets that have disappeared
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()


	def _update_aliens(self):
		"""check if the fleet is at an edge, 
		then update the positions of all aliens in the fleet"""
		self._check_fleet_edges()
		self.aliens.update() #pulling the method from the alien class and adding it to alien invasion class

		#look for alien-ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _check_bullet_alien_collisions(self):
		"""respond to bullet-alien collisions"""
		#remove any bullets and aliens that have collided
		#check for bullets that have hit aliens, if so, get rid of both
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True) #the true's mean that the bullets and aliens
		#will dissappear when you hit them

		if not self.aliens: #checking to see if the alien group is empty
			#destroy existing bullets and create a new fleet
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

	def _check_events(self): #THIS IS THE HELPER METHOD, it helps the main method
		"""respond to keyboard/mouse events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos() #restricting valid mouse clicks to button
				#get_pos returns tuple of x y mouse location
				self._check_play_button(mouse_pos) #send coordinates to the next method (check play button)

			elif event.type == pygame.KEYDOWN: #if the event does not evaluate to quit
				self._check_keydown_events(event)

			elif event.type == pygame.KEYUP: #else, if the event type is a key up
				self._check_keyup_events(event)

	def _check_keydown_events(self, event): #this is a helper method
		"""respond to keypresses"""
		if event.key == pygame.K_RIGHT: #check to see if the key that was pressed is right. if so:
			self.ship.moving_right = True #move the ship to the right
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self,event): #this is a helper method
		"""respond to key releases"""
		if event.key == pygame.K_RIGHT: #if the key that was lifted was the right arrow
			self.ship.moving_right = False #stop the continuous movement
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _check_aliens_bottom(self):
		"""check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#treat this the same as if the ship got hit
				self._ship_hit()
				break

	def _check_play_button(self, mouse_pos):
		"""start a new game when the player clicks play"""
		easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
		medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
		hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

		if easy_button_clicked and not self.stats.game_active: 
			#if the button was clicked and the game active evaluates to true
			#reset the game statistics
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True

			#get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#hide the mouse
			pygame.mouse.set_visible(False)


		if medium_button_clicked and not self.stats.game_active: 
			#if the button was clicked and the game active evaluates to true
			#reset the game statistics
			 #speed settings-override the normal settings
			self.settings.initialize_dynamic_settings()
			self.settings.ship_speed = 5.0
			self.settings.bullet_speed = 6.0
			self.settings.alien_speed = 2.0
			

			self.stats.reset_stats()
			self.stats.game_active = True

			#get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#hide the mouse
			pygame.mouse.set_visible(False)


		if hard_button_clicked and not self.stats.game_active: 
			#if the button was clicked and the game active evaluates to true
			#reset the game statistics
			#speed settings
			self.settings.initialize_dynamic_settings()
			self.settings.ship_speed = 5.0
			self.settings.bullet_speed = 6.0
			self.settings.alien_speed = 3.0
			

			self.stats.reset_stats()
			self.stats.game_active = True

			#get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#hide the mouse
			pygame.mouse.set_visible(False)


	def _fire_bullet(self):
		"""create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet) #add method is similar to the append method, just for pygame

	def _create_fleet(self):
		"""create the fleet of aliens"""
		#make an alien and find the number of aliens in a row
		#spacing between each alien is equal to one alien width
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width) #note, 2 variable can only be an int, not float

		#determine the number of rows of aliens that fit on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height -
								 (3 * alien_height) - ship_height)
		number_rows = available_space_y // (3 * alien_height)

		#create the first row of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		#create an alien and place it in the row
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)#creating an instance of alien and then adding it to the group 
		#that will hold the fleet

	def _check_fleet_edges(self):
		"""respond appropriately if any aliens have reached an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _ship_hit(self):
		"""respond to the ship being hit by an alien"""
		if self.stats.ships_left > 0:
			#decrement ships_left
			self.stats.ships_left -= 1

			#get rid of any remaining alines and bullets
			self.aliens.empty()
			self.bullets.empty() #here we are emptying the group/list

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#pause
			sleep(0.5)
		else:
			self.stats.game_active = False #ends the game if the player runs out of ships
			pygame.mouse.set_visible(True)

	def _change_fleet_direction(self):
		"""drop the entire fleet and change the fleet's direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self): #this is another helper method!
		"""update images on screen, flip to new screen"""
		self.screen.fill(self.settings.bg_color)#redraw the screen during each pass through the loop
		self.ship.blitme() #draws ship to center bottom of screen, appears on top of background
		for bullet in self.bullets.sprites():
			bullet.draw_bullet() #this is drawing all the grouped sprites on the screen
		self.aliens.draw(self.screen) #draws the alien on the screen, draw method requires one argument:
		#a surface upon which to draw the selement from the group on
		
		#draw button screen if game is inactive
		if not self.stats.game_active:
			self.easy_button.draw_easy_button()
			self.medium_button.draw_medium_button()
			self.hard_button.draw_hard_button()

		pygame.display.flip()#make the most recently drawn screen visible, keeps playing smooth



if __name__ == '__main__': #if the file is being run directly, run this if block
	#make the game instance and run the game
	ai = AlienInvasion()
	ai.run_game()