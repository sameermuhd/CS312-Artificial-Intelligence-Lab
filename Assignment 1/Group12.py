#libraries used
import sys
import copy


#==============================================================================================#
#Node Class Definition
class Node:
    def __init__(self):
        self.value = ""         #Value given in maze (+, |, \, * etc)
        self.color = "white"    #types of nodes (Open -> grey, Closed -> black, Unexplored -> white)
        self.dist = -1          #distance of node from source
        self.parent = None      #node's parent
        self.xpos = -1          #node's x position
        self.ypos = -1          #node's y position


#==============================================================================================#
#Goal Test
def goalTest(state):
    if (state.value == '*'):
        return True             #Food has be found
    else:
        return False            #Food has not been found


#==============================================================================================#
#Function to check if a given state/position is inside the maze
def isValid(width, height, state):
    row, col = state[0], state[1]
    if any((row < 0, row > height - 1, col < 0, col > width - 1)):
        return False            #State is not valid
    else:
        return True             #State is valid


#==============================================================================================#
#Function to check if a given state/position in a maze is a path or food
def isPath(mazeNodes, state):
    row, col = state[0], state[1]
    if mazeNodes[row][col].value == " " or mazeNodes[row][col].value == "*":
        return True             #State is path or food
    else:
        return False            #State is not path or food


#==============================================================================================#
#Function to generate neighbours of a node in the Order given below
def moveGen(mazeNodes, state):
    row, col = state.xpos, state.ypos
    width, height = len(mazeNodes[0]), len(mazeNodes)
    neighbours = []
    DOWN = [row + 1, col]
    UP = [row - 1, col]
    RIGHT = [row, col + 1]
    LEFT = [row, col - 1]
    if isValid(width, height, DOWN) and isPath(mazeNodes, DOWN):    #DOWN
        neighbours.append(mazeNodes[DOWN[0]][DOWN[1]])
    if isValid(width, height, UP) and isPath(mazeNodes, UP):        #UP
        neighbours.append(mazeNodes[UP[0]][UP[1]])
    if isValid(width, height, RIGHT) and isPath(mazeNodes, RIGHT):  #RIGHT
        neighbours.append(mazeNodes[RIGHT[0]][RIGHT[1]])
    if isValid(width, height, LEFT) and isPath(mazeNodes, LEFT):    #LEFT
        neighbours.append(mazeNodes[LEFT[0]][LEFT[1]])

    return neighbours


#==============================================================================================#
#Function to print maze with solution path and return solution path length
def SolutionMaze(maze, source, foodCoords):
    global outFile                                  #output file
    solution = copy.deepcopy(maze)
    solution[foodCoords.xpos][foodCoords.ypos] = 0
    path = [foodCoords]
    while path[-1] != source:
        previousParent = path[-1].parent
        path.append(previousParent)
        solution[previousParent.xpos][previousParent.ypos] = 0
    
    path.reverse()
    solPathLength = len(path)                       #Solution Path Length
    outFile.write(str(solPathLength) + "\n")
    for i in range(len(solution)):
        for j in range(len(solution[0])):
            outFile.write(str(solution[i][j]))
        outFile.write("\n")

    return solPathLength


#==============================================================================================#
#BFS
def BFS(maze, mazeNodes, source, foodCoords):
    global outFile                              #output file
    frontierQueue = []
    frontierQueue.append(source)                #Similar to enqueue
    numOfStatesExplored = 0
    solPathLength = -1

    while frontierQueue:
        state = frontierQueue.pop(0)            #Similar to dequeue
        numOfStatesExplored += 1

        if goalTest(state): 
            outFile.write(str(numOfStatesExplored) + "\n")
            solPathLength = SolutionMaze(maze, source, state)
            break

        stateNeighbours = moveGen(mazeNodes, state)
        unexploredNeighbours = [node for node in stateNeighbours if node.color == "white"]

        for neighbour in unexploredNeighbours:
            neighbour.color = "gray"
            neighbour.dist = state.dist + 1
            neighbour.parent = state
            frontierQueue.append(neighbour)
        state.color = "black"

    if solPathLength == -1:
        print("Food Not Found")


