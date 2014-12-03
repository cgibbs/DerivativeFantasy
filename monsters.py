import random
import fighter
import ai
import baseObject
import spritesheet

# temporary stuff here; need some sort of database of monsters, correlated to
# sprites and stats, which can be randomly created when a new CombatState is 
# pushed.

def makeSmallMon(name, mType, level=1):
	if mType == "imp":
		mType = 0
	elif mType == "skeleton":
		mType = 1
	elif mType == "wolf":
		mType = 2
	elif mType == "snake":
		mType = 3
	elif mType == "mudman":
		mType = 4
	elif mType == "scorpion":
		mType = 5
	elif mType == "madpriest":
		mType = 6
	else:
		print "not valid"
		mType = 0

	# TODO: make level stuff work here
	monFighter = fighter.Fighter(10,4,4,(1,6),2,0)
	monAI = ai.BasicMonster()
	mon = baseObject.Object(name, spritesheet.spritesheet("monsters.png").load_strip((70 * mType,0,70,70), 1, (195,195,195)),fighter=monFighter, ai=monAI)
	# do any other monster stuff here
	return mon