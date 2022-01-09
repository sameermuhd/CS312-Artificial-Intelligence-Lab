#libraries used
import sys
import copy
from numpy import random
from heapq import heappop, heappush, heapify, nlargest, nsmallest
import numpy as np
from pprint import pprint

#==============================================================================================#
#State Class
class state():
	def __init__(self):
		self.stateVariables = {}				#Stores the truth values of literals
		self.hValue = 0							#Heuristic Value of the state

	def __hash__(self):							#Overriding __hash__ to ensure heaps work
	    return hash(tuple(self.stateVariables.items()))

	def __lt__(self, other):					#Overriding __lt__ to ensure heaps work
		return self.hValue > other.hValue

	def __eq__(self, other):					#Overriding __eq__ to ensure heaps work
		if hash(self) == hash(other):
			return True
		else:
			return False

	def printState(self):						#Method to print a state
		print(self.stateVariables)
		print("Heuristic Value: " + str(self.hValue))

#==============================================================================================#
#initialState Function to generate a random initial state
def initialState(clauses, numOfVaribles):
	initState = state()
	for i in range(numOfVaribles):
		assign = random.choice([0, 1])
		initState.stateVariables[chr(i + 1 + ord('@'))] = assign
		initState.stateVariables[chr(i + 1 + ord('`'))] = 1 - assign

	heuristic(clauses, initState)
	return initState

#==============================================================================================#
#Heuristic Function (+1 if a clause is satisfied)
def heuristic(clauses, state):
	count = 0
	for clause in clauses:
		value = [state.stateVariables[i] for i in clause]
		count += int(any(value))
	
	state.hValue = count
	return

#==============================================================================================#
#moveGen (Generates all possible neighbours of a state while varying 'k' bits)
#Argument 'k' indicates the number of bits to flip
#We iterates from 0 to 2^{numOfLiterals} - 1 in binary string format
#In the above string, 1s postion represent bits to be flipped
def moveGen(clauses, state, k):
	neighbours = []
	global numOfVaribles
	for i in range(2 ** numOfVaribles):
		string = np.binary_repr(i, width = numOfVaribles)
		numOfOnes = string.count("1")
		if(numOfOnes == k):
			neighbour = copy.deepcopy(state)
			for ind, x in enumerate(string):
				if x == "1":					#Swapping the bits
					assign = neighbour.stateVariables[chr(ind + 1 + ord('@'))]
					neighbour.stateVariables[chr(ind + 1 + ord('@'))] = 1 - assign
					neighbour.stateVariables[chr(ind + 1 + ord('`'))] = assign
			heuristic(clauses, neighbour)
			neighbours.append(neighbour)
	return neighbours

#==============================================================================================#
#goalTest (returns True if all states are satisfied, else returns False)
def goalTest(state):
	global numOfClauses
	if state.hValue == numOfClauses:
		return True
	else:
		return False

#==============================================================================================#
#Hill Climbing (function internally used by Variable Neighbour Descent)
def HC(clauses, initialState, k):
	global numOfStatesExplored
	current = initialState
	explored = set()
	explored.add(current)

	while True:
		frontierHeap = []
		heapify(frontierHeap)
		stateNeighbours = moveGen(clauses, current, k)
		for neighbour in stateNeighbours:
			if neighbour not in explored:
				heappush(frontierHeap, neighbour)
		heapify(frontierHeap)
		if len(frontierHeap) == 0:
			numOfStatesExplored += len(explored)
			return current
		neighbour = heappop(frontierHeap)
		if(neighbour.hValue <= current.hValue):
			numOfStatesExplored += len(explored)
			return current
		current = neighbour
		explored.add(current)

	return False

#==============================================================================================#
#VND (Variable Neighbour Descent)
def VND(clauses, initialState):
	print("******** VND Stared ********")
	k = 1										#'k' indicates the number of bits to flip
	solFound = False
	global numOfVaribles
	global numOfStatesExplored
	while k <= numOfVaribles:
		#print("K Value: ", end="")
		#print(k)
		resultState = HC(clauses, initialState, k)

		if goalTest(resultState):
			solFound = True
			break
		k += 1 

	print("Final State: ")
	if solFound:
		resultState.printState()
		print("Number Of States Explored: ", end="")
		print(numOfStatesExplored)
	else:
		print("Solution Not Found")

