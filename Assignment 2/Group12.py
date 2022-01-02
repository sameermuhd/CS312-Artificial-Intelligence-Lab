#libraries used
import sys
import copy
from heapq import heappop, heappush, heapify
import time

start_time = time.time()

#==============================================================================================#
#Block Class Definition
class Block:
    def __init__(self):
        self.label = -1						#label of block {1, 2, 3...}
        self.stackNo = -1					#Stack in which block is present
        self.blockPos = -1					#Vertical Position of block in stack
        self.sittingOn = -1					#Label of block on which this block is sitting

    def printBlock(self):					#prinitng a block
    	print("Label: " + str(self.label) + " StackNo: " + str(self.stackNo) + " BlockNo: " + str(self.blockPos) + " SittingOn: " + str(self.sittingOn))


#==============================================================================================#
#Block World Definition
class BlockWorld:
    def __init__(self):
        self.stack1 = []					#Stacks in a block world state
        self.stack2 = []
        self.stack3 = []
        self.hValue = -1					#Heuristic Value of this state

    def __lt__(self, other):				#Overriding __lt__ to make max heap work
        return self.hValue > other.hValue

    def __eq__(self, other):				#Overriding __eq__ to make comparisions work
    	if goalTest(self, other):
    		return True
    	else:
    		return False
 
    def __hash__(self):						#Defining own hash to make set of this class work
        return hash((tuple([i.label for i in self.stack1]), tuple([i.label for i in self.stack2]), tuple([i.label for i in self.stack3])))

    def printBlockWorld(self):				#printing block world state
    	print("Stack1:")
    	for x in reversed(self.stack1):
    		x.printBlock()
    	print("Stack2:")
    	for x in reversed(self.stack2):
    		x.printBlock()
    	print("Stack3:")
    	for x in reversed(self.stack3):
    		x.printBlock()
    	print("hValue: " + str(self.hValue))

    def findBlock(self, label):				#Function used to find and return a block when label is given
    	for x in self.stack1:
    		if(x.label == label):
    			return x
    	for x in self.stack2:
    		if(x.label == label):
    			return x
    	for x in self.stack3:
    		if(x.label == label):
    			return x
    	return 


#==============================================================================================#
#Heuristic Function 1
def heuristic1(state, goalState):
	hValue = 0
	for block in state.stack1:
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.stackNo == goalBlock.stackNo):
			hValue += 1 
		if(block.blockPos == goalBlock.blockPos):
			hValue += 1
		if(block.sittingOn == goalBlock.sittingOn):
			hValue += 1

	for block in state.stack2:
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.stackNo == goalBlock.stackNo):
			hValue += 1 
		if(block.blockPos == goalBlock.blockPos):
			hValue += 1
		if(block.sittingOn == goalBlock.sittingOn):
			hValue += 1

	for block in state.stack3:
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.stackNo == goalBlock.stackNo):
			hValue += 1 
		if(block.blockPos == goalBlock.blockPos):
			hValue += 1
		if(block.sittingOn == goalBlock.sittingOn):
			hValue += 1

	state.hValue = hValue
	return

#==============================================================================================#
#Heuristic Function 2
def heuristic2(state, goalState):
	hValue = 0
	for block in state.stack1:
		label = block.label
		goalBlock = goalState.findBlock(label)
		hValue += -1 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))

	for block in state.stack2:
		label = block.label
		goalBlock = goalState.findBlock(label)
		hValue += -1 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))

	for block in state.stack3:
		label = block.label
		goalBlock = goalState.findBlock(label)
		hValue += -1 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))

	state.hValue = hValue
	return

#==============================================================================================#
#Heuristic Function 3
def heuristic3(state, goalState):
	hValue = 0
	for block in state.stack1:
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.sittingOn != goalBlock.sittingOn):
			hValue += -3 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))
		else:
			hValue += -2 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))

	for block in state.stack2:
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.sittingOn != goalBlock.sittingOn):
			hValue += -3 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))
		else:
			hValue += -2 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))

	for block in state.stack3:
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.sittingOn != goalBlock.sittingOn):
			hValue += -3 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))
		else:
			hValue += -2 * (abs(block.stackNo - goalBlock.stackNo) + abs(block.blockPos - goalBlock.blockPos))

	state.hValue = hValue
	return

#==============================================================================================#
#Goal Test
def goalTest(state, goalState):
	areSame = True

	for block in state.stack1:
		if not areSame:
			break
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.stackNo != goalBlock.stackNo):
			areSame = False
			break
		if(block.blockPos != goalBlock.blockPos):
			areSame = False
			break
		if(block.sittingOn != goalBlock.sittingOn):
			areSame = False
			break

	for block in state.stack2:
		if not areSame:
			break
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.stackNo != goalBlock.stackNo):
			areSame = False
			break
		if(block.blockPos != goalBlock.blockPos):
			areSame = False
			break
		if(block.sittingOn != goalBlock.sittingOn):
			areSame = False
			break

	for block in state.stack3:
		if not areSame:
			break
		label = block.label
		goalBlock = goalState.findBlock(label)
		if(block.stackNo != goalBlock.stackNo):
			areSame = False
			break
		if(block.blockPos != goalBlock.blockPos):
			areSame = False
			break
		if(block.sittingOn != goalBlock.sittingOn):
			areSame = False
			break

	return areSame


