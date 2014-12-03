import pygame
import random
import state
import constants as c

class gameState(state.State):
	""" This state exists purely for throwing new encounters at the player.
		Should have an exit condition, eventually (probably a value of "dead"
		passed to it from the combat state)."""
	def __init__():
		pass

	def update(self):
		# should only get called once between (combat and shop) pairs
		# create and push in this order: combatState, shopState
		# create these based on number of successful encounters, i.e. bigger
		# 	monsters and better items as the game goes on
		pass

	def input(self):
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				pygame.quit()
