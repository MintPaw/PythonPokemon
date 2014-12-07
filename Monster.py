import random

class Pokemon:
	def __init__(self, ):
		self.stunTime = 0;
		self.stunChance = 0;
		self.debuffAttackAmount = 0;
		self.debuffDefenceAmount = 0;
		self.debuffTime = 0;
		self.prepareChance = 0;
		self.prepareAmount = 0;

		self.id = 0;
		self.name = "";
		self.health = 0;
		self.maxHelath = 0;
		self.attack = 0;
		self.defense = 0;
		self.speed = 0;

	def createMoves(self, ):
		random.seed(self.name)

		points = 600 - (self.health + self.attack + self.defense + self.speed)

		for i in range(0, points // 15):
			placeAt = random.randint(0, 7)

			if placeAt == 1: self.stunTime += .2
			elif placeAt == 2: self.stunChance += 1.5
			elif placeAt == 3: self.debuffAttackAmount += .5
			elif placeAt == 4: self.debuffDefenceAmount += .5
			elif placeAt == 5: self.debuffTime += .2
			elif placeAt == 6: self.prepareChance += 1.5
			elif placeAt == 7: self.prepareAmount += 1.5

		self.stunTime = int(self.stunTime)
		self.stunChance = int(self.stunChance)
		self.debuffAttackAmount = int(self.debuffAttackAmount)
		self.debuffDefenceAmount = int(self.debuffDefenceAmount)
		self.debuffTime = int(self.debuffTime)
		self.prepareChance = int(self.prepareChance)
		self.prepareAmount = int(self.prepareAmount)