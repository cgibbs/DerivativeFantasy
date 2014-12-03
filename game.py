import pygame
import state
import menuState as menu
import constants as c
import baseObject
import fighter
import combatState as combat
import spritesheet
import ai
import item
import sounds
import monsters


c.SCREEN.fill((200,200,200))

def main():
	# test characters here; monsters will be initialized in gameState

	f1 = fighter.Fighter(10,4,4,(1,6),2,0)
	f2 = fighter.Fighter(10,4,4,(1,6),2,0)
	f3 = fighter.Fighter(10,4,4,(1,6),2,0)
	f4 = fighter.Fighter(10,4,4,(1,6),2,0)

	pc1 = baseObject.Object("PC1", spritesheet.spritesheet("FF1.png").load_strip((0,0,70,70), 7, (195,195,195)), fighter=f1)
	pc2 = baseObject.Object("PC2", spritesheet.spritesheet("FF1.png").load_strip((0,70,70,70), 7, (195,195,195)),fighter=f2)
	pc3 = baseObject.Object("PC3", spritesheet.spritesheet("FF1.png").load_strip((0,140,70,70), 7, (195,195,195)),fighter=f3)
	pc4 = baseObject.Object("PC4", spritesheet.spritesheet("FF1.png").load_strip((0,210,70,70), 7, (195,195,195)),fighter=f4)

	mon1 = monsters.makeSmallMon("Imp", "imp")
	mon2 = monsters.makeSmallMon("Skeleton", "skeleton")

	c.team.append(pc1)
	c.team.append(pc2)
	c.team.append(pc3)
	c.team.append(pc4)

	item1 = baseObject.Object("Healing Potion", item=item.Item(("heal", 20), choose_target=True))
	c.inventory.add_item(item1)

	sword1 = baseObject.Object("Masamune", equipment=item.Equipment("hand", power_bonus=10))
	c.inventory.add_item(sword1)
	pc1.equip(sword1)

	enemies = [mon1, mon2]

	e = state.EmptyState()
	c.gameStack.push(e)
	c.gameStack.push(combat.CombatState(enemies))

	while True:
		c.gameStack.update()
		pygame.display.flip()
		c.gameStack.input()

if __name__ == "__main__":
	main()
	pygame.quit()