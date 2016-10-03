# python3
from sys import stdin
from pprint import pprint as pp
    
def allocate_ads(n, m, A, b, c):  
    # Write your code here
    # we'll follow the logic as outlined in http://www.zweigmedia.com/RealWorld/tutorialsf4/frames4_3.html 
    #   and summarised in http://www.zweigmedia.com/RealWorld/tutorialsf4/stdsimplex.html
    
    # constants
    max_cols = n + m + 1
    new_cols = n + 1

    # first create the tableau and answer vector
    # n inequalities, m variables, 
    #   so tableau will have n + 1 rows, and n + m + 1 cols
    #   ans vector will have n + 1 elements
    # we'll expand A into the tableau, and expand b to be the answer vector
    
    #print("A and c before:")
    #pp(A)
    #pp(c)
    orig_A = A.copy() # note: this is not a deep copy, so the rows are still pointers to A
    orig_b = b.copy()

    # step2: we'll add the last row to A
    last_row = [ci * (-1) for ci in c]
    A.append(last_row)
    for i, row in enumerate(A):
        # here we are adding new columns to A
        remaining_cols = new_cols - i - 1
        new_row = row + [0] * i + [1] + [0] * remaining_cols
        #print("new_row", new_row)
        A[i] = new_row

    # now expanding vector b
    b.append(0)

    # now ensure all b elements are > 0
    for i, ans in enumerate(b):
        if ans < 0:
            new_row = [(-1)*aij for aij in A[i]]
            A[i] = new_row
            b[i] = (-1) * ans

    #print("A after:")
    #pp(A)
    #pp(b)

    # go through phase1 first
    phase1_not_done = True
    orig_tableau = []
    while phase1_not_done:
        # get basic solution
        solution, AT = get_basic_solution(A, b)
        # check all vars are >= 0
        if all(x >= 0 for x in solution[:n + 1]):
            phase1_not_done = False
            #print("basic solution={} is in feasible region.".format(solution))
            break

        # i am here, implies we have at least one non-negative var
        # select pivot column
        pivot_column_id, starred_row_ids = get_starred_pivot_col(A, AT, solution)

        # select pivot element
        test_ratios = [] # stores the ratio on answer element and candidate element
        #for i, row in enumerate(A):
        for i in range(n): # i.e. ignoring last row of A for calculating test row
            row = A[i]
            candidate_element = row[pivot_column_id]
            if candidate_element > 0:
                is_not_starred = 1
                if i in starred_row_ids:
                    is_not_starred = 0
                test_ratios.append( (b[i]/candidate_element, is_not_starred, i) ) 
                # the above line ensures that in case more than one row has the same test ratio, we'll always select a starred row over a non-starred row

        if len(test_ratios) == 0:
            # implies infinite solution
            #print("phase1 no test ratios! pivot_column_id={}", pivot_column_id)
            #print("A={}".format(A))
            return 1, [0] * m

        _, is_not_starred, pivot_row_id = min(test_ratios)
        pivot = A[pivot_row_id][pivot_column_id]
        #print("pivot_row_id={}, pivot={}".format(pivot_row_id, pivot))

        # clear pivot column
        A, b = clear_pivot_column(A, b, pivot_row_id, pivot_column_id)

        #print("new tableau generated in phase1")
        #pp(A)
        #pp(b)

        if A == orig_tableau:
            # implies we are in an infinite loop
            #print("infinite loop in phase1!")
            break
        orig_tableau = A.copy()

    solution, AT = get_basic_solution(A, b)
    if any(x < 0 for x in solution[:n + 1]):
        #print("one of solution elements is negative", solution)
        solution_flag = -1
        return [solution_flag, solution[0:m]]


    # now that we are done with phase1, let's move to steps 3-5
    # repeat the next 3 steps till we find a solution. this is step6
    not_done = True
    orig_tableau = []
    while not_done:
        # step3: select pivot column
        last_row = A[-1]
        smallest_number = min(last_row)
        if smallest_number >= 0:
            #print("we are done!")
            not_done = False
            break

        #print("A={}, last row={}, smallest_number={}".format(A, last_row, smallest_number))
        pivot_column_ids = [i for i, x in enumerate(last_row) if x == smallest_number]
        #print("pivot_column_ids={}".format(pivot_column_ids))
        num_pivot_columns = len(pivot_column_ids)
        pivot_row_not_found = True
        p_i = 0
        while pivot_row_not_found and p_i < num_pivot_columns:
            
            pivot_column_id = pivot_column_ids[p_i]
            p_i += 1
            #print("pivot_column={}, new i={}".format(pivot_column_id, i))

            # step4: select pivot element
            test_ratios = [] # stores the ratio on answer element and candidate element
            #for i, row in enumerate(A):
            for i in range(n): # i.e. ignoring last row of A for calculating test row
                row = A[i]
                candidate_element = row[pivot_column_id]
                if candidate_element > 0:
                    test_ratios.append( (b[i]/candidate_element, i) )

            if len(test_ratios) > 0:
                _, pivot_row_id = min(test_ratios)
                pivot_row_not_found = False
                break
                # implies infinite solution
                #print("no test ratios! pivot_column_id={}", pivot_column_id)
                #print("A={}".format(A))
            
        if pivot_row_not_found:
            #print("searched all possible pivot_column_ids={}. No column had test_ratios. so, infinite solutions!".format(pivot_column_ids))
            return 1, [0] * m

        pivot = A[pivot_row_id][pivot_column_id]
        #print("pivot_row_id={}, pivot={}".format(pivot_row_id, pivot))

        # step5: clear the pivot column to generate next tableau
        A, b = clear_pivot_column(A, b, pivot_row_id, pivot_column_id)

        #print("new tableau generated")
        #pp(A)
        #pp(b)

        if A == orig_tableau:
            # implies we are in an infinite loop
            #print("infinite loop!")
            break
        orig_tableau = A.copy()
        

    # step7: return the basic solution
    # find all cleared columns. I am only interested in the first m rows
    solution, AT = get_basic_solution(A, b)
    
    # before we return this solution, we need to check if it actually fits
    #print("candidate_solution={}".format(solution))
    solution_flag = 0 # implies one solution exists
    
    if sum(AT[-1]) == 0:
        # implies last column of A has all 0, so implies objective function is unbounded
        solution_flag = 1 # i.e. Infinity

    if any(x < 0 for x in solution[:n + 1]):
        #print("one of solution elements is negative", solution)
        solution_flag = -1

    for i in range(n):
        lhs = sum(a * s for a, s in zip(orig_A[i], solution))
        if lhs > (orig_b[i] + 0.001):
            # implies solution does not satisfy this inequality, so ignore this solution
            #print("lhs={}, orig_A[i]={}, orig_b[i]={}, i={}".format(lhs, orig_A[i], orig_b[i], i))
            solution_flag = -1
            break

    return [solution_flag, solution[0:m]]


