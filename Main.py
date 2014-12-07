from Monster import *
from tkinter import *
from _thread import *
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import socket
import pickle
import copy
import random

pokemen = []

pokemonList = None
partyList = None

sock = None
playing = False

playerNumber = None
enemyName = None
enemyNumber = None

party = None
enemyParty = None

currentMember = None
currentEnemyMember = None

root = None
connectButton = None
addButton = None
removeButton = None
combatButtons = []
canvas = None
tip = None

playerMove = None
enemyMove = None

def pokemonNameToID(name):
	global pokemen

	for i in pokemen:
		if i.name == name: return i.id

def getPokemonByID(id, getCopy=False):
	global pokemen

	for i in pokemen:
		if i.id == id:
			if getCopy: return copy.deepcopy(i)
			else: return i

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

		if (p == None):
			continue

		if (int(singleStat[1]) == 1): p.maxHealth = int(singleStat[2])
		if (int(singleStat[1]) == 2): p.attack = int(singleStat[2])
		if (int(singleStat[1]) == 3): p.defense = int(singleStat[2])
		if (int(singleStat[1]) == 4): p.speed = int(singleStat[2])
		p.health = p.maxHealth
		p.createMoves()

def sendStartData():
	global partyList
	global playerName

	data = {}
	data["mType"] = "start"
	data["playerName"] = playerName
	for i in range(0, 3):
		data[i] = pokemonNameToID(partyList.get(i))

	print("Sending player data")
	send(data)

def process(p):
	global playerNumber
	global enemyNumber

	data = pickle.loads(p)

	if (data["mType"] == "init"):
		playerNumber = data["playerNumber"]

	if (data["mType"] == "start"):
		if (data["players"][0] == playerNumber):
			enemyNumber = data["players"][1]
		elif (data["players"][1] == playerNumber):
			enemyNumber = data["players"][0]
		else:
			return

		print("A match was found")
		sendStartData()

	if ("playerNumber" in data):
		if (data["playerNumber"] != enemyNumber):
			print("Info was ignored")
			return\

	if (data["mType"] == "move"):
		global enemyMove
		enemyMove = data
		resolveMoves()


	if (data["mType"] == "playerData"):
		print("Got enemy data: " + str(data))

		global enemyParty
		global party
		global partyList
		global currentEnemyMember
		global currentMember
		global enemyName

		currentMember = 0
		currentEnemyMember = 0

		enemyName = data["playerName"]

		enemyParty = []
		enemyParty.append(getPokemonByID(data[0], True))
		enemyParty.append(getPokemonByID(data[1], True))
		enemyParty.append(getPokemonByID(data[2], True))

		party = []
		party.append(getPokemonByID(pokemonNameToID(partyList.get(0)), True))
		party.append(getPokemonByID(pokemonNameToID(partyList.get(1)), True))
		party.append(getPokemonByID(pokemonNameToID(partyList.get(2)), True))

		startBattle()

def resolveMoves():
	global playerMove
	global enemyMove
	global party
	global enemyParty
	global currentMember
	global currentEnemyMember

	if not playerMove or not enemyMove:
		return

	p1 = party[currentMember]
	p2 = enemyParty[currentEnemyMember]

	if (p1.speed > p2.speed):
		if (playerMove["choice"] >= 0 and playerMove["choice"] <= 2):
			logInfo(playerName + " swaped his " + party[currentMember].name + " for his " + party[playerMove["choice"]].name)
			currentMember = playerMove["choice"]

		if (enemyMove["choice"] >= 0 and enemyMove["choice"] <= 2):
			logInfo(enemyName + " swaped his " + enemyParty[currentEnemyMember].name + " for his " + enemyParty[enemyMove["choice"]].name)
			currentEnemyMember = enemyMove["choice"]


		if (p1.speed < p2.speed):
			if (enemyMove["choice"] >= 0 and enemyMove["choice"] <= 2):
				logInfo(enemyName + " swaped his " + enemyParty[currentEnemyMember].name + " for his " + enemyParty[enemyMove["choice"]].name)
				currentEnemyMember = enemyMove["choice"]

		if (playerMove["choice"] >= 0 and playerMove["choice"] <= 2):
			logInfo(playerName + " swaped his " + party[currentMember].name + " for his " + party[playerMove["choice"]].name)
			currentMember = playerMove["choice"]


	draw()

