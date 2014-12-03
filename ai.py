import random
import constants as c

class BasicMonster:
    """ AI component for basic (semi-brainless) monster. Attached to Objects to
        give them a cruel mockery of life."""
    def __init__(self):
        pass
            
    def take_turn(self, enemies):
        # what're you doing?
        # oh, just monster things.
        choice = random.randint(0,len(enemies)-1)
        return ("attack", enemies[choice], enemies[choice].name)