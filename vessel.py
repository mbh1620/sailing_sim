import math
import pygame
import random

class waypoint:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class sailboat:

	def __init__(self, pos, saildirection, direction, speed, pygame_instance, waypoints, tide_x, tide_y):
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
		self.tide_x = tide_x
		self.tide_y = tide_y
		self.upwind_waypoint1 = waypoint(0,0)
		self.upwind_waypoint2 = waypoint(0,0)
		self.upwind_waypoint = self.upwind_waypoint1
		self.flag = True
 
	
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

		self.pos = (self.pos[0]-(self.speed*self.x)+self.tide_x, self.pos[1]-(self.speed*self.y)+self.tide_y)

	def calculate_speed(self, winddirection):
		"""
		calculate speed based on where the sail is in relation to the wind
		"""
		angle_difference = abs(self.saildirection - winddirection)

		self.speed = 1.2*math.cos(angle_difference)+1

	def activate_waypoint(self):
		#activate the first waypoint in the array
		self.activated_waypoint = self.waypoints[0]

	def activate_upwind_mode(self, winddirection):
		#Activate the upwind mode calculates the next mini waypoints to add to the waypoints array at the front


		#----------------------------------------------------------------
		#	Step 1 - calculate the distance from wp to actual position
		#----------------------------------------------------------------

		distance = math.sqrt(abs(self.activated_waypoint.y-self.pos[1])**2 + abs(self.activated_waypoint.x-self.pos[0])**2)

		#--------------------------------------------------------------------------------------
		#	Step 2 - calculate two lines extending from the main waypoint separated by 15 deg either side of the wind direction
		#            to the distance calculated 
		#--------------------------------------------------------------------------------------

		#line equation y = mx + c

		right_line_angle = winddirection + 90 - 22.5
		left_line_angle = winddirection + 90 + 22.5

		r = distance

		pos2A_X = self.activated_waypoint.x + (distance*math.cos(math.radians(right_line_angle)))
		pos2A_Y = self.activated_waypoint.y + (distance*math.sin(math.radians(right_line_angle)))

		pos2B_X = self.activated_waypoint.x + (distance*math.cos(math.radians(left_line_angle)))
		pos2B_Y = self.activated_waypoint.y + (distance*math.sin(math.radians(left_line_angle)))

		#B is left line A is the Right line
		#pygame.draw.line(self.pygame_instance, (0,0,255), (self.activated_waypoint.x,self.activated_waypoint.y), (pos2A_X, pos2A_Y), 2)
		#pygame.draw.line(self.pygame_instance, (0,0,255), (self.activated_waypoint.x,self.activated_waypoint.y), (pos2B_X, pos2B_Y), 2)

		#We now know the second points for both lines so we can work out the gradients for both lines

		# so the gradient of a line is y1-y2/x2-x1

		# gradient of left line

		grad1 = (pos2A_Y - self.activated_waypoint.y)/(pos2A_X - self.activated_waypoint.x)

		grad2 = (self.activated_waypoint.y - pos2B_Y)/(self.activated_waypoint.x - pos2B_X)

		#we have the two gradients so we can now work out the y intercept of both lines by putting in a point on the line and solve for c

		'''
		Y = mx + c
		c = y-mx

		'''
		y = self.activated_waypoint.y
		x = self.activated_waypoint.x
		
		c1 = y - grad1*x
		c2 = y - grad2*x

		#Now we have our two line equations we now need to work out the two line equations for the vessel and equate them to each other to work out
		#at what point to tack

		boat_right_line = winddirection + 180 + 90 + 45
		boat_left_line = winddirection + 180 + 90 - 45

		r = distance

		pos3A_X = self.pos[0] + (distance*math.cos(math.radians(boat_right_line)))
		pos3A_Y = self.pos[1] + (distance*math.sin(math.radians(boat_right_line)))

		pos3B_X = self.pos[0] + (distance*math.cos(math.radians(boat_left_line)))
		pos3B_Y = self.pos[1] + (distance*math.sin(math.radians(boat_left_line)))

		#B is left A is the right hand line 
		#pygame.draw.line(self.pygame_instance, (0,0,255), (self.pos[0],self.pos[1]), (pos3A_X, pos3A_Y), 2)
		#pygame.draw.line(self.pygame_instance, (0,0,255), (self.pos[0],self.pos[1]), (pos3B_X, pos3B_Y), 2)

		#Now we need to work out the gradients of the lines of travel 

		grad_boat_1 = (self.pos[1]- pos3A_Y)/(self.pos[0]-pos3A_X)
		grad_boat_2 = (self.pos[1] - pos3B_Y) / (self.pos[0]-pos3B_X)

		#We can now work out the equations

		y = self.pos[1]
		x = self.pos[0]

		boat_c1 = y - grad_boat_1*x
		boat_c2 = y - grad_boat_2*x

		#we now need to equate the left two lines and find there cross point and do the same with the right lines and find their cross points
		
		#tack point 1
		var_x1 = (c1 - boat_c1)/(grad_boat_1+grad2) 
		var_y1 = boat_c1+grad_boat_1*var_x1

		var_x2 = (c2 - boat_c2)/(grad_boat_2+grad1)
		var_y2 = boat_c2 + grad_boat_2 * var_x2

		print(var_x1)
		print(var_y1)

		#pygame.draw.circle(self.pygame_instance, (255,0,0), (int(var_x1),int(var_y1)), 5, 2)
		#pygame.draw.circle(self.pygame_instance, (255,0,0), (int(var_x2),int(var_y2)), 5, 2)


		# num = random.randint(0,1)

		# if num == 1:


		# 	self.activated_waypoint.x = var_x1
		# 	self.activated_waypoint.y = var_y1

		# else:

		self.upwind_waypoint1.x = var_x1
		self.upwind_waypoint1.y = var_y1
		self.upwind_waypoint2.x = var_x2
		self.upwind_waypoint2.y = var_y2

		#self.steer_towards_WP(winddirection, self.upwind_waypoint)








	def steer_towards_WP(self, winddirection, waypoint):
		#Steer the boat towards the activated waypoint
		'''
		to steer towards waypoint, find waypoint x,y and self position x,y.
		Then find the angle between two points and then steer towards that heading

		'''
		angle = math.degrees(math.atan((waypoint.y-self.pos[1])/(waypoint.x-self.pos[0])))
		heading_to_steer_to = None

		adding_factor = None

		if (waypoint.x-self.pos[0]) > 0 and (waypoint.y - self.pos[1]) > 0:
			#heading_to_steer_to = #90 - angle
			heading_to_steer_to = 90 + angle + 90
		elif (waypoint.x-self.pos[0]) > 0 and (waypoint.y - self.pos[1]) < 0:
			#heading_to_steer_to = #90 + angle
			heading_to_steer_to = 90 + angle + 90
		elif (waypoint.x-self.pos[0]) < 0 and (waypoint.y - self.pos[1]) > 0:
			#heading_to_steer_to = 270 - angle
			heading_to_steer_to = 270 + angle + 90
		elif(waypoint.x-self.pos[0]) < 0 and (waypoint.y - self.pos[1]) < 0:
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
		factor = self.direction - 90 - winddirection

		if (self.direction - 90 - winddirection) > 180:
			factor = 360 - (self.direction - 90 - winddirection)

		elif (self.direction - 90 - winddirection) < -180:
			factor = -360 - (self.direction - 90 - winddirection)

		if abs(factor) < 90 and abs(factor) > -90:
			self.heading_upwind = True
			self.sailAngleLimit = 10
			self.pull_in_sail()

		elif abs(factor) < -90 or abs(factor) > 90:
			self.heading_upwind = False
			self.sailAngleLimit = 90
			self.let_sail_out()


	def detect_upwind_sailing(self,winddirection):
		if self.heading_upwind == True:
			self.activate_upwind_mode(winddirection)
			self.steer_towards_WP(winddirection, self.upwind_waypoint)
			self.reached_upwind_waypoint(self.upwind_waypoint)
		else:
			self.steer_towards_WP(winddirection, self.activated_waypoint)

	def reached_waypoint(self, waypoint):
		if abs(self.pos[0] - waypoint.x)<10 and abs(self.pos[1] - waypoint.y) < 10:
			self.num += 1
			self.activated_waypoint = self.waypoints[self.num]

	def reached_upwind_waypoint(self, waypoint):
		if abs(self.pos[0] - waypoint.x)<10 and abs(self.pos[1] - waypoint.y) < 10:
			if self.flag == True:
				self.upwind_waypoint = self.upwind_waypoint1
				self.flag = False
			else:
				self.upwind_waypoint = self.upwind_waypoint2
				print("switched waypoint")
				self.flag = True

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




