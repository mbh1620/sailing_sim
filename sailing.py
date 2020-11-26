"""
Sailing algorithm 

So far the boats speed is dependant on whether the sail is set 
to be in the same direction as the wind which is wrong in real life. 
However this was a simple approach to start off with 

"""
import math
import pygame
import random
import course 
import vessel



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

		self.direction = (math.radians(random.randint(-1,1)))


pygame.init()

#course initialisation
waypoints = []
#windward mark
waypoints.append(vessel.waypoint(815,85))
#next mark
waypoints.append(vessel.waypoint(300,300))
#leward mark
waypoints.append(vessel.waypoint(300,800))
waypoints.append(vessel.waypoint(600,900))


#startline
waypoints.append(vessel.waypoint(700,600))



waypoints.append(vessel.waypoint(815,85))
#next mark
waypoints.append(vessel.waypoint(300,300))
#leward mark
waypoints.append(vessel.waypoint(300,800))
waypoints.append(vessel.waypoint(600,900))
#startline
waypoints.append(vessel.waypoint(700,600))



screen = pygame.display.set_mode((1200,1200))

course1 = course.Course(screen)

screen.fill((0,0,0))

a = wind((1100,100),10,(180*(2*math.pi))/360)
a.paint()
#a.alter_wind()

course1.draw_course()

sailboats = []

x = 0

while x < 70:
	xx = random.randint(700,900)
	y = random.randint(600,700)
	sailboats.append(vessel.sailboat((xx,y),0,90,10, screen, waypoints, 0, -0.2))
	sailboats[x].activate_waypoint()
	x = x + 1

while True:
	# a = wind((1100,100),10,(180*(2*math.pi))/360).paint()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop = 0 

	
	# Clear Screen
	screen.fill((0,0,0))

	# update sprites

	for i in sailboats:
		i.paint()
		i.calculate_speed(a.direction)
		i.detect_upwind_sailing(a.direction)
		i.move()
		i.reached_waypoint(i.activated_waypoint)
		

	course1.draw_course()


	a.alter_wind()
	a.paint()
	
	pygame.display.update()
pygame.quit()