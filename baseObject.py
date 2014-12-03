import item as itemMod

class Object:
    """ Basic class for all items and actors. Characteristics are added by 
        attaching components (fighter, AI, item, etc.)."""
    def __init__(self, name, sprites=None, fighter=None, ai=None, equipment=None, item=None,
                 inv=None, spellbook=None, owner=None):
        self.name = name
        
        self.inv = inv # for equipment and monster item drops
        if not self.inv: 
            self.inv = [] # initialize an empty list

        self.owner = owner # object.owner only useful for equipment

        # components, owned by the Object, which allow special behaviors

        self.sprites = sprites

        self.fighter = fighter
        if self.fighter: # let the fighter component know who owns it
            self.fighter.owner = self

        self.ai = ai
        if self.ai: # let the ai component know who owns it
            self.ai.owner = self

        self.item = item
        if self.item: # let the item component know who owns it
            self.item.owner = self

        self.equipment = equipment
        if self.equipment: # let the equipment component know who owns it
            self.equipment.owner = self
            self.item = itemMod.Item(None, None) # a piece of equipment is always an Item (can be picked up and used)
            self.item.owner = self

        self.spellbook = spellbook
        if self.spellbook: # let the spellbook component know who owns it
            self.spellbook.owner = self

#    def get_equipped_in_slot(slot):
#        for obj in self.inv:
#            if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
#                return obj.equipment

    def equip(self, gear):
        # this exists purely to preserve understanding; player equips a sword,
        # as opposed to a sword equipping a player
        if gear.equipment:
            gear.equipment.equip(self)

    def dequip(self, gear):
        # this exists purely to preserve understanding; player dequips a sword,
        # as opposed to a sword dequipping a player
        if gear.equipment:
            gear.equipment.dequip(self)