def logInfo(s):
	global log
	log.insert(END, s)


def startBattle():
	global playing
	playing = True

	global addButton
	global removeButton
	global partyList
	global pokemonList
	global tip

	addButton.grid_forget()
	removeButton.grid_forget()
	partyList.grid_forget()
	pokemonList.grid_forget()

	tip.grid(row=1, column=10, rowspan=10, sticky="N")

	for b in combatButtons:
		b.config(state=NORMAL)

	draw()

def draw():
	global canvas
	global currentEnemyMember
	global currentMember
	global party
	global enemyParty
	global enemyName
	
	print("draw" + str(currentMember))

	p1 = party[currentMember]
	p2 = enemyParty[currentEnemyMember]

	print(p1.name)
	print(p2.name)

	canvas.delete("all")

	width = 200
	height = 275

	drawRect(5, 5, 100 * p1.health / p1.maxHealth, 5, "green", "black")
	canvas.create_text(60, 20, text=playerName + "'s " + p1.name)

	drawRect(width - 100 - 5, height - 10 - 5, 100 * p2.health / p2.maxHealth, 5, "green", "black")
	canvas.create_text(width - 80, height - 25, text=enemyName + "'s " + p2.name)

def drawRect(x, y, width, height, fill, outline):
	global canvas

	canvas.create_rectangle(x, y, x + width, y + height, fill=fill, outline=outline)

def exit():
	global root
	root.destroy()

def connect():
	global partyList

	if (partyList.get(2) == ""):
		messagebox.showwarning("Be careful", "You must have 3 pokemen in your party")
		return

	setupSocket()

	global connectButton


def choose(n):
	global combatButtons
	global party
	global currentMember
	global playerMove

	for i in combatButtons:
		i.config(state=DISABLED)

	data = {}
	data["mType"] = "move"
	data["choice"] = n

	data["fail"] = False

	if (n == 4): data["fail"] = random.randint(0, 100) > party[currentMember].stunChance
	if (n == 6): data["fail"] = random.randint(0, 100) > party[currentMember].prepareChance

	playerMove = data
	resolveMoves()

	send(data)


def addPokemon():
	global pokemonList
	global partyList

	if (partyList.get(2) != "" or pokemonList.curselection() == ()): return
	partyList.insert(END, pokemonList.get(pokemonList.curselection()))

	getPokemonByID(pokemonNameToID(pokemonList.get(pokemonList.curselection()))).createMoves()

def removePokemon():
	global pokemonList
	global partyList

	if (partyList.curselection() == ()): return

	partyList.delete(partyList.curselection())

def giveTip(label):
	global tip
	global enemyParty
	global party
	global currentEnemyMember
	global playing

	if not playing: return

	p = party[currentEnemyMember]

	text = ""

	if (label == "swap1"): text = "Swap for " + party[0].name
	if (label == "swap2"): text = "Swap for " + party[1].name
	if (label == "swap3"): text = "Swap for " + party[2].name

	if (label == "attack"): text = "Attack for " + str(p.attack) + " damage"
	if (label == "stun"): text = "Attempt (" + str(p.stunChance) + "% chance)\nfor " + str(int(p.stunTime)) + " turns\n(They will also be attacked)"
	if (label == "debuff"): text = "Debuff enemy attack by " + str(p.debuffAttackAmount) + "\nand defense by " + str(p.debuffDefenceAmount) + "\nfor " + str(p.debuffTime) + " turns (This will prevent swapping)"
	if (label == "prepare"): text = "Skip attacking to prepare\n(" + str(p.prepareChance) + "% chance) to reflect\n" + str(p.prepareAmount) + "% damage\n(You will still take this damage)"

	tip.config(state=NORMAL)
	tip.delete(1.0, END)
	tip.insert(END, text)
	tip.config(state=DISABLED)

