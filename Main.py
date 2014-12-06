from Monster import *
from tkinter import *
from _thread import *
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import socket
import pickle
import copy

pokemen = []

root = None
pokemonList = None
partyList = None

sock = None

playerInfo = None
enemyName = None

playerNumber = None
enemyNumber = None

party = None
enemyParty = None

currentMember = None
currentEnemyMember = None

connectButton = None

canvas = None

def pokemonNameToID(name):
	global pokemen

	for i in pokemen:
		if i.name == name: return i.id

def getPokemonByID(id):
	global pokemen

	for i in pokemen:
		if i.id == id: return copy.deepcopy(i)

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
		p.maxHealth = p.health

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

	print(data)

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
		enemyParty.append(getPokemonByID(data[0]))
		enemyParty.append(getPokemonByID(data[1]))
		enemyParty.append(getPokemonByID(data[2]))

		party = []
		party.append(getPokemonByID(pokemonNameToID(partyList.get(0))))
		party.append(getPokemonByID(pokemonNameToID(partyList.get(1))))
		party.append(getPokemonByID(pokemonNameToID(partyList.get(2))))

		startBattle()

	if ("playerName" in data):
		if (data["playerName"] != enemyName):
			print("Info was ignored")
			return												 	

def startBattle():
	draw()

def draw():
	global canvas
	global currentEnemyMember
	global currentMember
	global party
	global enemyParty
	global enemyName

	p1 = party[currentMember]
	p2 = enemyParty[currentEnemyMember]

	canvas.delete("all")

	width = 200
	height = 275

	drawRect(5, 5, 100, 5, "green", "black")
	canvas.create_text(60, 20, text=playerName + "'s " + p1.name)

	drawRect(width - 100 - 5, height - 10 - 5, 100, 5, "green", "black")

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
	connectButton.config(state=DISABLED)


def swap(n):
	send("Swapping for " + str(n))

def addPokemon():
	global pokemonList
	global partyList

	if (partyList.get(2) != "" or pokemonList.curselection() == ()): return
	partyList.insert(END, pokemonList.get(pokemonList.curselection()))

def removePokemon():
	global pokemonList
	global partyList

	if (partyList.curselection() == ()): return

	partyList.delete(partyList.curselection())


def initScreen():
	global root
	global pokemonList
	global partyList
	global pokemen
	global canvas
	global connectButton

	width = 720
	height = 402

	root = Tk()
	root.geometry(str(width) + "x" + str(height) + "+300+300")
	root.title("Pokemen")
	root.update()

	exitButton = Button(text="Quit", command=exit)
	exitButton.grid(row=1, column=1, sticky="W")

	connectButton = Button(text="Connect", command=connect)
	connectButton.grid(row=1, column=2)

	log = Listbox(height=15)
	log.grid(row=2, column=1, columnspan=2, rowspan=5)

	canvas = Canvas(width=200, height=275)
	canvas.create_rectangle(0, 0, 1000, 1000, fill="blue")
	canvas.grid(row=1, column=3, columnspan=2, rowspan=5, sticky="N")

	Button(text = "Swap for 1", command = lambda: swap(0), width=10).grid(row=6, column=3, sticky="W")
	Button(text = "Swap for 2", command = lambda: swap(1), width=10).grid(row=6, column=4, sticky="W")
	Button(text = "Swap for 3", command = lambda: swap(2), width=10).grid(row=7, column=3, sticky="W")

	Button(text = "Attack 1", command = lambda: swap(0), width=10).grid(row=8, column=3, sticky="SW")
	Button(text = "Attack 2", command = lambda: swap(1), width=10).grid(row=8, column=4, sticky="SW")
	Button(text = "Attack 3", command = lambda: swap(2), width=10).grid(row=9, column=4, sticky="NW")
	Button(text = "Attack 4", command = lambda: swap(4), width=10).grid(row=9, column=3, sticky="NW")

	pokemonList = Listbox(width=20, height=15)
	for i in pokemen:
		pokemonList.insert(END, i.name)

	pokemonList.grid(row=1, column=7, rowspan=100, sticky="N")

	Button(text = "->", command = addPokemon, width=2).grid(row=1, column=8, sticky="N")
	Button(text = "<-", command = removePokemon, width=2).grid(row=2, column=8, sticky="N")

	partyList = Listbox(width=20, height=3)
	partyList.grid(row=1, column=9, sticky="N")

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
	if playerNumber != None: p["playerNumber"] = playerNumber
	if sock != None:
		sock.send(pickle.dumps(p))

def main():
	global pokemen

	loadMonsterInfo()
	initScreen()

if (__name__ == "__main__"): main()