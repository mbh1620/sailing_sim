import math
import pygame

class waypoint:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class sailboat:

	def __init__(self, pos, saildirection, direction, speed, pygame_instance, waypoints):
		self.pos = pos
		self.direction = direction
		self.saildirection = saildirection
		self.sailAngle = 10
		self.sailAngleLimit = None
		self.speed = speed
		self.pygame_instance = pygame_instance
		self.activated_waypoint = None
		self.num = 0
		self.waypoints = waypoints
		self.heading_upwind = None #Will be a bool set to true or false depending on whether the vessel is going upwind or not

	
	def paint(self):
			
		# For now we are just goin to draw a line for the boats hull 
		self.x = math.sin(math.radians(self.direction))
		self.y = math.cos(math.radians(self.direction))

		self.sailx = math.sin(math.radians(self.saildirection))
		self.saily = math.cos(math.radians(self.saildirection))

		pygame.draw.line(self.pygame_instance, (0,0,255), (self.pos[0],self.pos[1]), (self.saily*50+self.pos[0],self.sailx*50+self.pos[1]), 2)
		pygame.draw.line(self.pygame_instance, (0,255,0), (self.pos[0],self.pos[1]), (self.y*50+self.pos[0],self.x*50+self.pos[1]), 2)

		# pygame.draw.arc(screen, (0, 255, 0), (100,100,100,100), 1,2,1 )
		# pygame.draw.arc(screen, (0, 255, 0), (100,100,200,200), 1,2,1 )
		
	def move(self):

		self.x = math.cos(math.radians(self.direction))
		self.y = math.sin(math.radians(self.direction))

		self.pos = (self.pos[0]-(self.speed*self.x), self.pos[1]-(self.speed*self.y))

	def calculate_speed(self, winddirection):
		"""
		calculate speed based on where the sail is in relation to the wind
		"""
		angle_difference = abs(self.saildirection - winddirection)

		self.speed = 1.2*math.cos(angle_difference)+1

	def activate_waypoint(self):
		#activate the first waypoint in the array
		self.activated_waypoint = self.waypoints[0]


	def steer_towards_WP(self, winddirection):
		#Steer the boat towards the activated waypoint
		'''
		to steer towards waypoint, find waypoint x,y and self position x,y.
		Then find the angle between two points and then steer towards that heading

		'''
		angle = math.degrees(math.atan((self.activated_waypoint.y-self.pos[1])/(self.activated_waypoint.x-self.pos[0])))
		heading_to_steer_to = None

		adding_factor = None

		if (self.activated_waypoint.x-self.pos[0]) > 0 and (self.activated_waypoint.y - self.pos[1]) > 0:
			#heading_to_steer_to = #90 - angle
			heading_to_steer_to = 90 + angle + 90
		elif (self.activated_waypoint.x-self.pos[0]) > 0 and (self.activated_waypoint.y - self.pos[1]) < 0:
			#heading_to_steer_to = #90 + angle
			heading_to_steer_to = 90 + angle + 90
		elif (self.activated_waypoint.x-self.pos[0]) < 0 and (self.activated_waypoint.y - self.pos[1]) > 0:
			#heading_to_steer_to = 270 - angle
			heading_to_steer_to = 270 + angle + 90
		elif(self.activated_waypoint.x-self.pos[0]) < 0 and (self.activated_waypoint.y - self.pos[1]) < 0:
			#heading_to_steer_to = 270 + angle
			heading_to_steer_to = 270 + angle + 90

		if ((self.direction - heading_to_steer_to) < 0 and (self.direction - heading_to_steer_to) > -180):
			self.direction += 2
		elif (self.direction -heading_to_steer_to) > 180:
			self.direction += 2
			self.direction -=360
		elif ((self.direction -heading_to_steer_to) > 0 and (self.direction - heading_to_steer_to) < 180):
			self.direction -= 2
		elif (self.direction -heading_to_steer_to) < -180:
			self.direction -= 2
			self.direction += 360
		elif(self.direction - heading_to_steer_to) == 0:
			self.direction = self.direction

		self.saildirection = self.direction + self.sailAngle

		#calculate whether sailing upwind 

		if abs(self.direction - winddirection) < 180:
			self.heading_upwind = True
			self.sailAngleLimit = 10
			self.pull_in_sail()
		elif abs(self.direction - winddirection) > -180:
			self.heading_upwind = False
			self.sailAngleLimit = 90
			self.let_sail_out()


	def reached_waypoint(self):
		if abs(self.pos[0] - self.activated_waypoint.x)<10 and abs(self.pos[1] - self.activated_waypoint.y) < 10:
			self.num += 1
			self.activated_waypoint = self.waypoints[self.num]

	def pull_in_sail(self):
		#Pulling in the sail will close the gap between the direction
		#of sail and direction of boat
		if self.sailAngle > self.sailAngleLimit:
			self.sailAngle -= 1

	def let_sail_out(self):
		#letting out sail will open the gap between the direction of
		#of the boat and the direction of the sail
		if self.sailAngle < self.sailAngleLimit:
			self.sailAngle += 1