def initScreen():
	global root
	global pokemonList
	global partyList
	global pokemen
	global canvas
	global connectButton
	global combatButtons
	global tip
	global log
	global addButton
	global removeButton

	root = Tk()
	root.geometry("720x415")
	root.title("Pokemen")
	root.update()

	exitButton = Button(text="Quit", command=exit)
	exitButton.grid(row=1, column=1, sticky="NW")

	connectButton = Button(text="Connect", command=connect)
	connectButton.grid(row=1, column=1, sticky="NE")

	log = Listbox(height=10, width=80)
	log.grid(row=6, column=7, columnspan=40, rowspan=5, sticky="W")

	canvas = Canvas(width=200, height=275)
	canvas.create_rectangle(0, 0, 1000, 1000, fill="blue")
	canvas.grid(row=2, column=1, columnspan=2, rowspan=5, sticky="N")

	b1 = Button(text = "Swap for 1", command = lambda: choose(0), width=10)
	b1.bind("<Enter>", lambda x: giveTip(copy.deepcopy("swap1")))
	b1.grid(row=7, column=1, sticky="SW")

	b2 = Button(text = "Swap for 2", command = lambda: choose(1), width=10)
	b2.bind("<Enter>", lambda x: giveTip(copy.deepcopy("swap2")))
	b2.grid(row=7, column=2, sticky="SW")

	b3 = Button(text = "Swap for 3", command = lambda: choose(2), width=10)
	b3.bind("<Enter>", lambda x: giveTip(copy.deepcopy("swap3")))
	b3.grid(row=8, column=1, sticky="NW")


	b4 = Button(text = "Attack", command = lambda: choose(3), width=10)
	b4.bind("<Enter>", lambda x: giveTip(copy.deepcopy("attack")))
	b4.grid(row=9, column=1, sticky="SW")

	b5 = Button(text = "Stun", command = lambda: choose(4), width=10)
	b5.bind("<Enter>", lambda x: giveTip(copy.deepcopy("stun")))
	b5.grid(row=9, column=2, sticky="SW")

	b6 = Button(text = "Debuff", command = lambda: choose(5), width=10)
	b6.bind("<Enter>", lambda x: giveTip(copy.deepcopy("debuff")))
	b6.grid(row=10, column=2, sticky="NW")

	b7 = Button(text = "Prepare", command = lambda: choose(6), width=10)
	b7.bind("<Enter>", lambda x: giveTip(copy.deepcopy("prepare")))
	b7.grid(row=10, column=1, sticky="NW")

	combatButtons = [b1, b2, b3, b4, b5, b6, b7]

	for b in combatButtons:
		b.config(state=DISABLED)

	pokemonList = Listbox(width=20, height=15)
	for i in pokemen:
		pokemonList.insert(END, i.name)

	pokemonList.grid(row=1, column=7, rowspan=5, sticky="N")

	addButton = Button(text = "->", command = addPokemon, width=2)
	addButton.grid(row=1, column=8, sticky="N")

	removeButton = Button(text = "<-", command = removePokemon, width=2)
	removeButton.grid(row=2, column=8, sticky="N")						

	partyList = Listbox(width=20, height=3)
	partyList.grid(row=1, column=9, rowspan=2, sticky="N")	 	

	tip = Text(width=30, height=15, state=DISABLED, font=("Arial", 10))
	tip.grid_forget()

	root.mainloop()

def setupSocket():
	global sock
	global playerName

	playerName = simpledialog.askstring("Name", "What is your username?")

	sock = socket.socket()
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.connect(("localhost", 50000))

	start_new_thread(listeningThread, ())

def listeningThread():
	global sock
	while (True):
		process(sock.recv(4096))

def send(p):
	global sock

	if playerNumber != None:
		p["playerNumber"] = playerNumber

	if sock != None:
		sock.send(pickle.dumps(p))

def main():
	global pokemen

	loadMonsterInfo()
	initScreen()

if (__name__ == "__main__"): main()