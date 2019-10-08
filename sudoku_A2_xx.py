import sys
import copy

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        #TODO: Your code here

        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans

    # CSP is list of list of domain or assigned value
    # Deduce assignment from csp
    def backtracking(self, csp):
        if self.assignmentIsComplete(csp):
            return csp

        # Get index of variable to assign
        var = self.selectUnassignedVar(csp)


    def assignmentIsComplete(self, csp):
        for i in csp:
            for j in i:
                if not self.isAssigned(j):
                    return False

        return True

    def selectUnassignedVar(self, csp):
        vars = self.selectMostConstrainedVars(csp)
        var = self.selectMostConstrainingVar(csp, vars)
        return var

    def selectMostConstrainingVar(self, csp, vars):
        most = (-1, None)
        for var in vars:
            numOfNeighbours = self.getNumOfUnassignedNeighbours(csp, var)
            if numOfNeighbours > most[0]:
                most = (numOfNeighbours, var)
        return most[1]

    def getNumOfUnassignedNeighbours(self, csp, var):
        row = csp[var[0]]
        col = [row[var[1]] for row in csp]
        topLeftOfBox = (var[0] % 3 + var[0], var[1] % 3 + var[1])
        box = []
        sum = 0
        for i in row:
            if not self.isAssigned(i):
                sum += 1

        for j in col:
            if not self.isAssigned(j):
                sum += 1

        return sum
        

    def isAssigned(self, i):
        return i == int


    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

    # CSP is list of list of domain or assigned value
    # CSP shouldn't be a deepcopy!
    # Domain would be a list of integer, assignment value would be an integer
    def revise(self, csp, i, j):
        iDomain = csp[i[0]][i[1]] # Must be a list, cannot be assigned
        jDomain = csp[j[0]][j[1]] # Might be already assigned, or a list
        if type(jDomain) == int:
            if jDomain in iDomain:
                iDomain.remove(jDomain)
                return True
            else:
                return False
        
        if len(jDomain) <= 1:
            if jDomain[0] in iDomain:
                iDomain.remove(jDomain[0])
                return True
        
        return False




if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
