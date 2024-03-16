import pygame
from pygame.locals import *
import random
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.Font('fonts/LilitaOne-Regular.ttf', 45)
fpsfont = pygame.font.Font('fonts/LilitaOne-Regular.ttf', 25)

#define colours
white = (255, 255, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
saved = False
win = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
bestscore = 0
oldscore = 0
pass_pipe = False
hearts = 3


#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')#ground images
button_img = pygame.image.load('img/restart.png')#button image
heart = pygame.image.load('img/heart.png') # heart value image

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#restart our game
def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	score = 0
	return score

#class of our ptichka
class Ptichka(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range (1, 4):
			img = pygame.image.load(f"img/ptichka{num}.png")
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):

		if flying == True:
			#apply gravity
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			#jump
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			#animation
			flap_cooldown = 5
			self.counter += 1
			
			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
				self.image = self.images[self.index]


			#rotate the bird
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			#point the bird at the ground
			self.image = pygame.transform.rotate(self.images[self.index], -90)


#our pipe(truba)
class Tpyba(pygame.sprite.Sprite):

	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/truba.png")
		self.rect = self.image.get_rect()
		#position variable determines if the pipe is coming from the bottom or top
		#position 1 is from the top, -1 is from the bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		elif position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]


	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()


#knopka
class Knopka():
	def __init__(self, x, y, image): #initilization
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action



pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Ptichka(100, int(screen_height / 2))

bird_group.add(flappy)

#create restart button instance
button = Knopka(screen_width // 2 - 50, screen_height // 2 - 100, button_img)


run = True
while run: #game loop

	clock.tick(fps) #our clock() method and bind him to fps

	#draw background
	screen.blit(bg, (0,0))

    #drawing
	pipe_group.draw(screen)
	bird_group.draw(screen)
	bird_group.update()

	#draw and scroll the ground
	screen.blit(ground_img, (ground_scroll, 768))
	screen.blit(heart, (790, 10))

	#check the score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				if score == 100 and score <= 105:
					hearts += 1
				elif score == 200 and score <= 204 or score == 300 and score <= 301:
					hearts += 2
				elif score == 500 and score <= 503:
					hearts += 3

				if pipe_gap >= 50:
					pipe_gap -= 0.5
				while pipe_gap >= 400:
					pipe_frequency -= 25
				fps += 1
				#score sys
				if score < 60:
					score += 6
				elif score >= 60 and score <= 124:
					score += 5
				elif score >= 125 and score <= 149:
					score += 4
				elif score >= 150 and score <= 199:
					score += 3
				elif score >= 200 and score <= 999:
					score += 2
				else:
					score += 0
				pass_pipe = False
	draw_text("score:" + str(score), font, white, int(screen_width / 2.45), 10)#score drawing
	draw_text(str(hearts), fpsfont, white, 807, 20)#val of hearts draw
	if score >= 200 and score <= 299:
		draw_text("score:" + str(score), font, (255, 223, 0), int(screen_width / 2.45), 10)#score drawing
	elif score >= 300:
		draw_text("score:" + str(score), font, (60, 0, 100), int(screen_width / 2.45), 10)#score drawing

	if fps >= 50:
		draw_text("fps:" + str(fps), fpsfont, green, int(screen_width / 15.6), 30)#fps draw
	elif fps >= 30:
		draw_text("fps:" + str(fps), fpsfont, yellow, int(screen_width / 15.6), 30)#fps draw
	else:
		draw_text("fps:" + str(fps), fpsfont, red, int(screen_width / 15.6), 30)#fps draw
	draw_text("last:" + str(oldscore), fpsfont, white, int(screen_width / 1.44), 30)# last score draw
	if oldscore == 1000:
		draw_text("last:" + str(oldscore) + "(max)", fpsfont, white, int(screen_width / 1.44), 30)# last score draw
	draw_text("best:" + str(bestscore), fpsfont, white, int(screen_width / 5.66), 30)# best score draw
	if bestscore == 1000:
		draw_text("best:" + str(bestscore) + "(max)", font, white, int(screen_width / 5.66), 30)# best score draw


	#look for collision
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		if hearts > 0:
			collision = pygame.sprite.spritecollide(flappy, pipe_group, False)
			if collision:
				# Видаляємо тільки першу трубу зі списку зіткнень
				collision[0].kill()
			hearts -= 1
		else:
			game_over = True

	#once the bird has hit the ground it's game over and no longer flying
	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False
	if flappy.rect.bottom <= 0:
		game_over = True
		flying = False


	if flying == True and game_over == False:
		#generate new pipes
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Tpyba(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Tpyba(screen_width, int(screen_height / 2) + pipe_height, 1)
			tpyabachislospawn = random.randint(0, 2) #random to spawn our pipe,0 to spawn btm_pipe, 1 to spawn top_pipe,2 to spawn both
			heartrandom = random.randint(0, 15)	 # random to spawn our hearts
			if score >= 200:
				tpyabachislospawn = 2

			if heartrandom == 15:
				hearts += 1
				draw_text("heart +" + str(hearts), fpsfont, white, 784, 40)#hear plus draw

			if tpyabachislospawn == 0:
				pipe_group.add(btm_pipe)
			elif tpyabachislospawn == 1:
				pipe_group.add(top_pipe)
			elif tpyabachislospawn == 2:
				pipe_group.add(btm_pipe)
				pipe_group.add(top_pipe)
			last_pipe = time_now

		pipe_group.update()

		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0
	

	#check for game over and reset
	if game_over == True and score < 1000:
		lose = draw_text("DEFEAT!!!!", fpsfont, red, int(screen_width / 2.15), 250)
		if button.draw():
			game_over = False
			oldscore = score
			pipe_gap = 150
			hearts = 3
			pipe_frequency = 1500
			if oldscore > bestscore:
				bestscore = oldscore
			score = reset_game()
			fps = 60 # reset fps to default,coz pygame use fps to do our events,if we have 30 fps our event doing so slow,but if we have 144 fps our events doing so fast

	if score >= 1000:
		win = True
		flying = False
		game_over = True
		win = draw_text("VICTORY!!!!", fpsfont, green, int(screen_width / 3.15), 250)
		if button.draw():
			game_over = False
			flying = True
			win = False
			oldscore = score
			pipe_gap = 150
			hearts = 3
			pipe_frequency = 1500
			if oldscore > bestscore:
				bestscore = oldscore
			score = reset_game()
			fps = 60 # reset fps to default,coz pygame use fps to do our events,if we have 30 fps our event doing so slow,but if we have 144 fps our events doing so fast



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update() #update the display

pygame.quit() #end our pygame