class StateStack:
	""" Manages game states via stack. Surprisingly lightweight code."""
	def __init__(self):
		self.stack = []

	def update(self):
		self.stack[-1].update() # update from top of stack

	def input(self):
		self.stack[-1].input() # handles state input and returns exit 
								# code, if any

	def push(self, state): 	
		state.owner = self
		self.stack.append(state) # make sure states have necessary stuff for 
		self.stack[-1].onEnter() # onEnter() before this is called
								
	def pop(self):
		p = self.stack[-1].pop_pass
		s = self.stack.pop()
		s.onExit()
		self.stack[-1].pop_get = p
		return s