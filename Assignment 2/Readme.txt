Command to run the file:
$ python3 <Group12>.py <input.txt> <BFS/HC> <1/2/3> <output.txt>

Eg.: python3 Group12.py input.txt BFS 1 output.txt

Command Line Arguments:
1. <Group12>.py : The code implementing Best First Search and Hill Climb-
ing algorithms along with three heuristic functions.
2. <input.txt> : Name of the input file used in .txt format.
3. <BFS/HC> : The algorithm used - BFS stands for Best First Search and
HC stands for Hill Climbing.
4. <1/2/3> : The index of heuristic function used.
5. <output.txt> : Name of the output file to be obtained on running the
code in .txt format.

------------------------------------------------------------------

For ease of running please use the given script file run.sh. To run it 
simply use the below command
$ bash run.sh

------------------------------------------------------------------

Note:

The input file format is as follows:

Initial State:
<[Stack 1]>
<[Stack 2]>
<[Stack 3]>

Goal State:
<[Stack 1]>
<[Stack 2]>
<[Stack 3]>

**Also note input file should not have any extra lines the above lines**

Eg.: 
Initial State:
[1, 5, 4, 2, 6]
[]
[3]

Goal State:
[1]
[5, 2, 6, 4]
[3]

------------------------------------------------------------------
