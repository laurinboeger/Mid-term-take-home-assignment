def main():
    while True:
        #gets the size and elements of the matrix
        matrix = enter_matrix()
        #copies the original matrix to keep it for future calculations
        original_matrix = copy_matrix(matrix)
        #displays the matrix in the terminal to get a better user experience
        display_matrix(matrix, "matrix")
        #checks if the matrix is invertible or not, if not the programm jumps back to the beginning so that the user can type in a new matrix
        if check_rank(matrix):
            break
    #if the check for invertibility passed, the programm calculates an elementary_matrix
    elementary_matrix = calc_elementary_matrix(original_matrix)
    #creates an augmented_matrix (original_matrix + elementary_matrix)
    augmented_matrix = calc_augmented_matrix(original_matrix, elementary_matrix)
    #claculate the inverse 
    calculate_inverse(augmented_matrix, elementary_matrix)
    #seperates the elementary matrix from the new inverse matrix and returns only the inverse matrix
    inverse_matrix = create_inverse(augmented_matrix)
    #user can decide wether he only wants to compute the inverse or wants to solve the system of linear equations Ax = b
    if choice():
        #user types in a right hand side b
        b = enter_b(original_matrix)
        #solves the system for b and returns the solution
        solutions = calc_b(inverse_matrix, b)
        #displays the inverse matrix 
        display_matrix(inverse_matrix, "inverse matrix")
        #displays the set of solutions for x
        display_matrix(solutions, "set of solutions for x")
        
    else:
        #only displays the inverse matrix
        display_matrix(inverse_matrix, "inverse matrix")

#user can decide wether he only wants to compute the inverse or wants to solve the system of linear equations Ax = b
def choice():
    while True:
        choice = input("Do you want to solve the matrix for some b? (yes/no): ")
        if choice == "yes":
            return True
        elif choice == "no": 
            return False

#user types in a right hand side b
def enter_b(original_matrix):
    b = []
    #loops through every row the the matrix
    for index in range(len(original_matrix)):
        while True:
            try:
                #asks for an element of b for each row
                element = int(input(f"Enter b{index+1}: "))
                b.append(element)
                break
            except ValueError:
                print("Invalid Input!")
                pass
    return b

#solves the system for b and returns the solution
def calc_b(inverse_matrix, b):
    solution = []
    for row in range(len(inverse_matrix)):
        x = 0
        for column in range(len(inverse_matrix)):
            #mulitplies every element of the row by the corresponding b of the right hand side and adds up the result of the row in x
            x += inverse_matrix[row][column]*b[column]
        #x is stored in solution
        solution.append(x)
    return solution

#checks the rank of the matrix to decide wether it is invertible or not
def check_rank(matrix):
    upper_triangular_matrix = copy_matrix(matrix)

    #claculate upper triangular form to get the rank of the matrix

    #loop through each row 
    for row_1 in upper_triangular_matrix:
        #save the index of the current row
        row_1_index = upper_triangular_matrix.index(row_1)
        #loops through each element of the row
        for element in row_1:
            #goes to the first non zero element in row
            if element != 0:
                #saves the index of that element
                element_index = row_1.index(element)
                #if element is not one, do elemetary row operation 3 which mulitplies the row by a value to turn the pivot element to 1 
                if element != 1:
                    r3(upper_triangular_matrix, row_1_index,  element)
                pivot = row_1[element_index]
                #eleminate all entries below the pivot element by looping through each row below and doing the elementary row operation 1 which substracts a multiple of the current row from the row below 
                for row_2 in upper_triangular_matrix[row_1_index+1:]:
                    r1(upper_triangular_matrix, row_1, row_2, pivot)

    #count the rank of the matrix
    rank = 0                
    for row in upper_triangular_matrix:
        for element in row:
            if element == 1:
                rank += 1
                break
    
    #if the rank does not equal the number of rows, there are depentend vectors in the matrix which makes it singular and not invertible 
    if rank != len(upper_triangular_matrix):
        print("The matrix is not invertible!")
        return False
    else: 
        return True

def copy_matrix(matrix):
    copied_matrix = []
    #loops through each row
    for row in matrix:
        new_row = []
        #copies each element of each row 
        for element in row:
            new_row.append(element)
        copied_matrix.append(new_row)
    return copied_matrix

