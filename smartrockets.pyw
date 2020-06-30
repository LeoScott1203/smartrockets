import os
import time
import random
import math
from tkinter import *

random.seed(time.time())

class rocket:
	startX = 250
	startY = 490

	height = 20
	width = 5

	upForce = -5

	def __init__(self, c, dna):
		self.stuck = False
		self.hit_target = False;

		self.dna = dna

		self.sideForce = 270
		self.fitness = 0

		self.x0 = rocket.startX
		self.y0 = rocket.startY
		self.x1 = rocket.startX
		self.y1 = self.y0 + rocket.height

		self.visual = c.create_line(self.x0, self.y0, self.x1, self.y1, width = rocket.width, fill="white")

	def draw(self, c, current):
		self.sideForce += self.dna[current]
		self.radAngle = (self.sideForce * math.pi) / 180

		self.x0 = self.x0 + rocket.upForce * -math.cos(self.radAngle)
		self.y0 = self.y0 + rocket.upForce * -math.sin(self.radAngle)
		self.x1 = self.x0 + rocket.height * math.cos(self.radAngle)
		self.y1 = self.y0 + rocket.height * math.sin(self.radAngle)

		self.visual = c.create_line(self.x0, self.y0, self.x1, self.y1, width = rocket.width, fill = "white")

		#test if hit
		#side of screen
		if self.x1 > 500 or self.x1 < 0:
			self.stuck = True
		if self.y1 > 500 or self.y1 < 0:
			self.stuck = True
		#obstacles
		if self.x1 > 150 and self.x1 < 350 and self.y1 > 240 and self.y1 < 250:
			self.stuck = True
		if self.x1 > 50 and self.x1 < 150 and self.y1 > 140 and self.y1 < 150:
			self.stuck = True
		if self.x1 > 350 and self.x1 < 450 and self.y1 > 140 and self.y1 < 150:
			self.stuck = True
		if self.x1 > 50 and self.x1 < 150 and self.y1 > 350 and self.y1 < 360:
			self.stuck = True
		if self.x1 > 350 and self.x1 < 450 and self.y1 > 350 and self.y1 < 360:
			self.stuck = True
		#goal
		if self.x1 > endPoint[0] - 10 and self.x1 < endPoint[0] + 10 and self.y1 > endPoint[1] - 10 and self.y1 < endPoint[1] + 10:
			self.stuck = True
			self.hit_target = True

	def calcFit(self):
		self.fitness = math.sqrt((self.startX - self.x1) ** 2 + (self.startY - self.y1) ** 2)
		self.fitness = self.fitness - (math.sqrt((endPoint[0] - self.x1) ** 2 + (endPoint[1] - self.y1) ** 2))
		self.fitness = math.floor(self.fitness)

		if (self.fitness <= 0):
			self.fitness = 1

		if (self.hit_target):
			self.fitness = 1000

		return self.fitness ** 2

	def reset(self, c, dna):
		self.stuck = False
		self.hit_target = False

		self.dna = dna

		self.sideForce = 270
		self.fitness = 0

		c.delete(self.visual)

		self.x0 = rocket.startX
		self.y0 = rocket.startY
		self.x1 = rocket.startX
		self.y1 = self.y0 + rocket.height

rockets = []
genePool = []

popSize = 20
lifespan = 550
generationCounter = 1

endPoint = (250, 50)

root = Tk()
root.title('smart rockets')
root.resizable(False, False)
	
canvas = Canvas(root, height = 500, width = 500, bg = 'black')
generationText = canvas.create_text(10, 10, anchor = 'nw', fill = 'white', font = 20)

canvas.itemconfig(generationText, text = "generation 1")

visualEND = canvas.create_rectangle(endPoint[0] - 10, endPoint[1] - 10, endPoint[0] + 10, endPoint[1] + 10, fill = "green")

visualObstacle = canvas.create_rectangle(150, 250, 350, 240, fill = "white")
visualObstacle2 = canvas.create_rectangle(50, 150, 150, 140, fill = "white")
visualObstacle3 = canvas.create_rectangle(350, 150, 450, 140, fill = "white")
visualObstacle4 = canvas.create_rectangle(50, 360, 150, 350, fill = "white")
visualObstacle5 = canvas.create_rectangle(350, 360, 450, 350, fill = "white")

for i in range(popSize):
	newDNA = []

	for j in range(lifespan):
		newDNA.append(random.uniform(-10, 10))

	newRocket = rocket(canvas, newDNA)
	rockets.append(newRocket)

while 1:
	#run through simulation
	for i in range(lifespan):
		all_stuck = True

		for j in range(popSize):
			if rockets[j].stuck == False:
				canvas.delete(rockets[j].visual)
				rockets[j].draw(canvas, i)

				canvas.pack()
				root.update_idletasks()
				root.update()

				all_stuck = False

		if (all_stuck == False):
			time.sleep(0.01)

	time.sleep(1)

	#calc fitness
	for i in range(popSize):
		for j in range(rockets[i].calcFit()):
			genePool.append(rockets[i].dna)

	#create new population
	for i in range(popSize):
		randDNA = []

		parent1 = random.choice(genePool)
		parent2 = random.choice(genePool)

		while parent1 == parent2:
			parent2 = random.choice(genePool)

		for j in range(lifespan):
			parents = [parent1[j], parent2[j]]
			_ = random.choice(parents)
			randDNA.append(_)

		#mutate
		if random.randint(0, 2) == 0:
			for j in range(math.floor(lifespan / 20)):
				randIndex = random.randint(0, lifespan - 1)
				randDNA.pop(randIndex)
				randDNA.insert(randIndex, random.uniform(-10, 10))

		newDNA = randDNA
		rockets[i].reset(canvas, newDNA)

	genePool.clear()
	generationCounter = generationCounter + 1
	canvas.itemconfig(generationText, text = ("generation " + str(generationCounter)))