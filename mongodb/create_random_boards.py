from pymongo import MongoClient
from random import sample

SUDOKU_ENTRIES = 10

# MongoDB connection settings
uri = "mongodb+srv://matthewlabrada:Hackathong@cluster0.hvtyobg.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
client = MongoClient(uri)

# Define a function to create a Sudoku board with 0 for empty spots
def create_sudoku_board():
    # Initialize an empty 9x9 Sudoku board
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Generate a random Sudoku puzzle
    for _ in range(9):
        row = sample(range(1, 10), 9)
        while not all(row):
            row = sample(range(1, 10), 9)
        board[_] = row

    return board

# MongoDB database and collection information
db = client["sudoku_db"]
collection = db["sudoku_puzzles"]

# Create a list of Sudoku boards
boards = [create_sudoku_board() for _ in range(SUDOKU_ENTRIES)]

# Insert the Sudoku boards into the collection
for i in range(SUDOKU_ENTRIES):
    inserted_id = collection.insert_one({"sudoku_board": boards[i]}).inserted_id
    print(f"Sudoku board successfully inserted into MongoDB with ID: {inserted_id}")

# Close the MongoDB connection
client.close()