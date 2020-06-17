"""
Sailing algorithm 

So far the boats speed is dependant on whether the sail is set 
to be in the same direction as the wind which is wrong in real life. 
However this was a simple approach to start off with 

"""
import math
import pygame
import random


class wind:

	def __init__(self, pos, force, direction):
		self.pos = pos
		self.force = force
		self.direction = direction

	def paint(self):
		""" to paint the wind direction we need to convert into vectors """

		self.x = math.cos(self.direction)
		self.y = math.sin(self.direction)

		"""Draw a line with x and y vectors shown"""
		pygame.draw.line(screen, (255,0,0), (self.pos[0],self.pos[1]), (self.y*50+self.pos[0],self.x*50+self.pos[1]), 2)
		pygame.draw.circle(screen, (255,0,0), (self.pos[0],self.pos[1]), 55, 2)


	def alter_wind(self):

		self.direction += (random.randint(-1,1)/10)


class sailboat:

	def __init__(self, pos, saildirection, direction, speed):
		self.pos = pos
		self.saildirection = saildirection
		self.direction = direction
		self.speed = speed
	
	def paint(self):
			
		# For now we are just goin to draw a line for the boats hull 
		self.x = math.sin(self.direction)
		self.y = math.cos(self.direction)

		self.sailx = math.sin(self.saildirection)
		self.saily = math.cos(self.saildirection)

		pygame.draw.line(screen, (0,0,255), (self.pos[0],self.pos[1]), (self.saily*50+self.pos[0],self.sailx*50+self.pos[1]), 2)
		pygame.draw.line(screen, (0,255,0), (self.pos[0],self.pos[1]), (self.y*50+self.pos[0],self.x*50+self.pos[1]), 2)

		# pygame.draw.arc(screen, (0, 255, 0), (100,100,100,100), 1,2,1 )
		# pygame.draw.arc(screen, (0, 255, 0), (100,100,200,200), 1,2,1 )
		
	def move(self):

		self.x = math.cos(self.direction)
		self.y = math.sin(self.direction)

		self.pos = (self.pos[0]-(self.speed*self.x), self.pos[1]-(self.speed*self.y))

	def calculate_speed(self, winddirection):
		"""
		calculate speed based on where the sail is in relation to the wind
		"""
		angle_difference = abs(self.saildirection - winddirection)

		self.speed = 10*math.cos(angle_difference)+10



	def pull_in_sail(self):
		#Pulling in the sail will close the gap between the direction
		#of sail and direction of boat
		pass

	def let_sail_out(self):
		#letting out sail will open the gap between the direction of
		#of the boat and the direction of the sail
		pass


pygame.init()

screen = pygame.display.set_mode((1200,1200))

screen.fill((0,0,0))

a = wind((1100,100),10,(180*(2*math.pi))/360)
a.paint()
#a.alter_wind()

b = sailboat((300,300),(210*(2*math.pi))/360,(190*(2*math.pi))/360,10)
b.calculate_speed(a.direction)
b.paint()

c = sailboat((600, 600), (210*(2*math.pi))/360,(190*(2*math.pi))/360,10)


while True:
	# a = wind((1100,100),10,(180*(2*math.pi))/360).paint()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop = 0 

	
	# Clear Screen
	screen.fill((0,0,0))

	# update sprites
	
	b.paint()
	b.direction += 0.1
	b.calculate_speed(a.direction)
	b.move()
	c.paint()
	c.direction -= 0.1
	c.calculate_speed(a.direction)
	c.move()


	a.alter_wind()
	a.paint()
	
	pygame.display.update()
pygame.quit()