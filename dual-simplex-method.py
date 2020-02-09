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


# method to check optimality condition for dual-simplex method
def optimalCondition(table):
    B = table[:,-1]
    for i in B:
        if i[0] < 0:
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
    B = np.transpose(B)


    '''
    converting in standard form
    '''

    # adding spaces for extra variables
    if n1 != 0:
        equalities = np.pad(equalities, ((0,0), (0,n1+n2)), 'constant', constant_values=0)
    if n2 != 0:        
        inequalities = np.pad(inequalities, ((0,0), (0,n1+n2)), 'constant', constant_values=0)
    Z = np.pad(Z, (0, n1+n2), 'constant', constant_values=0)

    # generating the simplex table
    if n1 == 0:
        table = equalities
    elif n2 == 0:
        table = inequalities
    else:
        table = np.append(inequalities, equalities, axis=0)
    B = np.reshape(B, (n1+n2, 1))
    table = np.append(table, B, axis=1)
    table = table.astype('float')

    # finally adding extra (slack) variables
    for i in range(n1 + n2):
        table[i][var_count + i] = 1
    
    '''
    doing optimization
    '''

    # array to keep track of basic variables, initially all slack variables
    basic_coeff = np.pad(np.zeros(var_count),(0,n1+n2),'constant',constant_values=1)

    # applying dual-simplex method recursively
    while(optimalCondition(table)):

        # getting the leaving variable
        B = table[:, -1].flatten()
        row_index = np.argmin(B)

        # calculating profit
        P = calculateProfit(table, Z, basic_coeff, var_count+n1+n2)

        # getting the entering variable
        col_index = -1
        ratio = np.devide(P, table[row_index])
        min_ratio = np.max(ratio)
        for i in range(n1+n2+var_count):
            if ratio[i] > 0 and ratio[i] < min_ratio:
                min_ratio = ratio[i]
                col_index = i

        if col_index == -1:
            print("No Solutions!!")
            exit(0)

        # performing the gauss jordan elimination
        table = gauss_jordan_elimination(table, row_index, col_index)

        # updating the basic coefficients
        basic_coeff[row_index] = col_index

    print(table)
    print(basic_coeff)