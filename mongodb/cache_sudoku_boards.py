from pymongo import MongoClient

# Caches a Sudoku board
def cache_sudoku_board(board, solution):
    # MongoDB connection settings
    uri = "ENTER_ATLAS_CONNECTION_STRING_HERE"
    client = MongoClient(uri)

    # MongoDB database and collection information
    db = client["sudoku_db"]
    collection = db["sudoku_cache"]

    # Get solution to board
    solution = 0 # Need to implement

    # Insert the solved Sudoku board into the collection
    inserted_id = collection.insert_one({"sudoku_board": board,
                                         "solution": solution}).inserted_id
    print(f"Solved sudoku board successfully cached into MongoDB with ID: {inserted_id}")

    # Close the MongoDB connection
    client.close()
