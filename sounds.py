import constants as c
import pygame
import time

cursor_move = pygame.mixer.Sound("move_cursor.wav")
cursor_select = pygame.mixer.Sound("select_cursor.wav")
#cursor_select = pygame.mixer.Sound("thwomp.wav")
attack = pygame.mixer.Sound("Shwing.wav")

cursor_move.set_volume(1.0)
cursor_select.set_volume(1.0)
attack.set_volume(1.0)