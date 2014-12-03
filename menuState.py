import pygame
import state
import constants as c
import sounds
import spritesheet

class Node:
	""" Node class for the (non-binary) menu tree structure."""
	def __init__(self, name, text, choice, children=None):
		self.name = name
		self.text = text
		self.choice = choice
		self.children = children
		if children is None:
			self.children = []
		self.parent = None

	def addChild(self, child):
		self.children.append(child)
		child.parent = self

	def sortChildren(self):
		self.children = self.children.sort()

class MenuState(state.State):
	""" Handles all of the menus for the combat and shop states. The states
		create the tree, and pass the root to this state."""
	def __init__(self, root):
		super(MenuState, self).__init__()
		self.root = root	# just in case
		self.cur_node = root
		self.root.parent = root
		self.cursor_loc = 0 # location of cursor for selection in the menu

		# fancy cheat code stuff
		self.cheat = [pygame.K_c, pygame.K_h, pygame.K_a, pygame.K_n, pygame.K_c, pygame.K_e]
		self.index = 0

	def update(self):
		# code to display message and options, then wait for input
		message = self.cur_node.text
		if len(message) > 50:
			message = message[:49]

		h = (len(self.cur_node.children) + 2) * c.FONT_SIZE # height of total menu text
		v_offset = (c.SCREEN_HEIGHT - h) / 2 # distance between top of screen and top of menu
		menuRect = pygame.Rect(90, v_offset, 610, h + (2 * c.FONT_SIZE))
		pygame.draw.rect(c.SCREEN, (0,0,0), menuRect)
		pygame.draw.rect(c.SCREEN, (100,100,100), menuRect, 5)

		m_text = c.TEXT12.render(message, True, (255,255,255))
		m_rect = m_text.get_rect(bottomleft = (90 + 10, v_offset + c.FONT_SIZE + 5))
		c.SCREEN.blit(m_text, m_rect)
		for i in range(len(self.cur_node.children)):
			if self.cursor_loc == i:
				o_text = c.TEXT12.render(">{0}".format(self.cur_node.children[i].name), True, (255,255,255))
			else:
				o_text = c.TEXT12.render("    {0}".format(self.cur_node.children[i].name), True, (255,255,255))
			o_rect = m_text.get_rect(bottomleft = (90 + 10, v_offset + (12 * (i +  3))))
			c.SCREEN.blit(o_text, o_rect)
		c.SCREEN.blit(m_text, m_rect)
		pygame.display.flip()

	def input(self):
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				pygame.quit()
			elif e.type == pygame.KEYDOWN:
				# cheat code stuff
				if e.key == self.cheat[self.index]:
					self.index += 1
				else:
					self.index = 0
				if self.index == len(self.cheat):
					print "cheat code activated"
					c.team[0].sprites = spritesheet.spritesheet("FF1.png").load_strip((0,280,70,70), 7, (195,195,195))
					self.index = 0
					self.owner.pop()

				# normal input stuff
				if e.key == pygame.K_UP:
					sounds.cursor_move.play()
					self.cursor_loc -= 1
					if self.cursor_loc < 0:
						self.cursor_loc = len(self.cur_node.children) - 1

				elif e.key == pygame.K_DOWN:
					sounds.cursor_move.play()
					self.cursor_loc += 1
					if self.cursor_loc > len(self.cur_node.children) - 1:
						self.cursor_loc = 0

				elif e.key == pygame.K_RETURN:
#					sounds.cursor_select.play()
					if len(self.cur_node.children[self.cursor_loc].children) > 0: # if has children
						sounds.cursor_select.play()
						self.cur_node = self.cur_node.children[self.cursor_loc]
						self.cursor_loc = 0
					else: 
						#self.cur_node.children[self.cursor_loc].choice() # do choice
						# do stuff to pass information here
						self.pop_pass = self.cur_node.children[self.cursor_loc].choice
						self.owner.pop() # exit menu

				elif e.key == pygame.K_BACKSPACE:
					self.cur_node = self.cur_node.parent
					self.cursor_loc = 0

	def onEnter(self):
		pass

	def onExit(self):
		pass