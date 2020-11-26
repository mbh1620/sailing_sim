import pygame


class Course:

	def __init__(self, pygame_instance):
		self.pygame_instance = pygame_instance



	def draw_course(self):
		#First start with the starting line
		pygame.draw.circle(self.pygame_instance, (255,0,0), (700,600), 5, 2)
		pygame.draw.circle(self.pygame_instance, (255,0,0), (900,600), 5, 2)
		#Windward mark
		pygame.draw.circle(self.pygame_instance, (255,0,0), (800,100), 5, 2)
		#Next Mark
		pygame.draw.circle(self.pygame_instance, (255,0,0), (300,300), 5, 2)
		#Leward Mark
		pygame.draw.circle(self.pygame_instance, (255,0,0), (300,800), 5, 2)
		pygame.draw.circle(self.pygame_instance, (255,0,0), (600,900), 5, 2)


