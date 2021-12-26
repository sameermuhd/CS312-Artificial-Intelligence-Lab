Command to run the file:
$ python3 <codeName>.py <inputFile.txt>

Eg.: python3 code.py input.txt

------------------------------------------------------------------

Note:

1. The input file format is as follows:

<index> 
<m * n maze>

Where index = 0 for BFS
	  index = 1 for DFS
	  index = 2 for DFID

**Also note input file should not have any extra lines after maze**

Eg.: 
2
+--+--+--+--+
   |     |  |
+  +  +  +  +
|    *|     |
+--+--+  +--+
|     |     |
+  +  +--+  +
|  |        |
+--+--+--+--+

------------------------------------------------------------------

2. The code outputs a text file output.txt with following format:

<Number of states explored>
<Length of path found>
<Maze with path formed with 0s>

Eg.:
62
9
0--+--+--+--+
00 |     |  |
+0 +  +  +  +
|00000|     |
+--+--+  +--+
|     |     |
+  +  +--+  +
|  |        |
+--+--+--+--+

------------------------------------------------------------------