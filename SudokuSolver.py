#!/usr/bin/env python
import sys
class SudokuSolver:
	def __init__(self,filename,debug=False):
		self.filename = filename
		self.functional = True
		self.key = 0
		self.debug = debug

	def changeBoard(self,filename):
		self.filename = filename
		self.functional = True
		print "Change: Success! (file " + self.filename + ")"

	def parseBoard(self):
		if len(self.filename.split('.')) > 1:
			suffix = self.filename.split('.')[1]
			if suffix == "csv":
				f = open(self.filename,'r')
				boardString = ''
				for line in f:
					boardString += line.rstrip()
				tmp = boardString.split(',')
			elif suffix == "sdk":
				f = open(self.filename,'r')
				boardString = ''
				for line in f:
					boardString += line.rstrip()[1:]
				boardString = boardString.rstrip('|')
				boardString = boardString.replace('| |','|')
				tmp = boardString.split('|')
			elif suffix == "raw":
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
				print "Parse : Fail! (invalid filetype given ." + self.filename.split('.')[1] + " not supported)"
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
			print "Parse : Fail! (invalid board provided, " + str(len(tmp)) + " entr" + yies + ")"
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
		print "Parse : Success!"

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


	def elim(self,i,j):
		row = self.getRow(i,j)
		col = self.getCol(i,j)
		square = self.getSquare(i,j)
		self.elimHelper(i,j,row,1,9)
		self.elimHelper(i,j,col,9,1)
		self.elimHelper(i,j,square,3,3)

	def elimHelper(self,i,j,group,fi,fj):
		val = self.board[i][j]
		if len(val) == 1:
			val = val[0]
			for oi in xrange(group[0],group[0]+fi):
				for oj in xrange(group[1],group[1]+fj):
					if (i,j) != (oi,oj) and val in self.board[oi][oj]:
						self.board[oi][oj].remove(val)

	def containsVal(self,val,oi,oj):
		for v in self.board[oi][oj]:
			if v == val:
				return True
		return False

	def onlyValid(self,i,j):
		row = self.getRow(i,j)
		col = self.getCol(i,j)
		square = self.getSquare(i,j)
		if len(self.board[i][j]) > 1:
			if self.onlyValidHelper(i,j,row,1,9):
				return None
			if self.onlyValidHelper(i,j,col,9,1):
				return None
			if self.onlyValidHelper(i,j,square,3,3):
				return None

	def onlyValidHelper(self,i,j,group,fi,fj):
		for entry in self.board[i][j]:
			only = True
			for oi in xrange(group[0],group[0]+fi):
				for oj in xrange(group[1],group[1]+fj):
					if self.containsVal(entry,oi,oj) and (oj,oi) != (j,i):
						only = False
			if only:
				self.board[i][j] = [entry]
				return True
		return False

	def findLast(self,i,j):
		row = self.getRow(i,j)
		col = self.getCol(i,j)
		square = self.getSquare(i,j)
		self.findLastHelper(i,j,row,1,9)
		self.findLastHelper(i,j,col,9,1)
		self.findLastHelper(i,j,square,3,3)

	def findLastHelper(self,i,j,group,fi,fj):
		triples = []
		doubles = []
		for oi in xrange(group[0],group[0]+fi):
			for oj in xrange(group[1],group[1]+fj):
				if len(self.board[oi][oj]) == 3:
					triples.append((oi,oj))
				if len(self.board[oi][oj]) == 2:
					doubles.append((oi,oj))
		self.singleOut(triples, doubles)

	def singleOut(self,triples,doubles):
		if len(doubles) > 1:
			pairs = {}
			for i,j in doubles:
				if not tuple(self.board[i][j]) in pairs.keys():
					pairs[tuple(self.board[i][j])] = 1
				else:
					pairs[tuple(self.board[i][j])]+= 1
			matches = {}
			for i,j in triples:
				for key in pairs.keys():
					val = pairs[key]
					if val == 2:
						if set(key).issubset(set(self.board[i][j])):
							if not tuple(self.board[i][j]) in matches.keys():
								lastval = [x for x in self.board[i][j] if x not in key]
								matches[tuple(self.board[i][j])] = (i,j,lastval)
							else:
								matches[tuple(self.board[i][j])] = None
			for key in matches:
				val = matches[key]
				if val != None:
					self.board[val[0]][val[1]] = val[2]

	def entryElim(self,i,j):
		row = self.getRow(i,j)
		col = self.getCol(i,j)
		square = self.getSquare(i,j)

		nums = []
		for n in xrange(0,9):
			nums.append([])
			for si in xrange(square[0],square[0]+3):
				for sj in xrange(square[1],square[1]+3):
					for s in self.board[si][sj]:
						if s == n+1:
							nums[n].append((si,sj))
		self.onlyCol(nums,square)
		self.onlyRow(nums,square)

	def onlyRow(self,nums,square):
		mySquare = []
		for i in xrange(0,3):
			mySquare.append(square[0]+i)
		for num,entry in enumerate(nums):
			num = num + 1
			only = True
			row = -1
			for sub in entry:
				if row != -1:
					if sub[1] != row:
						only = False
				else:
					row = sub[1]
			if only:
				for i in xrange(0,9):
					for sub in entry:
						if not i in mySquare:
							if not i in entry and num in self.board[i][row]:
								self.board[i][row].remove(num)

	def onlyCol(self,nums,square):
		mySquare = []
		for i in xrange(0,3):
			mySquare.append(square[1]+i)
		for num,entry in enumerate(nums):
			num = num + 1
			only = True
			col = -1
			for sub in entry:
				if col != -1:
					if sub[0] != col:
						only = False
				else:
					col = sub[0]
			if only:
				for i in xrange(0,9):
					for sub in entry:
						if not i in mySquare:
							if not i in entry and num in self.board[col][i]:
								self.board[col][i].remove(num)

	def checkComplete(self):
		for i in xrange(0,9):
			for j in xrange(0,9):
				if len(self.board[i][j]) != 1:
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
		return True

	def solveBoard(self):
		if self.functional:
			done = False
			oldBoard = []
			while not done and oldBoard != self.board:
				oldBoard = self.copyBoard()
				for i in xrange(0,9):
					for j in xrange(0,9):
						self.elim(i,j)
						self.onlyValid(i,j)
						self.findLast(i,j)
						self.entryElim(i,j)
				done = self.checkComplete()
			if self.checkValid():
				print "Solve : Success!"
			else:
				self.debug = True
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

	def printBoard(self,debug=False):
		if self.functional:
			warn = self.fout(sys.stdout,'  ',debug=debug)
			if warn == 0:
				print "Print : Success!"
			elif warn == 1:
				print "Print : Success! (Warning: not a solved board)"
			elif warn == 2:
				print "Print : Success! (Warning: broken board provided)"
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

	def fout(self,out,indent,debug=False):
		debug = debug and self.debug
		warn = 0
		for i in xrange(0,9):
			for j in xrange(0,9):
				if len(self.board[i][j]) == 0:
					warn = 2
				elif len(self.board[i][j]) > 1:
					if warn != 2:
						warn = 1
		def helper(it,i,ik):
			out.write(indent+'|')
			for j in xrange(0,9):
				for k in xrange(ik,ik+3):
					try:
						out.write(str(self.board[i][j][k]))
					except:
						out.write('.')
				out.write('|')
				it += 1
				if divmod(it,3)[1]==0 and it != 9:
					out.write(' |')
			out.write('\n')
		if not debug:
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
					elif len(self.board[i][j]) == 0:
						out.write('.')
					else:
						out.write('*')
					out.write('|')
					it += 1
					if divmod(it,3)[1]==0 and it != 9:
						out.write(' |')
				out.write('\n')
		else:
			it = 0
			jt = 0
			for i in xrange(0,9):
				if divmod(jt,3)[1]==0 and jt != 0:
						out.write('\n')
						jt = 0
				jt += 1
				it = 0
				helper(it,i,0)
				helper(it,i,3)
				helper(it,i,6)
		return warn
