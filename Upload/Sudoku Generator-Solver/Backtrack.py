from random import shuffle
import copy

class SudokuGenerator:
    def __init__(self,grid=None):
        self.counter = 0
        self.path = []
        if grid:
            if len(grid[0]) == 9 and len(grid) == 9:
                self.grid = grid
                self.original = copy.deepcopy(grid)
                self.solveInput()
            else:
                print("Input needs to be a 9x9 matrix.")
        else:
            self.grid = [[0 for i in range(9)] for j in range(9)]
            self.generatePuzzle()
            self.original = copy.deepcopy(self.grid)
    def solveInput(self):
        self.generateSolution(self.grid)
        self.removeNumbers()
        return
    def generatePuzzle(self):
        return
    def testSudoku(self,grid):
        for row in range(9):
            for col in range(9):
                num = grid[row][col]
                grid[row][col] = 0
                if not self.validLocation(grid,row,col,num):
                    return False
                else:
                    grid[row][col] = num
        return True
    def numRow(self,grid,row,number):
        if number in grid[row]:
            return True
        return False
    def numColumn(self,grid,col,number):
        for i in range(9):
            if grid[i][col] == number:
                return True
        return False
    def numSubgrid(self,grid,row,col,number):
        sub_row = (row // 3) * 3
        sub_col = (col // 3)  * 3
        for i in range(sub_row, (sub_row + 3)): 
            for j in range(sub_col, (sub_col + 3)): 
                if grid[i][j] == number: 
                    return True
        return False
    def validLocation(self,grid,row,col,number):
        if self.numRow(grid,row,number):
            return False
        elif self.numColumn(grid,col,number):
            return False
        elif self.numSubgrid(grid,row,col,number):
            return False
        return True
    def findEmpty(self,grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i,j)
        return
    def solvePuzzle(self, grid):
        for i in range(0,81):
            row=i//9
            col=i%9
            if grid[row][col]==0:
                for number in range(1,10):
                    if self.valid_location(grid,row,col,number):
                        grid[row][col]=number
                        if not self.findEmpty(grid):
                            self.counter+=1
                            break
                        else:
                            if self.solvePuzzle(grid):
                                return True
                break
        grid[row][col]=0  
        return False
    def generateSolution(self, grid):
        number_list = [1,2,3,4,5,6,7,8,9]
        for i in range(0,81):
            row=i//9
            col=i%9
            if grid[row][col]==0:
                shuffle(number_list)      
                for number in number_list:
                    if self.valid_location(grid,row,col,number):
                        self.path.append((number,row,col))
                        grid[row][col]=number
                        if not self.findEmpty(grid):
                            return True
                        else:
                            if self.generateSolution(grid):
                                return True
                break
        grid[row][col]=0  
        return False
    def getNonempty(self,grid):
        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    non_empty_squares.append((i,j))
        shuffle(non_empty_squares)
        return non_empty_squares
    def removeNumbers(self):
        non_empty_squares = self.getNonempty(self.grid)
        non_empty_squares_count = len(non_empty_squares)
        rounds = 3
        while rounds > 0 and non_empty_squares_count >= 17:
            row,col = non_empty_squares.pop()
            non_empty_squares_count -= 1
            removed_square = self.grid[row][col]
            self.grid[row][col]=0
            grid_copy = copy.deepcopy(self.grid)
            self.counter=0      
            self.solvePuzzle(grid_copy)   
            if self.counter!=1:
                self.grid[row][col]=removed_square
                non_empty_squares_count += 1
                rounds -=1
        return

import timeit
for i in range(5):
    print(timeit.timeit('SudokuGenerator()', setup='from __main__ import SudokuGenerator', number=1000))
    print(timeit.timeit('SudokuGenerator()', setup='from __main__ import SudokuGenerator', number=10000))