#==============================================================================================#
#Tabu Search
def TabuSearch(clauses, numOfVaribles, tabuTenurett, initialState):
	print("\nTabu Tenure:", tabuTenurett)
	bestState = initialState
	nextBest = initialState
	maxIterations = 2**numOfVaribles			#Upper limit on number of iterations
	numOfItr = 0
	tabuTenure = {}
	for i in range(numOfVaribles):				#Initializing tabu tenures to 0
		tabuTenure[chr(i + 1 + ord('@'))] = 0
	if tabuTenurett >= numOfVaribles:
		print("Tabu Tenure can't exceed number of variables")
		return
	while (not goalTest(bestState)) and (numOfItr < maxIterations):
		numOfItr += 1
		stateNeighbours = moveGen(clauses, nextBest, 1)
		nextBest = []
		tabuElement = ""
		for i in range(numOfVaribles):
			if (tabuTenure[chr(i + 1 + ord('@'))] == 0):
				if (not nextBest) or (stateNeighbours[i].hValue > nextBest.hValue):
					nextBest = stateNeighbours[i]
					tabuElement = chr(i + 1 + ord('@'))
			else:
				tabuTenure[chr(i + 1 + ord('@'))] = tabuTenure[chr(i + 1 + ord('@'))] - 1
		tabuTenure[tabuElement] = tabuTenurett
		if nextBest.hValue > bestState.hValue:
			bestState = nextBest
	if numOfItr >= maxIterations:
		print("\nMax Iterations Exceeded")
	else:
		print("Final State: ")
		bestState.printState()
	print("Number Of States Explored:", numOfItr+1)


#==============================================================================================#
#Beam Search
def BeamSearch(clauses, initialState, beamWidth):
	print("\nBeam Width:", beamWidth)
	global numOfStatesExplored
	bestState = initialState
	frontier = []
	frontier.append(initialState)
	explored = set()

	while frontier:
		numOfStatesExplored += len(frontier)

		for state in frontier:
			isBreak = False
			if goalTest(state):
				bestState = state
				isBreak = True
				break

		if isBreak:
			break

		allNeighbours = []
		for state in frontier:
			explored.add(state)
			stateNeighbours = moveGen(clauses, state, 1)
			for neighbour in stateNeighbours:
				if (neighbour not in frontier) and (neighbour not in explored):
					allNeighbours.append(neighbour)

		heapify(allNeighbours)
		if len(allNeighbours) > beamWidth:	#Making sure the frontier has lenght <= beam width
			allNeighbours = copy.deepcopy(allNeighbours)
			heapify(allNeighbours)
			frontier = nsmallest(beamWidth, allNeighbours)
		else:
			frontier = copy.deepcopy(allNeighbours)


	print("Final State: ")
	bestState.printState()
	print("Number Of States Explored:", numOfStatesExplored)


#==============================================================================================#
#main
file = open("clauses.txt", "r")
sys.stdout = open("output.txt", "w")

clauses = []
setOfAllVariables = set()
for current in file:
    current = current.strip("\n)")
    current = current.strip("(")
    current = current.replace(",", "")
    current = current.replace("'", "")
    current = current.split()
    clauses.append(current)
    for x in current:
    	setOfAllVariables.add(x.upper())

global numOfStatesExplored
global numOfVaribles
global numOfClauses
numOfClauses = len(clauses)
numOfVaribles = ord(max(setOfAllVariables)) - ord('@')
numOfStatesExplored = 0
initState = initialState(clauses, numOfVaribles)
'''while initState.hValue != 5:
	initState = initialState(clauses, numOfVaribles)'''

print("Number of Variables:", numOfVaribles)
print("Number of Clauses:", numOfClauses)
print("\n---------Clauses---------")
pprint(clauses)
print()
print("------Initial State-------")
print(initState.stateVariables)
print("Heuristic Value: " + str(initState.hValue))

print("\n**********************************************************************************\n")
numOfStatesExplored = 0
VND(clauses, initState)

print("\n**********************************************************************************\n")
print("****** TabuSearch Stared ******")
for tabuTenure in range(numOfVaribles):
	numOfStatesExplored = 0
	TabuSearch(clauses, numOfVaribles, tabuTenure, initState)

print("\n**********************************************************************************\n") 
print("****** BeamSearch Stared ******")
for beamWidth in range(1, numOfVaribles + 1):
	numOfStatesExplored = 0
	BeamSearch(clauses, initState, beamWidth)
#==============================================================================================#