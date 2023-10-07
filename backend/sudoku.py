import numpy as np

from itertools import product


class Solver:
    def __init__(self):
        pass

    def solve_sudoku(self, size, grid):
        R, C = size
        N = R * C
        X = (
            [("rc", rc) for rc in product(range(N), range(N))]
            + [("rn", rn) for rn in product(range(N), range(1, N + 1))]
            + [("cn", cn) for cn in product(range(N), range(1, N + 1))]
            + [("bn", bn) for bn in product(range(N), range(1, N + 1))]
        )
        Y = dict()
        for r, c, n in product(range(N), range(N), range(1, N + 1)):
            b = (r // R) * R + (c // C)
            Y[(r, c, n)] = [
                ("rc", (r, c)),
                ("rn", (r, n)),
                ("cn", (c, n)),
                ("bn", (b, n)),
            ]
        X, Y = self.exact_cover(X, Y)
        for i, row in enumerate(grid):
            for j, n in enumerate(row):
                if n:
                    self.select(X, Y, (i, j, n))
        for solution in self.solve(X, Y, []):
            for (r, c, n) in solution:
                grid[r][c] = n
            yield grid

    def exact_cover(self, X, Y):
        X = {j: set() for j in X}
        for i, row in Y.items():
            for j in row:
                X[j].add(i)
        return X, Y

    def solve(self, X, Y, solution):
        if not X:
            yield list(solution)
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = self.select(X, Y, r)
                for s in self.solve(X, Y, solution):
                    yield s
                self.deselect(X, Y, r, cols)
                solution.pop()

    def select(self, X, Y, r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    def deselect(self, X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

    def solve_wrapper(self, arr):
        try:
            ans = np.array(
                list(self.solve_sudoku(size=(3, 3), grid=arr))[0], dtype=np.uint8
            )
            return ans
        except:
            return None


class Validator:
    def __init__(self):
        pass

    def not_in_row(self, arr, row):

        st = set()
        for i in range(0, 9):
            if arr[row][i] in st:
                return False
            if arr[row][i] != 0:
                st.add(arr[row][i])
        return True

    def not_in_col(self, arr, col):

        st = set()
        for i in range(0, 9):
            if arr[i][col] in st:
                return False
            if arr[i][col] != 0:
                st.add(arr[i][col])
        return True

    def not_in_box(self, arr, startRow, startCol):

        st = set()
        for row in range(0, 3):
            for col in range(0, 3):
                curr = arr[row + startRow][col + startCol]
                if curr in st:
                    return False
                if curr != 0:
                    st.add(curr)
        return True

    def is_valid_number(self, arr, row, col):

        return (
            self.not_in_row(arr, row)
            and self.not_in_col(arr, col)
            and self.not_in_box(arr, row - row % 3, col - col % 3)
        )

    def is_valid_board(self, arr):

        for i in range(0, 9):
            for j in range(0, 9):
                if not self.is_valid_number(arr, i, j):
                    return False
        return True
