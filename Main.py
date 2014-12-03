from Monster import *
from tkinter import *
from _thread import *
import tkinter.simpledialog as simpledialog
import socket

pokemen = []
root = None
sock = None
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

def process(s):
	global playerNumber

	print(s)

	command = s.split(":")

	if (command[0] == "playerNumber"): playerNumber = int(command[1])

def exit():
	print("Exit")

def connect():
	setupSocket()

def send(s):
	global sock
	if sock != None:
		sock.send(s.encode("utf-8"))

def swap(n):
	send("Swapping for " + str(n))


def initScreen():
	global root
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
	log.grid(row=2, column=1, columnspan=2)

	canvas = Canvas(width=300, height=275)
	canvas.create_rectangle(0, 0, 1000, 1000, fill="blue")
	canvas.grid(row=1, column=3, rowspan=3, sticky="N")

	swaps = []
	for i in range(0, 3):
		print(i)
		if (i == 0): s = Button(text = "Swap for " + str(i), command = lambda: swap(0))
		if (i == 1): s = Button(text = "Swap for " + str(i), command = lambda: swap(1))
		if (i == 2): s = Button(text = "Swap for " + str(i), command = lambda: swap(2))
		s.grid(row = i + 3, column = 4)

	root.mainloop()

def setupSocket():
	global sock

	name = simpledialog.askstring("Name", "What is your username?")

	sock = socket.socket()
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.connect(("localhost", 50000))

	start_new_thread(listeningThread, ())

def listeningThread():
	while (True):
		process(sock.recv(1024).decode("utf-8"))

def main():
	global pokemen

	loadMonsterInfo()
	initScreen()

if (__name__ == "__main__"): main()