#==============================================================================================#
#funPopPush() Function used by moveGen internally to move top block from one stack to another
def funPopPush(fromStackNo, fromStack, toStackNo, toStack):
	topBlock = fromStack.pop()
	topBlock.stackNo = toStackNo
	toStacklen = len(toStack)

	if(toStacklen > 0):
			topBlock.blockPos = toStacklen
			topBlock.sittingOn = toStack[-1].label
	else:
		topBlock.blockPos = 0
		topBlock.sittingOn = -1

	toStack.append(topBlock)

#==============================================================================================#
#moveGen()
def moveGen(state, goalState, heuristic):
	neighbours = []
	if len(state.stack1) > 0:

		neighbour1 = copy.deepcopy(state)
		funPopPush(1, neighbour1.stack1, 2, neighbour1.stack2)	#Stack 1 to Stack 2

		neighbour2 = copy.deepcopy(state)
		funPopPush(1, neighbour2.stack1, 3, neighbour2.stack3)	#Stack 1 to Stack 3

		if(heuristic == 1):
			heuristic1(neighbour1, goalState)
			heuristic1(neighbour2, goalState)
		elif(heuristic == 2):
			heuristic2(neighbour1, goalState)
			heuristic2(neighbour2, goalState)
		elif(heuristic == 3):
			heuristic3(neighbour1, goalState)
			heuristic3(neighbour2, goalState)

		neighbours.append(neighbour1)
		neighbours.append(neighbour2)

	if len(state.stack2) > 0:

		neighbour3 = copy.deepcopy(state)
		funPopPush(2, neighbour3.stack2, 1, neighbour3.stack1)	#Stack 2 to Stack 1

		neighbour4 = copy.deepcopy(state)
		funPopPush(2, neighbour4.stack2, 3, neighbour4.stack3)	#Stack 2 to Stack 3

		if(heuristic == 1):
			heuristic1(neighbour3, goalState)
			heuristic1(neighbour4, goalState)
		elif(heuristic == 2):
			heuristic2(neighbour3, goalState)
			heuristic2(neighbour4, goalState)
		elif(heuristic == 3):
			heuristic3(neighbour3, goalState)
			heuristic3(neighbour4, goalState)

		neighbours.append(neighbour3)
		neighbours.append(neighbour4)

	if len(state.stack3) > 0:

		neighbour5 = copy.deepcopy(state)
		funPopPush(3, neighbour5.stack3, 1, neighbour5.stack1)	#Stack 3 to Stack 1

		neighbour6 = copy.deepcopy(state)
		funPopPush(3, neighbour6.stack3, 2, neighbour6.stack2)	#Stack 3 to Stack 2

		if(heuristic == 1):
			heuristic1(neighbour5, goalState)
			heuristic1(neighbour6, goalState)
		elif(heuristic == 2):
			heuristic2(neighbour5, goalState)
			heuristic2(neighbour6, goalState)
		elif(heuristic == 3):
			heuristic3(neighbour5, goalState)
			heuristic3(neighbour6, goalState)

		neighbours.append(neighbour5)
		neighbours.append(neighbour6)

	return neighbours


#==============================================================================================#
#Greedy Best First Search
def BFS(initialState, goalState, heuristic):
	global numOfStatesExplored
	frontierHeap = []
	heapify(frontierHeap)
	heappush(frontierHeap, initialState)
	explored = set()

	while frontierHeap:
		state = heappop(frontierHeap)
		explored.add(state)
		if goalTest(state, goalState):
			numOfStatesExplored = len(explored)
			return state

		stateNeighbours = moveGen(state, goalState, heuristic)

		for neighbour in stateNeighbours:
			if (neighbour not in frontierHeap) and (neighbour not in explored):
				heappush(frontierHeap, neighbour)
			elif (neighbour in frontierHeap):
				heapify(frontierHeap)

	return False

#==============================================================================================#
#Hill Climbing
def HC(initialState, goalState, heuristic):
	global numOfStatesExplored
	current = initialState
	explored = set()
	explored.add(current)

	while True:
		frontierHeap = []
		heapify(frontierHeap)
		stateNeighbours = moveGen(current, goalState, heuristic)
		for neighbour in stateNeighbours:
			if neighbour not in explored:
				heappush(frontierHeap, neighbour)
		heapify(frontierHeap)
		neighbour = heappop(frontierHeap)
		if(neighbour.hValue <= current.hValue):
			numOfStatesExplored = len(explored)
			return current
		current = neighbour
		explored.add(current)

	return False

#==============================================================================================#
#main

#Total arguments
n = len(sys.argv)
if(n != 5):
    print("Usage: python3 <code>.py <inputFile> <BFS/HC> <1/2/3> <outputFile>")
    sys.exit()

try:
    inputFile = open(sys.argv[1], "r")
    sys.stdout = open(sys.argv[4], "w")	#any print statement is written in outout file
