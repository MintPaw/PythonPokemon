from Monster import *

pokemen = []

def getPokemonByID(id):
	global pokemen

	for i in pokemen:
		if i.id == id: return i



def loadMonsterInfo():
	global pokemen
	pokemen = []

	f = open("info/pokemon", "r")
	pokemon = f.read().split("\n")
	f.close();

	f = open("info/stats", "r")
	stats = f.read().split("\n")
	f.close();

	for i in pokemon:
		p = Pokemon()
		
		singlePokemon = i.split(",")

		p.id = int(singlePokemon[0])
		p.name = singlePokemon[1].capitalize()

		pokemen.append(p)

	for i in stats:
		singleStat = i.split(",")
		p = getPokemonByID(int(singleStat[0]))
		if (p == None): continue

		if (int(singleStat[1]) == 1): p.health = int(singleStat[2])
		if (int(singleStat[1]) == 2): p.attack = int(singleStat[2])
		if (int(singleStat[1]) == 3): p.defense = int(singleStat[2])
		if (int(singleStat[1]) == 6): p.speed = int(singleStat[2])



def main():
	global pokemen

	loadMonsterInfo()

	print(pokemen[100].id)
	print(pokemen[100].name)
	print(pokemen[100].health)
	print(pokemen[100].attack)
	print(pokemen[100].defense)
	print(pokemen[100].speed)


if (__name__ == "__main__"): main()