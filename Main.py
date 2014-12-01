from Monster import *
import Tkinter as Tk
import tkSimpleDialog
import socket

pokemen = []
root = None
sock = None

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

def exit():
	print("Exit")

def connect():
	setupSocket()

def send(s):
	global sock
	if sock != None:
		sock.send(s)

def swap1():
	send("Swapping for 1")


def initScreen():
	global root
	width = 720
	height = 402

	root = Tk.Tk()
	root.geometry(str(width) + "x" + str(height) + "+300+300")
	root.title("Pokemen")
	root.update()

	exitButton = Tk.Button(text="Quit", command=exit)
	exitButton.grid(row=1, column=1, sticky="W")

	connectButton = Tk.Button(text="Connect", command=connect)
	connectButton.grid(row=1, column=2)

	log = Tk.Listbox(height=15)
	log.grid(row=2, column=1, columnspan=2)

	canvas = Tk.Canvas(width=300, height=275)
	canvas.create_rectangle(0, 0, 1000, 1000, fill="blue")
	canvas.grid(row=1, column=3, rowspan=3, sticky="N")

	swaps = []
	for i in range(0, 3):
		s = Tk.Button(text = "Swap for " + str(i), command=swap1)
		s.grid(row = i + 3, column = 4)

	root.mainloop()

def setupSocket():
	global sock

	name = tkSimpleDialog.askstring("Name", "What is your username?")

	sock = socket.socket()
	sock.connect(("", 50000))
	print(sock.recv(1024))
	sock.send("Name:" + name)


def main():
	global pokemen

	loadMonsterInfo()
	initScreen()


if (__name__ == "__main__"): main()