#libraries used
import sys
from numpy import random

#==============================================================================================#
#Generate Function
def generate(n, k):
	literals = [item for item in range(1, 2*n+1)]
	clause = []
	for _ in range(k):
		terminate = False
		while not terminate:
			choices = sorted(list(random.choice(literals, 3)))
			end = False
			for i in range(0, 2):
				for j in range(i+1, 3):
					#Making sure same literals or literal and its negation doesn't occur
					if (choices[j] - choices[i] == 0) or ((choices[j] - choices[i] == 1) and (choices[j]%2 == 0)):
						end = True
			if not end:
				for i in range(3):
					if (choices[i]%2 == 0):
						choices[i] = chr((choices[i]//2) + ord('`'))
					else:
						choices[i] = chr((choices[i]//2 + 1) + ord('@'))

				choices = tuple(choices)
				if tuple(choices) not in clause:
					clause.append(tuple(choices))
					terminate = True
				
	return clause

#==============================================================================================#
#main
#Total arguments
n = len(sys.argv)
if(n != 3):
    print("Usage: python3 <code>.py <numOfVariables> <numOfClauses>")
    sys.exit()

numOfVar = int(sys.argv[1])
numOfCla = int(sys.argv[2])
if numOfCla > 2**(numOfVar):
	print("Maximum number of clauses exceeded")
	sys.exit()
	
sys.stdout = open("clauses.txt", "w")
clause = generate(numOfVar, numOfCla)
for row in clause:
	print(row)

#==============================================================================================#