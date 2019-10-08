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
        initial_domain = [1,2,3,4,5,6,7,8,9]
        transformed_puzzle = copy.deepcopy(self.puzzle)
        for row_index, row in enumerate(self.puzzle):
            for col_index, value in enumerate(row):
                if value == 0:
                    transformed_puzzle[row_index][col_index] = initial_domain[::]
                else:
                    transformed_puzzle[row_index][col_index] = value

        # in AC3,
        # loop through queue constraints tuple
        self.acthree(transformed_puzzle)
        return self.backtracking(transformed_puzzle)

    # CSP is list of list of domain or assigned value
    # Deduce assignment from csp

    # Returns False if result == failure, else return the csp
    def backtracking(self, csp):
        if self.assignmentIsComplete(csp):
            return csp

        # Get index of variable to assign
        var = self.selectUnassignedVar(csp)
        domain = csp[var[0]][var[1]]
        for val in domain:
            cspcopy = copy.deepcopy(csp) # Should be the only place required for deepcopy
            cspcopy[var[0]][var[1]] = val # Assignment
            if self.acthree(cspcopy): # If inference never fail
                result = self.backtracking(cspcopy)
                if result != False: # If never fail
                    return result

        return False


    def assignmentIsComplete(self, csp):
        for row in csp:
            for elem in row:
                if not self.isAssigned(elem):
                    return False

        return True

    def selectUnassignedVar(self, csp):
        vars = self.selectMostConstrainedVars(csp)
        var = self.selectMostConstrainingVar(csp, vars)
        return var

    def selectMostConstrainedVars(self, csp):
        vars = (9, []) # (Domain size, all vars with that domain size)
        for i in range(9):
            for j in range(9):
                domain = csp[i][j]
                if type(domain) == int:
                    continue

                size = len(domain)
                if size == vars[0]:
                    vars[1].append((i,j))

                if size < vars[0]:
                    vars = (size, [(i,j)])

        return vars[1]

    def selectMostConstrainingVar(self, csp, vars):
        most = (-1, None)
        for var in vars:
            numOfNeighbours = self.getNumOfUnassignedNeighbours(csp, var)
            if numOfNeighbours > most[0]:
                most = (numOfNeighbours, var)
        return most[1]

    def getNumOfUnassignedNeighbours(self, csp, var):
        neighbours = self.get_neighbouring_constraints(var)
        total = 0
        for neighbour in neighbours:
            if not self.isAssigned(csp[neighbour[0]][neighbour[1]]):
                total += 1
        return total

    def isAssigned(self, i):
        return i == int

    # index is a tuple with (row, col)
    def get_neighbouring_constraints(self, index):

        neighbours = set()

        #same col
        for row_index in range(0, 9):
            neighbours.add((row_index,index[1]))

        #same row
        for col_index in range(0, 9):
            neighbours.add((index[0], col_index))

        topLeftOfBox = (index[0] - (index[0] % 3), index[1] - (index[1] % 3))

        for i in range(topLeftOfBox[0], topLeftOfBox[0] + 3):
            for j in range(topLeftOfBox[1], topLeftOfBox[1] + 3):
                neighbours.add((i,j))
        
        neighbours.remove((index)) # Remove self
        return list(neighbours)


    # Modifies CSP directly
    # Returns False if not consistent
    def acthree(self, csp):
        # define initial constraints into a queue
        queue_constraint_tuple = []
        for row_index, row in enumerate(csp):
            for col_index, value in enumerate(row):
                if not self.isAssigned(value):  # if variable
                    neighbours = self.get_neighbouring_constraints((row_index, col_index))
                    constraints = [((row_index, col_index), neighbour) for neighbour in neighbours]
                    queue_constraint_tuple += constraints

        while queue_constraint_tuple:
            constraint = queue_constraint_tuple.pop()
<<<<<<< HEAD
            if self.revise(csp, constraint[0], constraint[1]):
                if len(csp[constraint[0][0]][constraint[0][1]]) == 0:
                    return False
                neighbouring_arcs = self.get_neighbouring_constraints(constraint[0])
                neighbouring_arcs.remove(constraint[1])
=======
            if self.revise(self.transformed_puzzle, constraint[0], constraint[1]):
                neighbouring_arcs = self.get_neighbouring_constraints(constraint[0])
>>>>>>> 194e5de3bf593c8407aa8d65c09903b7cd2ebf4d
                for arc in neighbouring_arcs:
                    if not self.isAssigned(csp[arc[0]][arc[1]]):
                        queue_constraint_tuple.append((arc, constraint[0]))

        return True

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
