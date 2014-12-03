class Spell:
	def __init__(self, name, effects):
		""" self.effects is a tuple to be handled by CombatState."""
		self.name = name
		self.effects = effects

class Spellbook:
	""" Component for storing and casting spells. Attached to Objects to make
		them spellcasters, AKA unclean heathens in the eyes of the Christian
		God. (I don't think Hammurabi would be cool with it, either.)"""
	def __init__(self, spells=None):
		""" Takes an optional list of spells, which are just fancy tuples."""
		self.spells = spells