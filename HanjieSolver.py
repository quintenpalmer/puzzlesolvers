#!/usr/bin/env python
import sys
import re
class HanjieSolver:
	def __init__(self,filename):
		self.filename = filename
		self.functional = True

	def changeBoard(self,filename):
		self.filename = filename
		self.functional = True
		print "Change: Success! (file " + self.filename + ")"

	def parseBoard(self):
		if len(self.filename.split('.')) > 1:
			if self.filename.split('.')[1] == "hj":
				f = open(self.filename,'r')
				tmpBoard = []
				height = 0
				self.rowEntries = []
				self.colEntries = []
				for line in f:
					tmpBoard.append(line)
					t = re.findall('\|',line)
					if len(t) > 0:
						height += 1
						tmp = line.replace('|','').replace(' ','').rstrip().split(',')
						ints = []
						for c in tmp:
							ints.append(int(c))
						self.rowEntries.append(ints)
				width = len(tmpBoard[0].split('|'))-2
				for i in xrange(0,width):
					self.colEntries.append([])
				for line in tmpBoard[height:]:
					i = 0
					line = line.rstrip()
					for char in line[1:][::2]:
						if char != ' ':
							self.colEntries[i].append(int(char))
						i += 1
				if len(self.rowEntries) != height or len(self.colEntries) != width:
					print "Load  : Fail! (number of col/row entries did not match board size)"
					self.functional = False
					return 3
				self.board = []
				for i in xrange(0,height):
					self.board.append([])
					for j in xrange(0,width):
						self.board[i].append('g')
				self.height = height
				self.width = width
				for entry in self.colEntries:
					total = 0
					for i in entry:
						total += i + 1
					if total-1 > self.height:
						print "Load  : Fail! (A row tried to add up to more than the height)"
						self.functional = False
						return 3
				for entry in self.rowEntries:
					total = 0
					for i in entry:
						total += i + 1
					if total-1 > self.width:
						print "Load  : Fail! (A column tried to add up to more than the width)"
						self.functional = False
						return 3
			else:
				print "Load  : Fail! (invalid filetype given only .hj supported)"
				self.functional = False
				return 1
		else:
			print "Load  : Fail! (must give a .hj file)"
			self.functional = False
			return 6
		self.functional = True
		print "Load  : Success!"

	def checkComplete(self):
		for i in xrange(0,len(self.board)):
			for j in xrange(0,len(self.board[i])):
				if self.board[i][j] == 'g':
					return False
		return True

	def checkValid(self):
		for i in xrange(0,len(self.board)):
			for j in xrange(0,len(self.board[i])):
				if len(self.board[i][j]) > 1:
					return False
		return True

	def getLowHigh(self,i,wh,rc):
		highs = []
		lows = []
		for entry in rc[i]:
			if len(highs) !=0:
				highs.append(entry+highs[len(highs)-1]+1)
			else:
				highs.append(entry)
			lows.append(0)
		j = len(lows)-1
		for entry in rc[i].__reversed__():
			if j != len(lows)-1:
				lows[j] = lows[j+1]-entry-1
			else:
				lows[j] = wh-entry
			j -= 1
		return (lows,highs)

	def rowSolve(self):
		for i in xrange(0,self.height):
			anchors = []
			for j in xrange(0,self.width):
				if self.board[i][j] == 'f':
					anchors.append(j)
			for a in anchors:
				print a
			lowHigh = self.getLowHigh(i,self.width,self.rowEntries)
			lows = lowHigh[0]
			highs = lowHigh[1]
			for si in xrange(0,len(lows)):
				for j in xrange(lows[si],highs[si]):
					print "filling in at: ", i, j
					self.board[i][j] = 'f'
			print '\n',

	def colSolve(self):
		for i in xrange(0,self.width):
			anchors = []
			for j in xrange(0,self.height):
				if self.board[j][i] == 'f':
					anchors.append(j)
			lowHigh = self.getLowHigh(i,self.height,self.colEntries)
			lows = lowHigh[0]
			highs = lowHigh[1]
			for si in xrange(0,len(lows)):
				for j in xrange(lows[si],highs[si]):
					print "filling in at: ", i, j
					self.board[j][i] = 'f'
			print '\n',

	def solveBoard(self):
		if self.functional:
			done = False
			oldBoard = []
			while not done and oldBoard != self.board:
				oldBoard = self.copyBoard()
				self.rowSolve()
				self.colSolve()
				done = self.checkComplete()
			if self.checkValid():
				print "Solve : Success!"
			else:
				print "Solve : Fail! (invalid board produced)"
		else:
			print "Solve : Fail! (nonfunctional board provided)"

	def copyBoard(self):
		copy = []
		for i in xrange(0,len(self.board)):
			copy.append([])
			for j in xrange(0,len(self.board[i])):
				copy[i].append(self.board[i][j])
		return copy
		
	def printBoard(self,debug=False):
		if self.functional:
			self.fout(sys.stdout,'  ',debug=debug)
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

	def fout(self,out,indent,debug=False):
		for i in xrange(0,self.height):
			for j in xrange(0,self.width):
				out.write(self.board[i][j])
			out.write('\n')
		for entry in self.rowEntries:
			out.write('\n')
			for n in entry:
				out.write(str(n))
		out.write('\n')
		for entry in self.colEntries:
			out.write('\n')
			for n in entry:
				out.write(str(n))
		out.write('\n')
