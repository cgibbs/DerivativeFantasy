import pygame
import random
import constants as c
import item

# TODO: replace message() calls with call to combat state to display message in message area?

class Fighter:
    """ Component for combat-related properties and methods. Attached to 
    	Objects to give them these characteristics."""
    def __init__(self, hp, defense, power, attack_dice, initiative, xp, mana=0, death_function=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_max_mana = mana
        self.mana = mana
        self.base_defense = defense
        self.base_power = power
        self.attack_dice = attack_dice
        self.initiative = initiative
        self.xp = xp
        self.death_function = death_function

        self.isDead = False

    @property
    def power(self):
        bonus = sum(equipment.power_bonus for equipment in item.get_all_equipped(self.owner))
        return self.base_power + bonus

    @property
    def defense(self):
        bonus = sum(equipment.defense_bonus for equipment in item.get_all_equipped(self.owner))
        return self.base_defense + bonus

    @property
    def max_hp(self):
        bonus = sum(equipment.max_hp_bonus for equipment in item.get_all_equipped(self.owner))
        return self.base_max_hp + bonus

    @property
    def max_mana(self):
        bonus = sum(equipment.max_mana_bonus for equipment in item.get_all_equipped(self.owner))
        return self.base_max_mana + bonus

    @property
    def health_status(self):
        p = (self.hp * 100) / self.max_hp
        if p > 80:
            return 'Healthy'
        elif p > 60:
            return 'Lightly Injured'
        elif p > 40:
            return 'Injured'
        elif p > 20:
            return 'Badly Injured'
        elif p > 0:
            return 'Nearly Dead'
        elif p == 0:
            return 'Dead'
        
    def take_damage(self, damage):
        # separate from attack, for uses with stuff like poisons
        message = ""
        if damage > 0:
            self.hp -= damage
            message = self.owner.name + "takes " + str(damage) + " points of damage. "

        if self.hp <= 0:
            self.isDead = True
            message += self.owner.name + " is dead!"

        return message

    def attack(self, target):
        message = []
        damage = (self.power/2)
        if (self.owner.inv is not None):
            for obj in self.owner.inv:
                if isinstance(obj.equipment, item.Weapon):
                    if obj.equipment.is_equipped:
                        damage += roll_dice(obj.equipment.attack_dice)
        else:
            damage += roll_dice(self.attack_dice)
        damage -= (target.fighter.defense/2)

        message.append(self.owner.name + " attacks " + target.name + ".")

        if damage > 0:
            #message(self.owner.full_name + ' attacks ' + target.full_name + ' for ' + str(damage) + ' hit points.')
            message.append(target.fighter.take_damage(damage))
        
        return message


    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

def roll_dice(dice):
	""" dice should be a tuple; 2d6 would simply be (2,6)"""
	return c.damage_mod * sum(random.randint(1,dice[1]) for i in range(0,dice[0]+1))