def get_basic_solution(A, b):
    #AT = []
    #for j in range(m):
    #    col = []
    #    for row in A:
    #        col.append(row[j])
    #    AT.append(col)

    AT = list(map(list, zip(*A)))
    num_cols = len(AT)

    solution = [0] * num_cols
    for j, col in enumerate(AT):
        non_zero_elements = [ (i,element) for i, element in enumerate(col) if element != 0] # sum([1 for element in col if element == 0])
        if len(non_zero_elements) == 1: # implies this column is cleared
            solution[j] = b[non_zero_elements[0][0]] / non_zero_elements[0][1]

    return solution, AT


def clear_pivot_column(A, b, pivot_row_id, pivot_column_id):
    """Updates A and b, such that the entries in pivot column (other than the pivot itself) are zeroed out."""
    pivot_row = A[pivot_row_id]
    pivot = pivot_row[pivot_column_id]
    for i, row in enumerate(A):
        if i == pivot_row_id:
            continue
        multiplier = row[pivot_column_id]
        if multiplier:
            new_row = [ri*pivot - pri*multiplier for ri, pri in zip(row, pivot_row)]
            b[i] = b[i] * pivot - b[pivot_row_id] * multiplier
        else:
            new_row = row.copy()
        A[i] = new_row
        

    return A, b


def get_starred_pivot_col(A, AT, solution):
    starred_row_ids = []
    #print("phase1 basic solution={}".format(solution))
    for i, x in enumerate(solution):
        if x < 0:
            starred_row_id, _ = [(j, x) for j, x in enumerate(AT[i]) if x != 0][0]
            starred_row_ids.append(starred_row_id)
            #print("var_value={}, col_id={}, starred_row_id={}".format(x, i, starred_row_id))
    starred_row = A[starred_row_ids[0]]
    max_x = max(starred_row)
    #if max_x < 0:
        #print("max value in starred row is non-negative! max={}, starred_row_id={}, starred_row={}".format(max_x, starred_row_id, starred_row))
    pivot_col_id = starred_row.index(max_x)
    #print("pivot_col_id={}".format(pivot_col_id))
    return pivot_col_id, starred_row_ids

    

        

def main():
    n, m = list(map(int, stdin.readline().split()))
    A = []
    for i in range(n):
        A += [list(map(int, stdin.readline().split()))]
    b = list(map(int, stdin.readline().split()))
    c = list(map(int, stdin.readline().split()))

    anst, ansx = allocate_ads(n, m, A, b, c)

    if anst == -1:
        print("No solution")
    if anst == 0:  
        print("Bounded solution")
        print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
    if anst == 1:
        print("Infinity")
            
if __name__ == "__main__":
    main()