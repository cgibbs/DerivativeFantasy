__metaclass__ = type

import pygame

class State:
	""" Base class, extend for actual state classes."""
	def __init__(self):
		self.owner = ""
		self.pop_pass = "" # used for passing values to next state underneath
		self.pop_get = "" # used for getting values from the state above
	def update(): 
		# do logic here, draw at the end
		pass
	def input(self):
		# do input here
		pass
	def onEnter(self):
		# do one-time start stuff here
		pass
	def onExit(self):
		# do one-time exit stuff here
		pass

class EmptyState(State):
	# when stack pops to this state, exit
	def update(self):
		print "all states popped, exiting game"
		self.owner.pop()
		pygame.quit()

	def input(self):
		pass
