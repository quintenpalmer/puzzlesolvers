#!/usr/bin/env python
import sys
class SudokuSolver:
	def __init__(self,filename):
		self.filename = filename
		self.functional = True

	def changeBoard(self,filename):
		self.filename = filename
		self.functional = True
		print "Change: Success! (file " + self.filename + ")"

	def parseBoard(self):
		if len(self.filename.split('.')) > 1:
			if self.filename.split('.')[1] == "csv":
				f = open(self.filename,'r')
				boardString = ''
				for line in f:
					boardString += line.rstrip()
				tmp = boardString.split(',')
			elif self.filename.split('.')[1] == "sdk":
				f = open(self.filename,'r')
				boardString = ''
				for line in f:
					boardString += line.rstrip()[1:]
				boardString = boardString.rstrip('|')
				boardString = boardString.replace('| |','|')
				tmp = boardString.split('|')
			elif self.filename.split('.')[1] == "raw":
				f = open(self.filename,'r')
				boardString = ''
				for line in f:
					boardString += line.rstrip('\n')
				pass
				tmp = []
				for i in xrange(0,9):
					for j in xrange(0,9):
						tmp.append(boardString[j+i*9])
			else:
				print "Load  : Fail! (invalid filetype given ." + self.filename.split('.')[1] + " not supported)"
				self.functional = False
				return 1
		else:
			boardString = self.filename
			self.filename = 'noFile'
			tmp = boardString.split(',')
		if len(tmp) != 81:
			if len(tmp) == 1:
				yies = 'y'
			else:
				yies = 'ies'
			print "Load  : Fail! (invalid board provided, " + str(len(tmp)) + " entr" + yies + ")"
			self.functional = False
			return 2
		self.board = []
		for i in xrange(0,9):
			self.board.append([])
			for j in xrange(0,9):
				if tmp[j+i*9] == ' ' or tmp[j+i*9] == '.':
					self.board[i].append([1,2,3,4,5,6,7,8,9])
				else:
					self.board[i].append([int(tmp[j+i*9])])
		self.functional = True
		print "Load  : Success!"

	def getSquare(self,i,j):
		if i < 3:
			oi = 0
		elif i < 6:
			oi = 3
		elif i < 9:
			oi = 6
		if j < 3:
			oj = 0
		elif j < 6:
			oj = 3
		elif j < 9:
			oj = 6
		return (oi,oj)
	def getRow(self,i,j):
		return (i,0)
	def getCol(self,i,j):
		return (0,j)

	def elimSquare(self,i,j):
		square = self.getSquare(i,j)
		val = self.board[i][j]
		if len(val) == 1:
			val = val[0]
			for oi in xrange(square[0],square[0]+3):
				for oj in xrange(square[1],square[1]+3):
					if (i,j) != (oi,oj) and val in self.board[oi][oj]:
						self.board[oi][oj].remove(val)

	def elimColumn(self,i,j):
		col = self.getCol(i,j)
		val = self.board[i][j]
		if len(val) == 1:
			val = val[0]
			for oi in xrange(col[0],col[0]+9):
				for oj in xrange(col[1],col[1]+1):
					if (i,j) != (oi,oj) and val in self.board[oi][oj]:
						self.board[oi][oj].remove(val)

	def elimRow(self,i,j):
		row = self.getRow(i,j)
		val = self.board[i][j]
		if len(val) == 1:
			val = val[0]
			for oi in xrange(row[0],row[0]+1):
				for oj in xrange(row[1],row[1]+9):
					if (i,j) != (oi,oj) and val in self.board[oi][oj]:
						self.board[oi][oj].remove(val)

	def onlyValid(self,i,j):
		row = self.getRow(i,j)
		col = self.getCol(i,j)
		square = self.getSquare(i,j)
		if len(self.board[i][j]) > 1:
			for entry in self.board[i][j]:
				only = True
				for oi in xrange(row[0],row[0]+1):
					for oj in xrange(row[1],row[1]+9):
						if self.containsVal(entry,oi,oj) and oj != j:
							only = False

				if only:
					self.board[i][j] = [entry]
					return None
			for entry in self.board[i][j]:
				only = True
				for oi in xrange(col[0],col[0]+9):
					for oj in xrange(col[1],col[1]+1):
						if self.containsVal(entry,oi,oj) and oi != i:
							only = False

				if only:
					self.board[i][j] = [entry]
					return None
			for entry in self.board[i][j]:
				only = True
				for oi in xrange(square[0],square[0]+3):
					for oj in xrange(square[1],square[1]+3):
						if self.containsVal(entry,oi,oj) and (oj,oi) != (j,i):
							only = False

				if only:
					self.board[i][j] = [entry]
					return None

	def containsVal(self,val,oi,oj):
		for v in self.board[oi][oj]:
			if v == val:
				return True
		return False

	def checkComplete(self):
		for i in xrange(0,9):
			for j in xrange(0,9):
				if len(self.board[i][j]) > 1:
					return False
		return True

	def checkValid(self):
		for i in xrange(0,9):
			a = []
			b = []
			for j in xrange(0,9):
				if len(self.board[i][j]) != 1:
					return False
				if len(self.board[j][i]) != 1:
					return False
				if self.board[i][j][0] in a:
					return False
				if self.board[j][i][0] in b:
					return False
				a.append(self.board[i][j][0])
				b.append(self.board[j][i][0])
		for i in xrange(0,9,3):
			for j in xrange(0,9,3):
				a = []
				for si in xrange(i,i+3):
					for sj in xrange(j,j+3):
						if len(self.board[si][sj]) != 1:
							return False
						if self.board[si][sj][0] in a:
							return False
				pass
		return True

	def solveBoard(self):
		if self.functional:
			done = False
			oldBoard = []
			while not done and oldBoard != self.board:
				oldBoard = self.copyBoard()
				for i in xrange(0,9):
					for j in xrange(0,9):
						self.elimSquare(i,j)
						self.elimRow(i,j)
						self.elimColumn(i,j)
						self.onlyValid(i,j)
				done = self.checkComplete()
			if self.checkValid():
				print "Solve : Success!"
			else:
				print "Solve : Fail! (invalid board produced)"
		else:
			print "Solve : Fail! (nonfunctional board provided)"

	def copyBoard(self):
		copy = []
		for i in xrange(0,9):
			copy.append([])
			for j in xrange(0,9):
				copy[i].append([])
				for k in xrange(0,len(self.board[i][j])):
					copy[i][j].append(self.board[i][j][k])
		return copy
		
	def printBoard(self):
		if self.functional:
			self.fout(sys.stdout,'  ')
			print "Print : Success!"
		else:
			print "Print : Fail! (nonfunctional board provided)"
			return 1

	def writeBoard(self):
		if self.functional:
			try:
				splitFile = self.filename.split('/')
				outFile = ''
				for path in splitFile[:(len(splitFile)-1)]:
					outFile += path + '/'
				outFile += "solved/"
				outFile += splitFile[len(splitFile)-1].split('.')[0] + '.sdk'
				f = open(outFile,"w")
				self.fout(f,'')
				print "Write : Success! (to " + outFile + ")"
				f.close()
			except:
				print "Write : Fail! (possibly solved directory doesn't exist)"
				return 3
		else:
			print "Write : Fail! (nonfunctional board provided)"

	def fout(self,out,indent):
		it = 0
		jt = 0
		for i in xrange(0,9):
			if divmod(jt,3)[1]==0 and jt != 0:
					out.write('\n')
					jt = 0
			jt += 1
			it = 0
			out.write(indent+'|')
			for j in xrange(0,9):
				if len(self.board[i][j]) == 1:
					out.write(str(self.board[i][j][0]))
				else:
					out.write('*')
				out.write('|')
				it += 1
				if divmod(it,3)[1]==0 and it != 9:
					out.write(' |')
			out.write('\n')
