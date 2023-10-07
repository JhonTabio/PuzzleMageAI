from pymongo import MongoClient
from random import sample

# MongoDB connection settings
uri = "mongodb+srv://matthewlabrada:Hackathong@cluster0.hvtyobg.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
client = MongoClient(uri)

# Define a function to create a Sudoku board with "X" for empty spots
def create_sudoku_board():
    # Initialize an empty 9x9 Sudoku board
    board = [["X" for _ in range(9)] for _ in range(9)]

    # Generate a random Sudoku puzzle
    for _ in range(9):
        row = sample(range(1, 10), 9)
        while not all(row):
            row = sample(range(1, 10), 9)
        board[_] = row

    return board

# Create a Sudoku board
sudoku_board = create_sudoku_board()

# MongoDB database and collection information
db = client["sudoku_db"]
collection = db["sudoku_puzzles"]

# Insert the Sudoku board into the collection
inserted_id = collection.insert_one({"sudoku_board": sudoku_board}).inserted_id

print(f"Sudoku board successfully inserted into MongoDB with ID: {inserted_id}")

# Close the MongoDB connection
client.close()