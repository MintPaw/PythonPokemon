from Monster import *

monsters = []

def loadMonsterInfo():
	global monsters

	f = open("info/monsters", "r")
	monstersDefs = f.read().split("-")
	f.close();

	for i in monstersDefs:
		m = Monster()
		i = i.replace("\n", "")
		i = i.replace(" ", "")
		singleMonster = i.split("|")

		for j in singleMonster:
			stat = j.split(":")
			if (stat[0] == "name"): m.name = stat[1]
			if (stat[0] == "speed"): m.speed = int(stat[1])
			if (stat[0] == "attack"): m.attack = int(stat[1])
			if (stat[0] == "defense"): m.defense = int(stat[1])
			if (stat[0] == "health"): m.health = int(stat[1])
		monsters.append(m)

			
	


def main():
	loadMonsterInfo()

if (__name__ == "__main__"): main()