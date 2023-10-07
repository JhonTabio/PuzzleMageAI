import random

def create_sudoku_board():
    # Initialize a 9x9 Sudoku board with zeros
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Fill the diagonal sub-grids (3x3) with random numbers
    fill_diagonals(board)

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

def create_puzzle(board):
    # Remove a random number of cells (20-30) to create the puzzle
    num_cells_to_remove = random.randint(20, 30)
    for _ in range(num_cells_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

def print_sudoku(board):
    for row in board:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    sudoku_board = create_sudoku_board()
    print("Sudoku Board:")
    print_sudoku(sudoku_board)
