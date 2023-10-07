import cv2
import torch
import numpy as np
from boards.classifier.classifier import load_model
from time import time
from itertools import product

class Sudoku:
    def __init__(self, img):
        self.board = img
        self.size, (self.width, self.height) = self.get_dim()
        if self.size == None:
            return
        self.matrix = self.get_matrix()
        print(self.matrix,"\n")
        self.rows, self.cols = self.init_row_col()
        self.solution = []
        self.solve_sudoku(self.matrix.copy())

        if len(self.solution) == 0:
            print("No solution")
            return
        print("SOLVED!\n", self.solution, "SOLVED!\n")

    def get_dim(self):
        blur = cv2.GaussianBlur(self.board, (15, 15), 0) # Apply a gaussian blur 
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] # Applying threshold to display thick borders

        # Mask the border of the puzzle
        thresh[0:10, :] = 255 # Top
        thresh[:, 0:10] = 255 # Left
        thresh[-10:, :] = 255 # Bottom
        thresh[:, -10:] = 255 # Right
        thresh = np.bitwise_not(thresh) / 255 # Inverse the image

        vertical_sum = np.sum(np.round(thresh, 0), axis=0)
        horizontal_sum = np.sum(np.round(thresh, 0), axis=1)

        min_height = int(0.66 * self.board.shape[0])
        min_width = int(0.66 * self.board.shape[1])
        
        vertical_bool = vertical_sum > min_height
        horizontal_bool = horizontal_sum > min_width

        v_lines = 1
        for i in range(1, len(vertical_bool)): # Detect total num of '01' patterns vertically
            v_lines += (~ vertical_bool[i - 1]) & vertical_bool[i]

        h_lines = 1
        for i in range(1, len(horizontal_bool)): # Detect total num of '01' patterns vertically
            h_lines += (~ horizontal_bool[i - 1]) & horizontal_bool[i]

        board_size = v_lines * h_lines
        
        if board_size not in (4, 6, 8, 9): # We only want to detect size of {4, 6, 8, 9}
            # raise exception for improper grid size
            #raise RuntimeError("Improper Grid Size, expected in {{4,6,8,9}}, got {}".format(board_size))
            return None, (None, None)

        # return the game dimensions
        return board_size, (v_lines, h_lines)

    def preprocess_digit(self, digit_img):
        """
            Helper method to clear borders and darken the digit of an individual cell of the puzzle.
        """

        digit_img = cv2.resize(digit_img, (112, 112), # Expand the image
                               interpolation=cv2.INTER_CUBIC)
        digit_img = cv2.GaussianBlur(digit_img, (5, 5), 0) # Apply Gaussian blur
        digit_img = cv2.threshold(digit_img, 135, 255, cv2.THRESH_TRUNC)[1] # Apply a threshold to the image
        digit_img[digit_img >= 110] = 255

        # Mask the surrounding border of the cell
        digit_img[0:10, :] = 255 # Top
        digit_img[:, 0:10] = 255 # Left
        digit_img[-10:, :] = 255 # Bottom
        digit_img[:, -10:] = 255 # Right

        digit_img = cv2.resize(digit_img, (28, 28),
                               interpolation=cv2.INTER_CUBIC)

        if np.sum(np.bitwise_not(digit_img)) < 255 * 10:
            return None

        # Scale pixels with value less than 150 to 3/4th the value
        pos = digit_img < 150
        digit_img[pos] = 3 * (digit_img[pos] // 4)
        # Double the values of other pixels
        digit_img[np.bitwise_not(pos)] = 2 * digit_img[np.bitwise_not(pos)]

        return digit_img

    def get_matrix(self):
        """Returns the puzzle matrix from the image"""

        matrix = np.zeros((self.size, self.size), dtype=int) # Initialize a matrix with 0
        model = load_model("assets/char74k-cnn.pth") # Load the lassifier model
        model.eval()

        cell_h, cell_w = np.array(self.board.shape) / self.size # Get the width and height of each cell

        for i in range(self.size):
            y_start = int(i * cell_h)
            y_end = int((i + 1) * cell_h)

            for j in range(self.size):
                x_start = int(j * cell_w)
                x_end = int((j + 1) * cell_w)

                digit_img = self.board[y_start:y_end, x_start:x_end].copy()
                digit_img = self.preprocess_digit(digit_img)
                
                if digit_img is None:
                    matrix[i, j] = 0
                    continue

                digit_img = digit_img / 255 # Map the value of the pixel between 0 - 1
                digit_img = np.array(digit_img).reshape((1, 1, 28, 28))
                digit_img_tensor = torch.tensor(digit_img, dtype=torch.float)
                digit_img_out = np.array(model(digit_img_tensor).detach(), dtype=np.float32).flatten()
                element = int(np.argmax(digit_img_out))

                """
                    Sanity Check: This will ensure that an impossible puzzle does not get loaded because
                              2 cells in a row or in a column or in a sub grid have the same value.
                              If they have same values, then the one with higher prediction score for 
                              the specific label gets the value of the element and the other variable 
                              chooses the value with the second highest prediction score.
                """
                
                # Values for a subgrid
                sub_r, sub_c = i - (i % self.width), j - (j % self.height)
                sub_matrix = matrix[sub_r:sub_r + self.width, sub_c:sub_c + self.height]

                if element in matrix[i, :]:
                    x = i
                    y = list(matrix[i, :]).index(element)

                elif element in matrix[:, j]:
                    x = i
                    y = list(matrix[:, j]).index(element)

                elif element in sub_matrix:
                    pos = list(sub_matrix.flatten()).index(element)
                    x = sub_r + pos // self.width
                    y = sub_c + pos % self.height

                else:
                    matrix[i, j] = element
                    continue

                duplicate = np.copy(self.board[int(x * cell_h):int((x + 1) * cell_h),
                                    int(y * cell_w):int((y + 1) * cell_w)])
                duplicate = self.preprocess_digit(duplicate)
                if duplicate is None:
                    matrix[i, j] = element
                    matrix[x, y] = 0
                    continue

                # map the image pixel values between 0-1
                duplicate = duplicate / 255
                # reshape the numpy array
                duplicate = np.array(duplicate).reshape((1, 1, 28, 28))
                # convert the image to tensor
                duplicate_tensor = torch.tensor(duplicate, dtype=torch.float)
                # get the model prediction
                duplicate_out = np.array(model(duplicate_tensor).detach(), dtype=np.float32).flatten()

                # if prediction score of current element is more
                if digit_img_out[element] > duplicate_out[element]:
                    # set the current index with the current element value
                    matrix[i, j] = element
                    # assign the index in duplicate output with negative infinity
                    duplicate_out[element] = np.NINF
                    # set the duplicate index with the new highest of its respective output
                    matrix[x, y] = int(np.argmax(duplicate_out))

                # if prediction score of duplicate element is more
                else:
                    # set the duplicate index with the current element value
                    matrix[x, y] = element
                    # assign the index in current output with negative infinity
                    digit_img_out[element] = np.NINF
                    # set the current index with the new highest of its respective output
                    matrix[i, j] = int(np.argmax(digit_img_out))

        # return the matrix
        return matrix

    def init_row_col(self):
        """Initialize the rows and columns"""

        # rows for the exact cover problem
        rows = dict()
        for (i, j, n) in product(range(self.size), range(self.size), range(1, self.size + 1)):
            b = (i // self.width) * self.width + (j // self.height)
            rows[(i, j, n)] = [("row-col", (i, j)), ("row-num", (i, n)),
                               ("col-num", (j, n)), ("box-num", (b, n))]

        # cols for the exact cover problem
        columns = dict()
        for (i, j) in product(range(self.size), range(self.size)):
            columns[("row-col", (i, j))] = set()
            columns[("row-num", (i, j + 1))] = set()
            columns[("col-num", (i, j + 1))] = set()
            columns[("box-num", (i, j + 1))] = set()

        for pos, list_value in rows.items():
            for value in list_value:
                columns[value].add(pos)

        return rows, columns

    def cover_column(self, rows: dict, cols: dict, values):
        """Cover or Hide a column in the exact cover problem"""

        # empty list of removed columns yet
        removed_columns = []
        # for each row in selected column
        for row in rows[values]:
            # for each column in current row
            for row_col in cols[row]:
                # for each row of this column
                for col_row_col in rows[row_col]:
                    # if this row is not the initial row
                    if col_row_col != row:
                        # remove item from set
                        cols[col_row_col].remove(row_col)

            removed_columns.append(cols.pop(row))
        return removed_columns

    def uncover_column(self, rows: dict, cols: dict, values, removed_columns: list):
        """Uncover or Unhide a column in the exact cover problem"""

        # since removed columns is stack, work in reverse order of list
        for row in reversed(rows[values]):
            # pop the last column removed
            cols[row] = removed_columns.pop()
            # for row in col of previously deleted row
            for row_col in cols[row]:
                # for col in the above row
                for col_row_col in rows[row_col]:
                    # if this row is not the initial row
                    if col_row_col != row:
                        # add item back to set
                        cols[col_row_col].add(row_col)

    def get_solution(self):
        """ Returns list of possible solutios for the Problem"""

        # initialize rows and columns
        rows, cols = self.init_row_cols()
        # initialize list of solutions
        solutions = []

        # for each row in puzzle matrix
        for i in range(self.size):
            # for each column 
            for j in range(self.size):
                # if the value is not zero
                if self.matrix[i, j] != 0:
                    # remove associated values from the solution space
                    self.cover_column(rows, cols, (i, j, self.matrix[i, j]))

        # iterate through the solutions
        for solution in self.solve(rows, cols, []):
            # iterate through coordinates and there values
            for (i, j, element) in solution:
                # assign the values to the respective elements
                self.matrix[i, j] = element
            # append the solution to the list of solutions
            solutions.append(self.matrix)
            # reset the matrix to the initial matrix
            self.matrix = self.init_matrix.copy()
        # return the list of solutions
        return solutions

    def element_possible(self, matrix: np.ndarray, box_row: int, box_col: int, i: int, j: int):
        """Helper method to check if a value in the matrix is valid"""

        # backup the element in place
        element = matrix[i, j].copy()
        # reassign as 0
        matrix[i, j] = 0
        # find the sub grid
        sub_r, sub_c = i - i % box_row, j - j % box_col

        not_found = True
        # if element exists in the same row or the same column or the same sub grid
        if element in matrix[i, :] or \
                element in matrix[:, j] or \
                element in matrix[sub_r:sub_r + box_row, sub_c:sub_c + box_col]:
            not_found = False

        # reassign the backup value
        matrix[i, j] = element
        # return the status variable
        return not_found

    def solve(self, rows: dict, cols: dict, partial_solution: list):
        # if the cols is empty list
        if not cols:
            # yield the part of the solution
            yield list(partial_solution)
        else:
            # select column with min links
            selected_col = min(cols, key=lambda value: len(cols[value]))
            # for each of the value in the selected link
            for values in list(cols[selected_col]):
                # add it to the partial solution considered
                partial_solution.append(values)
                # cover or hide associated links
                removed_cols = self.cover_column(rows, cols, values)
                # recursive call with the values left to cover
                for solution in self.solve(rows, cols, partial_solution):
                    # yield the solution
                    yield solution
                # uncover or unhide associated links
                self.uncover_column(rows, cols, values, removed_cols)
                # remove them from the part of the solution considered
                partial_solution.pop()
    
    def solve_sudoku_old(self):
        start = time()

        try:
            # get solution_list from the class
            solution_list = self.get_solution()
            # get shape of the matrix
            rows, cols = matrix.shape
            # iterate through all the solutions
            for sol_num, solution in enumerate(solution_list):
                print("Solution Number {} -\n".format(sol_num + 1))
                # iterate through rows
                for i in range(rows):
                    # if sub grid rows are over
                    if i % num_rows_sub_grid == 0 and i != 0:
                        print('-' * (2 * (cols + num_rows_sub_grid - 1)))
                    # iterate through columns
                    for j in range(cols):
                        # if sub grid columns are over
                        if j % num_cols_sub_grid == 0 and j != 0:
                            print(end=' | ')
                        else:
                            print(end=' ')
                        # print solution element
                        print(solution[i, j], end='')
                    # end row
                    print()
                print("\n")
            # time taken to solve
            print("\nSolved in {} s".format(round(time() - start, 4)))
            return solution_list
        # Key Value Error raised if solution not possible
        except Exception:
            print("Solution does not exist, try with a different puzzle")

    def solve_sudoku(self, board):
        # Find an empty cell in the Sudoku board
        empty_cell = self.find_empty_cell(board)
    
        # If there are no empty cells, the Sudoku is solved
        if not empty_cell:
            self.solution = board
            return True
    
        row, col = empty_cell
    
        # Try placing numbers from 1 to 9 in the empty cell
        for num in range(1, 10):
            if self.is_valid_move(board, num, (row, col)):
                board[row][col] = num
            
                # Recursively try to solve the Sudoku
                if self.solve_sudoku(board):
                    return True
            
                # If the current placement leads to an invalid solution, backtrack
                board[row][col] = 0
    
        # No solution found for the current state
        return False

    def find_empty_cell(self, board):
        # Find the first empty cell (cell with 0)
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid_move(self, board, num, position):
        # Check if the number is valid in the current position (row, column, and box)
        row, col = position
    
        # Check row
        if num in board[row]:
            return False
    
        # Check column
        if num in [board[i][col] for i in range(self.height)]:
            return False
    
        # Check 3x3 box
        box_row, box_col = row // 3 * 3, col // 3 * 3
        if num in [board[i][j] for i in range(box_row, box_row + 3) for j in range(box_col, box_col + 3)]:
            return False
    
        return True

