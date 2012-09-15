#!/usr/bin/env python
import sys
from HanjieSolver import HanjieSolver
from SudokuSolver import SudokuSolver
class PuzzleSolver:
	def __init__(self,filename):
		self.filename = filename

	def changeBoard(self,filename):
		self.filename = filename
		print "Change: Success! (file " + self.filename + ")"

	def loadBoard(self):
		if len(self.filename.split('.')) > 1:
			if self.filename.split('.')[1] == "sdk":
				self.parser = SudokuSolver(self.filename)
			elif self.filename.split('.')[1] == "hj":
				self.parser = HanjieSolver(self.filename)
			else:
				print "Load  : Fail! (invalid filetype given ." + self.filename.split('.')[1] + " not supported)"
				return 1
		else:
			print "Load  : Fail! (input file has no extension)"
			return 5
		self.parser.parseBoard()
		print "Load  : Success!"

	def solveBoard(self):
		self.parser.solveBoard()
		
	def printBoard(self,debug=False):
		self.parser.printBoard(debug=debug)

	def writeBoard(self):
		self.parser.writeBoard()