#user enters the matrix size and each element of 
def enter_matrix():
    #enter the size of the matrix and repeat as long as the input is invalid 
    while True: 
        try:
            n = int(input("Enter the size of the square matrix: "))
            if n not in [0, 1]:
                break
            print("Invalid Input!")
        except ValueError:
            print("Invalid Input!")

    matrix = []

    print("\nEnter the elements of the matrix:")

    #loops through each row of the matrix
    for row in range(n):
        row_elements = []
        #asks for a value for each element of the row 
        for column in range(n):
            while True:
                try:
                    row_elements.append(float(input(f"Enter the element of row {row+1} and column {column+1}: ")))
                    break
                except ValueError:
                    print("Invalid Input!")
        matrix.append(row_elements)

    return matrix

def display_matrix(matrix, text):
    print(f"\nThis is your {text}: \n")
    try:
        for row in matrix:
            #displays the solution for x
            float(row)
            print(f"x{matrix.index(row)+1} = {round(row, 3)}")
    except TypeError:
        #displays the matrix
        for row in matrix:
            for element in row:
                print(f"{round(element, 3)}  ", end="")
            print("\n")

#seperates the inverse from the elementary matrix 
def create_inverse(augmented_matrix):
    inverse_matrix = []
    for row in augmented_matrix:
        row_new = row[len(augmented_matrix):]
        inverse_matrix.append(row_new)
    return inverse_matrix

def calc_elementary_matrix(matrix):
    n = len(matrix)
    elementary_matrix = []
    row_elements = []

    #create a row with n 0s
    for element in range(n):
        row_elements.append(0)

    #implement the 1s in diagonal
    for row in range(n):
        updated_row_elements = list(row_elements)
        updated_row_elements[row] = 1
        elementary_matrix.append(updated_row_elements)

    return elementary_matrix


def calculate_inverse(augmented_matrix, elementary_matrix): 

    #claculate upper triangular form
    #loop through each row
    for row_1 in augmented_matrix:
        #save the index of the current row
        row_1_index = augmented_matrix.index(row_1)
        #loops through each element of the row
        for element in row_1[:len(elementary_matrix)]:
            #goes to the first non zero element in row 
            if element != 0:
                #saves the index of that element    
                element_index = row_1.index(element)
                #if element is not one, do elemetary row operation 3 which mulitplies the row by a value to turn the pivot element to 1 
                if element != 1:
                    r3(augmented_matrix, row_1_index,  element)
                pivot = row_1[element_index]
                #eleminate all entries below the pivot element by looping through each row below and doing the elementary row operation 1 which substracts a multiple of the current row from the row below 
                for row_2 in augmented_matrix[row_1_index+1:]:
                    r1(augmented_matrix, row_1, row_2, pivot)
                break
    
    #calculate row reduced form
    for row_1 in augmented_matrix:
        #save the index of the current row
        row_1_index = augmented_matrix.index(row_1)
        #loops through each element of the row
        for element in row_1:
            #goes to the pivot of the row 
            if element == 1:
                pivot = element
                #eleminate all entries above the pivot element by looping through each row above and doing the elementary row operation 1 which substracts a multiple of the current row from the row above 
                for row_2 in augmented_matrix[:row_1_index]:
                    r1(augmented_matrix, row_1, row_2, pivot)
                break

#calculates an augmented matrix by passing in the original matrix and the elementary_matrix
#returns augmented matrix which is used to calculate the inverse
def calc_augmented_matrix(matrix, elementary_matrix):
    rows = len(matrix)
    augmented_matrix = []

    for index in range(rows):
        augmented_row = matrix[index] + elementary_matrix[index]
        augmented_matrix.append(augmented_row)

    return augmented_matrix

#the following three functions are doing elementary row operations

#add a multiple of r1 to r2
def r1(matrix, row_1, row_2, pivot):
    row_2_index = matrix.index(row_2)
    pivot_index = row_1.index(pivot)

    if row_2[pivot_index] != 0:
        mulitplicator = 1/get_multiplicator(row_2[pivot_index])
        for index in range(len(row_1)):
            element = row_2[index] - mulitplicator*row_1[index]
            #element = round(element, 3)
            row_2[index] = element
        matrix[row_2_index] = row_2

#interchange two rows
def r2(matrix, row_j, row_i):
    row_j_index = matrix.index(row_j)
    row_i_index = matrix.index(row_i)
    matrix[row_j_index] = matrix[row_i_index]
    matrix[row_i_index] = row_j

#multiply a row by a non-zero scalar to get the pivot to 1
def r3(matrix, row_1_index, pivot):
    multiplicator = get_multiplicator(pivot)
    for column_index in range(len(matrix[row_1_index])):
        element = matrix[row_1_index][column_index]*multiplicator
        #matrix[row_1_index][column_index] = round(element, 3)
        matrix[row_1_index][column_index] = element

def get_multiplicator(pivot):
    return 1/pivot

main()