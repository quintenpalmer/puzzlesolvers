#!/usr/bin/env python
from SudokuSolver import SudokuSolver
import sys

s = SudokuSolver('sudoku/example.sdk')
s.parseBoard()
s.printBoard()
s.onlyValid(0,0)
s.printBoard()
