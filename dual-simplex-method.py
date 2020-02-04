import numpy as np
import matplotlib.pyplot as plt


# method to calculate the profit
def calculateProfit(table, Z, basic_coeff, total_count):
    P = []
    table = np.transpose(table)
    for i in range(total_count):
        Q = 0
        for j in range(len(basic_coeff)):
            Q += basic_coeff[j] * table[i][j]
        P.append(Z[i] - Q)
    
    return np.array(P)


# method to check optimality condition for simplex method
def optimalCondition(P, choice):
    if choice == 'min':
        for i in P:
            if i < 0:
                return True
        return False
    else:
        for i in P:
            if i > 0:
                return True
        return False
    

# method to perform Gauss-Jordan Elimination on the simplex table
def gauss_jordan_elimination(table, row_index, column_index):
    
    # first converting the coefficient to 1
    table[row_index] = table[row_index]/table[row_index][column_index]

    # eliminating from rest of the constraints
    for i in range(row_index):
        table[i] -= table[row_index] * table[i][column_index]
    
    for i in range(row_index+1, len(table)):
        table[i] -= table[row_index] * table[i][column_index]

    return table


if __name__ == '__main__' :

    '''
    taking input and initializing
    '''

    # taking the objective function as input
    print('Enter the Objective Function Z : ', end='')
    Z = list(map(int, input().split()))
    var_count = len(Z)

    # array for constraints
    inequalities = []
    equalities = []

    # the RHS values/solution column
    B = []

    #initializing the number-of-constraints
    n1, n2 = 0, 0

    # taking inequalities LHS
    print("Enter the number of inequalities : ", end='')
    n1 = int(input())

    if n1 != 0:
        print("Enter LHS of inequalities in less-than form : ")
        for i in range(n1):
            inequalities.append(list(map(int, input().split())))

        # taking inequalities RHS
        print("Enter RHS of inequalties : ")
        for i in range(n1):
            B.append(int(input()))
    
    # taking equalities LHS
    print("Enter the number of equalities : ", end='')
    n2 = int(input())

    if n2 != 0:
        print("Enter the LHS equalities : ")
        for i in range(n2):
            equalities.append(list(map(int ,input().split())))
    
        # taking equalities RHS
        print("Enter the RHS of inequalities : ")
        for i in range(n2):
            B.append(int(input()))

    if n1 == 0 and n2 == 0:
        print("No constraints entered!!")
        exit(0)
    
    equalities = np.array(equalities)
    inequalities = np.array(inequalities)
    B = np.array(B)

    