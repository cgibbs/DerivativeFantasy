import constants as c

class Inventory:
	""" The methods involving inventory management. Not strictly necessary,
		but it makes the code easier to read, so whatevs. Keys are item names,
		values are quantities of items."""
	def __init__(self):
		self.inventory = {}

	def add_item(self, item, amount=1):
		try:
			self.inventory[item] += amount
		except:
			self.inventory[item] = amount

	def remove_item(self, item, amount=1):
		try: 
			if self.inventory[item] >= amount:
				print "able to remove from inventory"
				self.inventory[item] -= amount
				if self.inventory[item] == 0:
					print "out of " + item.name + "; removing item from inventory"
					self.inventory.pop(item)
			else:
				print "tried to remove too many of " + item.name
		except:
			print item.name + " not in inventory."
		
	def keys(self):
		return self.inventory.keys()