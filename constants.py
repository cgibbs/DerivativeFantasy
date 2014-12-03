import pygame
import stateStack
import inventory as inv

""" This file holds all the constants that are necessary for multiple parts.
	Cleverly allows me to avoid passing the screen stuff to each state."""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FONT_SIZE = 12

pygame.mixer.pre_init(44100, -16, 1, 2048)

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TEXT12 = pygame.font.Font("freesansbold.ttf", FONT_SIZE)

gameStack = stateStack.StateStack()

rnd = 1 # current round

inventory = inv.Inventory()

team = []		# global player character list

damage_mod = 1 	# modified by hacker challenge hashes; allows things like 
				#"double damage bonus"; make sure to reset in CombatState's
				# onExit(); this concept is easily extensible for other bonuses