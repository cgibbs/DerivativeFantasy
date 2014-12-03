import pygame
import random
import state
import spritesheet
import constants as c
import menuState as menu
import sounds

MESSAGES_TOP_Y = 400

# TODO: Implement a message list and buffer

class CombatState(state.State):
	""" Handles all combat. Creates menu trees, handles AI, and is the heart
		of the gameplay."""
	def __init__(self, enemies):
		super(CombatState, self).__init__()
		self.enemies = enemies
		self.curCharacter = None
		self.command = None

		self.turn_list = []

		self.messages = ["Test", "Derpity Doo"]

	def turnOrder(self):
		# determine turn order (currently debug code, set this up properly later)
		self.turn_list = c.team[:]
		for i in self.enemies:
			self.turn_list.append(i)
		for i in self.turn_list:
			print i.name
		self.curCharacter = self.turn_list[0]
		

	def parseCommand(self):
		""" command should be a tuple of strings and objects; the strings 
			determine the actions taken by/on the objects."""
		# if command[0] == "attack":
		#	do attack stuff
		# elif command[0] == "item":
		#	do item stuff
		# etc.

		# this is done before the turn, in case curCharacter is killed during turn
		ind = self.turn_list.index(self.curCharacter)

		if (self.command is not None) and self.command != "":
			# handle command
			# TODO: Maybe make command a class, to clarify code?
			print self.command

			if self.command[0] == "attack":
				sounds.attack.play()
				# TODO: take return value from attack, put it in message box
				self.messages += self.curCharacter.fighter.attack(self.command[1])
				print self.command[1].fighter.hp
				if self.command[1].fighter.isDead:
					self.turn_list.remove(self.command[1])
					print "he ded"

			if self.command[0] == "use":
				# TODO: do item use stuff
				c.inventory.remove_item(self.command[-2])

			# TODO: parse other commands

			# next character's turn
			# if curCharacter died this turn, don't increment ind, because
			# he is removed from turn_list, and next character now occupies
			# the position at ind
			if not self.curCharacter.fighter.isDead:
				ind += 1
			# check ind regardless of death; it may still be out of range
			if ind > len(self.turn_list) - 1:
				ind = 0
			self.curCharacter = self.turn_list[ind]
		else:
			print "Doing nothing, turn does not progress."

	def createMenuTree(self, character):
		""" create menu tree algorithmically"""
		# menu contains the following:
		#	Fight (list of monsters (and player characters?))
		#	Magic (list of spells, which each can target monsters (and PCs))
		#	Item (list of items in global inventory, which can target the user)
		#	Bonus (list of usable bonuses gained from hacking challenges)
		#	Run (no options, and you're a sissy for even considering it)
		root = menu.Node("root", "{0}, choose an option:".format(self.curCharacter.name), None)
		
		fight = menu.Node("fight", "Choose your target:", None)
		root.addChild(fight)
		for i in self.enemies:
			# eventually replace these with more nested for loops to fill in 
			# sub-menu options
			if not i.fighter.isDead:
				fight.addChild(menu.Node(i.name, "a jerk", ("attack", i, i.name))) 
		for i in c.team:
			if not i.fighter.isDead:
				fight.addChild(menu.Node(i.name, "a cool dude", ("attack", i, i.name)))
		
		magic = menu.Node("magic", "Choose your spell:", None)
		root.addChild(magic)
		if self.curCharacter.spellbook is not None:
			# TODO: actual magic stuff
			magic.addChild(menu.Node("SPELL", "ain't a goddamn thing", ("cast", "spell", "target")))
			pass
		else:
			# basically an empty menu, to give visual feedback
			magic.addChild(menu.Node("NOTHING", "ain't a goddamn thing", None))

		item = menu.Node("item", "Choose your item:", None)
		root.addChild(item)
		for i in c.inventory.keys():
			if i.item.choose_target:
				targeted_item = menu.Node(i.name, "Use {0} on:".format(i.name), None)
				for j in c.team:
					t = ("use",) + (i.item.use_function) + (j, j.name) + (i, i.name)
					targeted_item.addChild(menu.Node(j.name, "using that shit, son", t))
				item.addChild(targeted_item)
			else:
				item.addChild(menu.Node(i.name, "a great item!", i.item.use_function))
		# basically an empty menu, to give visual feedback
		item.addChild(menu.Node("NOTHING", "ain't a goddamn thing", None))
				
		root.addChild(menu.Node("run", "COWARD", ("parse", "my", "failure")))

		return root

	def drawScreen(self):
		# drawing stuff
		c.SCREEN.fill((200,200,200))
		tempHeight = 30	# running height total for drawing sprites vertically
		for i in range(len(c.team)):
			if not c.team[i].fighter.isDead:
				c.SCREEN.blit(c.team[i].sprites[0], (720, tempHeight))
				if c.team[i] == self.curCharacter:
					# TODO: Figure out why this isn't drawing
					tri = [(tempHeight + 30, 700), (tempHeight + 40, 700), (tempHeight + 35, 708)]
					pygame.draw.polygon(c.SCREEN, (0,0,0), tri)
				tempHeight += c.team[i].sprites[0].get_height() + 10
		tempHeight = 30
		for i in range(len(self.enemies)):
			if not self.enemies[i].fighter.isDead:
				c.SCREEN.blit(self.enemies[i].sprites[0], (10, tempHeight))
				tempHeight += self.enemies[i].sprites[0].get_height() + 10

		# TODO: draw message buffer
		pygame.draw.rect(c.SCREEN, (0,0,0), pygame.Rect(0,MESSAGES_TOP_Y,c.SCREEN_WIDTH, c.SCREEN_HEIGHT - MESSAGES_TOP_Y))
		buf = self.messages[-12:]
		for i in range(1,len(buf)+1): 
			text = c.TEXT12.render(buf[i-1], True, (255,255,255))
			text_rect = text.get_rect(bottomleft=(50,MESSAGES_TOP_Y + 10 + 14 * i))
			c.SCREEN.blit(text, text_rect)

		

	def onEnter(self):
		self.turnOrder()

	def update(self):
		# handle command parsing here
		if not self.curCharacter.ai:
			# this actually pulls and interprets the command from the menu
			# state of the previous call, so it'll parse nothing the "first"
			# time this state is updated
			self.command = self.pop_get
		else:
			# do ai stuff
			self.command = self.curCharacter.ai.take_turn(c.team)
		self.parseCommand()

		self.drawScreen()
		
		if not self.curCharacter.ai:
			# if not ai, push menu
			m = menu.MenuState(self.createMenuTree(self.curCharacter))
			self.owner.push(m)
			

	def input(self):
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				pygame.quit()

	def onExit(self):
		# reset temporary bonus mods
		c.damage_mod = 1