except IOError:
    print("File not found")
    sys.exit()

algo = sys.argv[2]
heuristic = sys.argv[3]

if(algo not in ["BFS", "HC"]) or (heuristic not in ["1", "2", "3"]):
	print("Usage: python3 <code>.py <inputFile> <BFS/HC> <1/2/3> <outputFile>")
	sys.exit()

heuristic = int(heuristic)

initialState = []
goalState = []

#Reading input file
inputFile.readline()

line1 = inputFile.readline()
line1 = line1[1:-2]
if len(line1) > 1:
	line1 = line1.split(", ")
	line1 = list(map(int, line1))
elif len(line1) == 1:
	line1 = [int(line1)]
else:
	line1 = []
initialState.append(line1)

line2 = inputFile.readline()
line2 = line2[1:-2]
if len(line2) > 1:
	line2 = line2.split(", ")
	line2 = list(map(int, line2))
elif len(line2) == 1:
	line2 = [int(line2)]
else:
	line2 = []
initialState.append(line2)

line3 = inputFile.readline()
line3 = line3[1:-2]
if len(line3) > 1:
	line3 = line3.split(", ")
	line3 = list(map(int, line3))
elif len(line3) == 1:
	line3 = [int(line3)]
else:
	line3 = []
initialState.append(line3)

inputFile.readline()
inputFile.readline()

line4 = inputFile.readline()
line4 = line4[1:-2]
if len(line4) > 1:
	line4 = line4.split(", ")
	line4 = list(map(int, line4))
elif len(line4) == 1:
	line4 = [int(line4)]
else:
	line4 = []
goalState.append(line4)

line5 = inputFile.readline()
line5 = line5[1:-2]
if len(line5) > 1:
	line5 = line5.split(", ")
	line5 = list(map(int, line5))
elif len(line5) == 1:
	line5 = [int(line5)]
else:
	line5 = []
goalState.append(line5)

line6 = inputFile.readline()
line6 = line6[1:-2]
if len(line6) > 1:
	line6 = line6.split(", ")
	line6 = list(map(int, line6))
elif len(line6) == 1:
	line6 = [int(line6)]
else:
	line6 = []
goalState.append(line6)

inputFile.close()

#Converting the given input to blockworld state
initialBlockState = BlockWorld()
for x, stack in enumerate(initialState):
	stackOfBlocks = []
	for y, num in enumerate(stack):
		newBlock = Block()
		newBlock.label = num
		newBlock.stackNo = x + 1
		newBlock.blockPos = y 
		if(y-1 >= 0):
			newBlock.sittingOn = stack[y-1]
		stackOfBlocks.append(newBlock)
	if(x == 0):
		initialBlockState.stack1 = copy.deepcopy(stackOfBlocks)
	elif(x == 1):
		initialBlockState.stack2 = copy.deepcopy(stackOfBlocks)
	else:
		initialBlockState.stack3 = copy.deepcopy(stackOfBlocks)

#Converting the goal state to blockworld state
goalBlockState = BlockWorld()
for x, stack in enumerate(goalState):
	stackOfBlocks = []
	for y, num in enumerate(stack):
		newBlock = Block()
		newBlock.label = num
		newBlock.stackNo = x + 1
		newBlock.blockPos = y 
		if(y-1 >= 0):
			newBlock.sittingOn = stack[y-1]
		stackOfBlocks.append(newBlock)
	if(x == 0):
		goalBlockState.stack1 = copy.deepcopy(stackOfBlocks)
	elif(x == 1):
		goalBlockState.stack2 = copy.deepcopy(stackOfBlocks)
	else:
		goalBlockState.stack3 = copy.deepcopy(stackOfBlocks)

#Initial Heuristic of the goal state
if(heuristic == 1):
	hValue = 0
	hValue = 3 * (len(goalBlockState.stack1) + len(goalBlockState.stack2) + len(goalBlockState.stack3))
	goalBlockState.hValue = hValue
	heuristic1(initialBlockState, goalBlockState)
elif(heuristic == 2):
	hValue = 0
	goalBlockState.hValue = hValue
	heuristic2(initialBlockState, goalBlockState)
elif(heuristic == 3):
	hValue = 0
	goalBlockState.hValue = hValue
	heuristic3(initialBlockState, goalBlockState)

#Printing all info to output file
print("Algorithm: " + algo)
print("Heuristic: " + str(heuristic))
#print("\n----Initial State----")
#initialBlockState.printBlockWorld()
print("\n----Goal State----")
goalBlockState.printBlockWorld()

global numOfStatesExplored
numOfStatesExplored = 0
if(algo == "BFS"):
	result = BFS(initialBlockState, goalBlockState, heuristic)
elif(algo == "HC"):
	result = HC(initialBlockState, goalBlockState, heuristic)

print("\n----Final State----")
result.printBlockWorld()

print("\nIs goal state reached?: ", end="")
if goalTest(result, goalBlockState):
	print("Yes")
else:
	print("No")

print("No of States Explored: " + str(numOfStatesExplored))
print("Time Taken: %s seconds" % (time.time() - start_time))

#==============================================================================================#