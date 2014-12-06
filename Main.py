from Monster import *
from tkinter import *
from _thread import *
import tkinter.simpledialog as simpledialog
import socket
import pickle

pokemen = []

root = None
pokemonList = None
partyList = None

sock = None

playerInfo = None
enemyName = None

playerNumber = None
enemyNumber = None

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
		if (int(singleStat[1]) == 4): p.speed = int(singleStat[2])

def sendStartData():
	pass
	#send("startData:" + )

def process(p):
	print(p)
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

		sendStartData()

def exit():
	global root
	root.destroy()

def connect():
	setupSocket()

def swap(n):
	send("Swapping for " + str(n))


def initScreen():
	global root
	global pokemonList
	global partyList
	global pokemen

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
	canvas.grid(row=1, column=3, rowspan=5, sticky="N")

	Button(text = "Swap for 1", command = lambda: swap(0), width=10).grid(row=1, column=4, sticky="N")
	Button(text = "Swap for 2", command = lambda: swap(1), width=10).grid(row=1, column=5, sticky="N")
	Button(text = "Swap for 3", command = lambda: swap(2), width=10).grid(row=2, column=4, sticky="N")

	Button(text = "Attack 1", command = lambda: swap(0), width=10).grid(row=3, column=4, sticky="SW")
	Button(text = "Attack 2", command = lambda: swap(1), width=10).grid(row=3, column=5, sticky="SW")
	Button(text = "Attack 3", command = lambda: swap(2), width=10).grid(row=4, column=4, sticky="NW")
	Button(text = "Attack 4", command = lambda: swap(4), width=10).grid(row=4, column=5, sticky="NW")

	pokemonList = Listbox(width=10)
	for i in pokemen:
		pokemonList.insert(END, i.name)

	pokemonList.grid(row=1, column=7, rowspan=100, sticky="N")

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
		process(sock.recv(1024))

def send(p):
	global sock
	if sock != None:
		sock.send(pickle.dumps(p))

def main():
	global pokemen

	loadMonsterInfo()
	initScreen()

if (__name__ == "__main__"): main()