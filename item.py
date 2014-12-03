import constants as c

# TODO: replace message() calls

class Item:
    """ Component for an item that can be acquired and used. Attached to 
        Objects to give them these characteristics. use_function is a tuple, 
        containing command values to pass to the CombatState/ShopState."""
    def __init__(self, use_function, choose_target):
        self.use_function = use_function
        self.choose_target = choose_target

    def use(self):
        c.inventory.remove_item(self)
        return self.use_function



class Equipment:
    # an object that can be equipped to provide bonuses
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0, max_mana_bonus=0):
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.max_mana_bonus = max_mana_bonus
        self.slot = slot 
        self.is_equipped = False

    def equip(self, character):
        # not actually meant to be called by anything other than character.equip();
        # equip object and remove from global inventory
        # dequip old item first
        old_equipment = get_equipped_in_slot(self.slot, character)
        if old_equipment is not None:
            old_equipment.dequip()
        self.is_equipped = True
        character.inv.append(self.owner)
        c.inventory.remove_item(self.owner)

        #message('Equipped ' + self.owner.full_name + ' on ' + self.slot + '.', libtcod.light_green)        

    def dequip(self):
        # not actually meant to be called by anything other than character.dequip()
        # dequip object and add back to global inventory
        if not self.is_equipped:
            return
        self.is_equipped = False
        c.inventory.add_item(self.owner)

        #message('Dequipped ' + self.owner.full_name + ' from ' + self.slot + '.', libtcod.light_yellow)



class Weapon(Equipment):
    def __init__(self, slot, attack_dice, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        Equipment.__init__(self, slot, power_bonus, defense_bonus, max_hp_bonus)
        self.attack_dice = attack_dice

    def equip(self, character):
        r_hand_check = get_equipped_in_slot('right hand', character)
        if r_hand_check is not None:
            old_equipment = get_equipped_in_slot('left hand', character)
            self.slot = 'left hand'
        else:
            old_equipment = r_hand_check
            self.slot = 'right hand'
        Equipment.equip(self)

    def dequip(self):
        Equipment.dequip(self)
        self.slot = 'hand'



def get_equipped_in_slot(slot, character):
    for obj in character.inv:
        if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
            return obj.equipment

def get_all_equipped(character): 
    equipped_list = []
    for item in character.inv:
        if item.equipment and item.equipment.is_equipped:
            equipped_list.append(item.equipment)
    return equipped_list