#==============================================================================================#
#DFS
def DFS(maze, mazeNodes, source, foodCoords):
    frontierStack = []
    frontierStack.append(source)                #Similiar to push
    numOfStatesExplored = 0
    solPathLength = -1

    while frontierStack:
        state = frontierStack.pop()             #Similar to pop
        numOfStatesExplored += 1

        if goalTest(state): 
            outFile.write(str(numOfStatesExplored) + "\n")
            solPathLength = SolutionMaze(maze, source, state)
            break

        stateNeighbours = moveGen(mazeNodes, state)
        unexploredNeighbours = [node for node in stateNeighbours if node.color == "white"]

        for neighbour in unexploredNeighbours:
            neighbour.color = "gray"
            neighbour.dist = state.dist + 1
            neighbour.parent = state
            frontierStack.append(neighbour)
        state.color = "black"

    if solPathLength == -1:
        print("Food Not Found")


#==============================================================================================#
#DLS
def DLS(maze, mazeNodes, state, foodCoords, explored, depth):
    global isFoodFound
    explored.dist += 1
    solPathLength = -1

    if goalTest(state): 
        isFoodFound = True
        outFile.write(str(explored.dist) + "\n")
        solPathLength = SolutionMaze(maze, source, state)
        if solPathLength == -1:
            print("Food Not Found")
        return

    if state.dist - 1 == depth + 1:
        return

    stateNeighbours =  moveGen(mazeNodes, state)
    for neighbour in stateNeighbours:
        if isFoodFound:
            break;
        if neighbour.dist == -1:                #Unexplored Node
            neighbour.parent = state 
            neighbour.dist = state.dist + 1
            DLS(maze, mazeNodes, neighbour, foodCoords, explored, depth)
        elif neighbour.dist > state.dist + 1:   #Optimization
            neighbour.parent = state 
            neighbour.dist = state.dist + 1
            DLS(maze, mazeNodes, neighbour, foodCoords, explored, depth)


#==============================================================================================#
#DFID
def DFID(maze, mazeNodes, source, foodCoords):
    global isFoodFound
    isFoodFound = False
    depth = -1
    explored = Node()
    explored.dist = 0

    while not isFoodFound:
        depth += 1                              #Iteratively increasing depth
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                mazeNodes[i][j].dist = -1
        source.dist = 1
        DLS(maze, mazeNodes, source, foodCoords, explored, depth)


#==============================================================================================#
#main function

#Total arguments
n = len(sys.argv)
if(n != 2):
    print("Usage: python3 <code>.py <inputfile>")
    sys.exit()

try:
    file = open(sys.argv[1], "r")
except IOError:
    print("File not found")
    sys.exit()

algoType = int(file.read(1))            #Reading algorithm type

if(algoType > 2):
    print("Please enter one of the following <index> in input file")
    print("index = 0 for BFS\nindex = 1 for DFS\nindex = 2 for DFID")
    sys.exit()

maze = []                               #Reading maze from input file
file.readline()
for line in file:
    line = line[ :-1]
    maze.append(list(line))
file.close()
    
foodCoords = []                         #Finding food coordinates
for i, row in enumerate(maze):
    if '*' in row:
        foodCoords = [i, row.index('*')]
        break

if not foodCoords:
    print("Food not in maze")
    sys.exit()

mazeNodes = []                          #Converting maze to nodes
for i in range(len(maze)):
    row = []
    for j in range(len(maze[0])):
        newNode = Node()
        newNode.value = maze[i][j]
        newNode.xpos = i
        newNode.ypos = j
        row.append(newNode)
    mazeNodes.append(row)

source = mazeNodes[0][0]                   #Source taken as [0, 0]
global outFile
outFile = open("output.txt", "w")
if algoType == 0:                           #BFS
    BFS(maze, mazeNodes, source, foodCoords)
elif algoType == 1:                         #DFS
    DFS(maze, mazeNodes, source, foodCoords)
elif algoType == 2:                         #DFID
    DFID(maze, mazeNodes, source, foodCoords)
outFile.close()
#==============================================================================================#