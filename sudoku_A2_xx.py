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
                    transformed_puzzle[row_index][col_index] = copy.deepcopy(initial_domain)
                else:
                    transformed_puzzle[row_index][col_index] = copy.deepcopy(value)
        self.transformed_puzzle = transformed_puzzle

        # define initial constraints into a queue
        queue_constraint_tuple = []
        for row_index, row in enumerate(self.transformed_puzzle):
            for col_index, value in enumerate(row):
                if isinstance(value, list):  # if variable
                    print((row_index, col_index))
                    neighbours = self.get_neighbouring_constraints(row_index, col_index)
                    print(neighbours)
                    queue_constraint_tuple += neighbours

        # in AC3,
        # loop through queue constraints tuple
        self.acthree(queue_constraint_tuple)
        return self.ans

    def get_neighbouring_constraints(self, i, j):
        #get index of neighbours
        list_of_neighbours = []
        #same col
        for row_index in range(0,i):
            list_of_neighbours.append(((i,j), (row_index, j)))
        for row_index in range(i+1,9):
            list_of_neighbours.append(((i,j), (row_index, j)))

        #same col
        for col_index in range(0,j):
            list_of_neighbours.append(((i,j), (i, col_index)))
        for col_index in range(j+1,9):
            list_of_neighbours.append(((i,j), (i, col_index)))

        return list_of_neighbours



    def acthree(self, queue_constraint_tuple):

        while queue_constraint_tuple:
            constraint = queue_constraint_tuple.popleft()
            if self.revise(self.transformed_puzzle, constraint[0], constraint[1]):

                #neighbouring_arcs = self.get_neighbouring_constraints(constraint[1][0], constraint[1][1])
                #for arc in neighbouring_arcs:
                #     if arc == value: continue
                #     else: add ((arc, constraint[0]))

            #
        print (self.transformed_puzzle)





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
