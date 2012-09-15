#!/usr/bin/env python
from SudokuSolver import SudokuSolver
import sys

s = SudokuSolver('boards/example.sdk')
s.parseBoard()
s.printBoard()
s.onlyValid(0,0)
s.printBoard()
