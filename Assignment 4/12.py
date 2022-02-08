#libraries used
import sys
import time
import random

#==============================================================================================#

global startTime				#Keeps track of start time
startTime = time.time()
random.seed(13)

#==============================================================================================#
#Ant Object Definition
class Ant(object):
	def __init__(self, cityDistances):
		self.tour = []								#Ant's tour		
		self.tourCost = float('Inf')				#Ant's tour cost


#==============================================================================================#
#Defining Generate Tour. Generates a tour for a given ant
def generateTour(ant, cityDistances, alpha, beta, pathPheromone):
	numOfCities = len(cityDistances)

	startCity = random.randint(0, numOfCities-1)				#Select a random start city
	notVisitedCities = [city for city in range(numOfCities)]	#Keeps track of cities not visited
	notVisitedCities.remove(startCity)
	ant.tour.append(startCity)
	ant.tourCost = 0

	while(len(ant.tour) != numOfCities):						#Finding cities untill we get a complete tour
		currentCity = ant.tour[-1]
		allProbabilities = []
		
		for nextCity in notVisitedCities:						#Finding propabilities of selecting a city
			allProbabilities.append(pathPheromone[currentCity][nextCity]**alpha * (1/cityDistances[currentCity][nextCity])**beta)
		
		sumProbabilities = sum(allProbabilities)
		weights = []
		
		for x in allProbabilities:
			weights.append(x / sumProbabilities)
																#Choosing a not visited city based on probability
		nextCity = random.choices(notVisitedCities, weights=weights)
		nextCity = nextCity[0]

		ant.tour.append(nextCity)								#Updating tour
		notVisitedCities.remove(nextCity)						#Updating list of not visited cities
		ant.tourCost += cityDistances[currentCity][nextCity]	#Updating tour cost

	currentCity = nextCity
	ant.tourCost += cityDistances[currentCity][startCity]		#Adding the cost from last city to start city


#==============================================================================================#
#Ant Colony Optimization
def ACO(cityDistances, alpha, beta, rho, Qvalue, numOfAnts):
	numOfCities = len(cityDistances)			#Keeps track of number of cities
	convergenceRate = int(0.1 * numOfCities)	#Convergence rate keeps track of how many best ants to consider
												#Keeps track of path peromones
	pathPheromone = [[Qvalue for _ in range(numOfCities)] for _ in range(numOfCities)]
	bestTour = []								#Best tour so far
	bestTourCost = float('Inf')					#Best tour cost

	global startTime							#Keeps track of start time

	while True:
		#print("Current time:", time.time() - startTime, "sec")
		ants = []								#List of all ants

		for _ in range(numOfAnts):				#Initializing all ants
			ant = Ant(cityDistances)
			generateTour(ant, cityDistances, alpha, beta, pathPheromone)	#Generating tour of ant
			ants.append(ant)

			if (ant.tourCost < bestTourCost):	#Finding best tour
				bestTour = ant.tour 
				bestTourCost = ant.tourCost

				print("\nBest Tour So Far: ")	#Printing best tour
				print(bestTour, sep=" ")
				print("Tour Cost: ", bestTourCost)
				print("Time Taken:", time.time() - startTime, "sec")

												#Keeps track of pheromone delta 
		deltaPheromones = [[0 for _ in range(numOfCities)] for _ in range(numOfCities)]

		ants.sort(key=lambda x: x.tourCost)		#Sorting all choosing best ants
		ants = ants[ :convergenceRate]

		for ant in ants:
			for i, u in enumerate(ant.tour):
				v = ant.tour[(i+1) % numOfCities]
				deltaPheromones[u][v] += Qvalue / ant.tourCost

		for i in range(numOfCities):			#Updating Pheromone content on all paths
			for j in range(numOfCities):
				pathPheromone[i][j] = (1 - rho) * pathPheromone[i][j] + deltaPheromones[i][j]

		if time.time() - startTime > 299:		#If time exceeds exit the function
			exit()


#==============================================================================================#
#main
#Total arguments
n = len(sys.argv)
if(n != 2):
    print("Usage: python3 <code>.py <inputfile>")
    sys.exit()

try:									#Opening file
    inFile = open(sys.argv[1], "r")
except IOError:
    print("File not found")
    sys.exit()

data = inFile.readlines()
inFile.close()
distType = data[0].strip("\n")
numOfCities = int(data[1])

cityCoords = []
cityDistances = []

for i in range(numOfCities):			#Reading city coordinates
	coords = list(map(float, data[i+2].split()))
	cityCoords.append(coords)

for i in range(numOfCities):			#Reading city distances
	dist = list(map(float, data[i+numOfCities+2].split()))
	cityDistances.append(dist)

										#Running ACO
if numOfCities <= 100:
	ACO(cityDistances, alpha=10, beta=10, rho=0.1, Qvalue=0.1, numOfAnts=numOfCities)
else:
	ACO(cityDistances, alpha=10, beta=10, rho=0.5, Qvalue=0.5, numOfAnts=numOfCities)

#==============================================================================================#