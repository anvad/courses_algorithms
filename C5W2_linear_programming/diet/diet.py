# python3

# Good job! (Max time used: 9.48/30.00, max memory used: 105963520/536870912.)
#   had to change the inequality check to use (lhs > (b[i] + 0.001)) instead of (lhs > (b[i]))

from sys import stdin
from pprint import pprint as pp

EPS = 1e-6
PRECISION = 20


class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row


def SelectPivotElement(a, used_rows, used_columns):
    # This algorithm selects the first free element.
    # You'll need to improve it to pass the problem.
    pivot_element = Position(0, 0)
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column]:
        pivot_element.column += 1

    # at this point, the selected pivot_element might have value 0. 
    # so, we might need to swap rows till we arrive at a non-zero pivot element
    size = len(a)
    while size > (pivot_element.row + 1):
        if a[pivot_element.row][pivot_element.column] == 0:
            pivot_element.row += 1
        else:
            break

    #print("pivot_element is ({},{}) = {}".format(pivot_element.row, pivot_element.column, a[pivot_element.row][pivot_element.column]))
    return pivot_element


def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column;


def ProcessPivotElement(a, b, pivot_element):
    # Write your code here
    pivot_row = pivot_element.row
    pivot_col = pivot_element.column
    divisor = a[pivot_row][pivot_col]

    if divisor == 0:
        return # nothing to process

    # divide pivot row by divisor, so pivot_element scales to 1
    a[pivot_row] = [a_p_el/divisor for a_p_el in a[pivot_row]]
    b[pivot_row] = b[pivot_row]/divisor
    
    # substitute into other equations (i.e rows). This will make the pivot_col entry in all rows = 0
    for row_id in range(len(a)):
        if row_id == pivot_row:
            continue
        row_multiplier = a[row_id][pivot_col]
        a[row_id] = [a_r_el - (row_multiplier * a_p_el) for a_r_el, a_p_el in zip(a[row_id], a[pivot_row])]
        b[row_id] = b[row_id] - (row_multiplier * b[pivot_row])

    #print("a after processing: ", a)


def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True


def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns)
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)

    return b


def solve_diet_problem(n, m, A, b, c):
    # Write your code here

    # all constants
    min_pleasure = -100
    very_big_number = 10 ** 9

    # let's start by adding the implicit inequalities into A and b
    #print("A before:")
    #pp(A)
    #pp(b)
    for i in range(m):
        new_row_A = ([0] * i) + [-1] + ([0] * (m - i - 1))
        #print("new_row_A", new_row_A)
        A += [new_row_A]
    b.extend([0] * m)

    # next add the bounding inequality
    A += [[1]* m]
    b.append(very_big_number)
    #print("A after:")
    #pp(A)
    #pp(b)

    # next, we need a way of selecting m rows out of n + m + 1 rows
    subsets, subsets_b, subsets_rowsets = find_subsets(A, b, m)

    # now solve each subset of inequalities as if they were a set of equalities
    pleasure = [] # we'll store the pleasure from each solution here.
    solutions = []
    for subset, subset_b, rowset in zip(subsets, subsets_b, subsets_rowsets):
        #print("subset={}, subset_b={}".format(subset, subset_b))
        equation = Equation(subset, subset_b)
        solution = SolveEquation(equation)
        solutions.append(solution)
        #print("solution={}".format(solution))

        # now check if solution satisfies remaining inequalities too
        # if yes, then store the pleasure value. if not, store lowest possible pleasure value
        is_a_solution = True
        for i in range(n+m+1):
            #if i not in rowset:
            lhs = sum(a * s for a, s in zip(A[i], solution))
            #print("i={}, A[i]={}, lhs={}, b[i]={}".format(i, A[i], lhs, b[i]))
            if lhs > (b[i] + 0.001):
                # implies solution does not satisfy this inequality, so ignore this solution
                is_a_solution = False
                #pleasure.append(sum(s * min_pleasure) for s in solution)
                #pleasure.append(None)
                anst = -1
                pleasure.append( (float("-inf"), anst, solution) )
                break
        if is_a_solution:
            #print("is_a_solution")
            anst = 1
            if (m+n) in rowset:
                anst = 0
            pleasure.append( (sum(s * p for s, p in zip(solution, c)), anst, solution) ) 

    #print("all pleasure values={}".format(pleasure))
    max_pleasure = max(pleasure)
    #max_pleasure_index = pleasure.index(max_pleasure)
    #print("max_pleasure={}, max_pleasure_index={}, m+n={}".format(max_pleasure, max_pleasure_index, m+n))
    #print("max_pleasure={}".format(max_pleasure))
    
    return max_pleasure[1], max_pleasure[2]
    

def find_subsets(A, b, m):
    """Finds all subsets containing m elements, given a set or list A containing at least m elements"""
    n = len(A)
    if m==0:
        # implies return all subsets
        pass
    if m > n:
        # implies return the set itself
        pass

    num_subsets = 2 ** n
    subsets = []
    subsets_b = []
    subsets_rowsets = []
    for i in range(num_subsets):
        subset = []
        subset_b = []
        rowset = set()
        for j in range(n):
            if ((i >> j) & 1) == 1:
                subset.append(A[j])
                subset_b.append(b[j])
                rowset.add(j)
        if (len(subset) == m) or (m == 0):
            subsets.append(subset)
            subsets_b.append(subset_b)
            subsets_rowsets.append(rowset)

    #print("found subsets=")
    #pp(subsets)
    return subsets, subsets_b, subsets_rowsets

def main():
    n, m = list(map(int, stdin.readline().split()))
    A = []
    for i in range(n):
        A += [list(map(int, stdin.readline().split()))]
    b = list(map(int, stdin.readline().split()))
    c = list(map(int, stdin.readline().split())) # this is the pleasure co-efficients

    anst, ansx = solve_diet_problem(n, m, A, b, c)

    if anst == -1:
        print("No solution")
    if anst == 1:
        print("Bounded solution")
        print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
    if anst == 0:
        print("Infinity")


if __name__ == "__main__":
    main()