#!/usr/bin/env python
import sys
from PuzzleSolver import PuzzleSolver

if len(sys.argv) < 2:
	print "Must supply file to read or an input board"
	sys.exit(1)
first = True
for arg in sys.argv[1:]:
	if first:
		s = PuzzleSolver(arg)
		first = False
	else:
		s.changeBoard(arg)
	s.loadBoard()
	s.solveBoard()
	#s.writeBoard()
	s.printBoard()
