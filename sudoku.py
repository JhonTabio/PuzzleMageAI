import random

def create_sudoku_board():
    # Initialize a 9x9 Sudoku board with zeros
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Fill the diagonal sub-grids (3x3) with random numbers
    fill_diagonals(board)

    # Solve the Sudoku board to make it a valid puzzle
    solve_sudoku(board)

    # Randomly remove numbers to create a puzzle
    create_puzzle(board)

    return board

def fill_diagonals(board):
    for i in range(0, 9, 3):
        fill_subgrid(board, i, i)

def fill_subgrid(board, row, col):
    nums = list(range(1, 10))
    random.shuffle(nums)

    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums.pop()

def solve_sudoku(board):
    find_empty = find_empty_cell(board)
    if not find_empty:
        return True
    else:
        row, col = find_empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def is_valid(board, num, pos):
    row, col = pos

    # Check row
    if num in board[row]:
        return False

    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check 3x3 sub-grid
    subgrid_row, subgrid_col = row // 3 * 3, col // 3 * 3
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if board[i][j] == num:
                return False

    return True

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def create_puzzle(board):
    # Remove a random number of cells (20-30) to create the puzzle
    num_cells_to_remove = random.randint(20, 30)
    for _ in range(num_cells_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 'X'

def print_sudoku(board):
    for row in board:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    sudoku_board = create_sudoku_board()
    print("Sudoku Board:")
    print_sudoku(sudoku_board)