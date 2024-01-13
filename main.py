import numpy as np


class PartialSudokuState:
    def __init__(self, current_board):
        """
        current_state = current state of the sudoku solver
        """
        self.board = current_board
        # When initialising, we always want to create an array of possible values
        # and then remove from these
        self.possible_values = [
            [[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(1, 9 + 1)]
            for _ in range(1, 9 + 1)
        ]
        self.possible_values = self.__satisfy_constraints__()

    # CHANGE THIS
    def is_goal(self):
        # True if every square in the board has been filled in
        all_non_zero = all(square != 0 for row in self.board for square in row)

        # True if every square in each board row has a unique value
        goal_rows = all(len(set(row)) == 9 for row in self.board)

        # True if every square in each board column has a unique value
        board_transposed = list(map(list, zip(*self.board)))
        goal_cols = all(len(set(col)) == 9 for col in board_transposed)

        # True if every square in each 3x3 board block has a unique value (!= 0 already covered in all_non_zero)
        board_blocks = [
            np.array(self.board)[3 * i : 3 * i + 3, 3 * j : 3 * j + 3]
            for i in range(3)
            for j in range(3)
        ]
        goal_blocks = all(len(set(block.flatten())) == 9 for block in board_blocks)

        return all((all_non_zero, goal_rows, goal_cols, goal_blocks))

    def __satisfy_constraints__(self):
        """
        A sudoku game has four constraints. These are:
        1. each square must have a value between 1-9 in it
        2. each row should have a unique number in each square
        3. each column should have a unique number in each square
        4. each 3x3 grid should have a unique number in each square

        Given this, this method goes through each value in the remaining values in the board and
        makes sure they are satisfying these constraints
        """
        for col in range(9):
            for row in range(9):
                current_value = self.board[row][col]
                if current_value == 0:
                    # If the current value in the board is 0, then we know there are
                    # possibilities that we need to find
                    self.possible_values[row][
                        col
                    ] = self.get_potential_value_for_square(row, col)
                else:
                    self.possible_values[row][col] = None

        print(self.possible_values, "poss")

    def get_potential_value_for_square(self, row, col):
        """
        We need to satisfy constraints for a given index and we can do this here
        """
        potential_values_in_square = self.possible_values[row][col]
        print(potential_values_in_square, "potential_values_in_square")
        # handle row and column
        for i in range(9):
            # handle rows
            current_value_in_board = self.board[row][i]
            current_value_found = current_value_in_board != 0
            if (
                current_value_found
                and current_value_in_board in potential_values_in_square
            ):
                potential_values_in_square.remove(current_value_in_board)
            current_value_in_board = self.board[i][col]
            current_value_found = current_value_in_board != 0
            # handle columns
            if (
                current_value_found
                and current_value_in_board in potential_values_in_square
            ):
                potential_values_in_square.remove(current_value_in_board)

        # handle grids
        block_row = row - row % 3
        block_col = col - col % 3
        for i in range(3):
            for j in range(3):
                current_value = self.board[i + block_row][j + block_col]
                current_value_found = current_value != 0
                if current_value_found and current_value in potential_values_in_square:
                    potential_values_in_square.remove(current_value)

        return potential_values_in_square

    def remove_values(self):
        pass

    def has_potential_solution(self):
        """
        Checks whether there are any rows, columns or grids that are invalid. If this is the case, then this
        sudoku state cannot be solved so it is invalid. This will mean going back up the chain and checking
        a different permutation
        """
        pass


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    sudoku_state = PartialSudokuState(sudoku)
    # print(sudoku_state.is_goal())

    return []


if __name__ == "__main__":
    sudoku = np.load("data/hard_puzzle.npy")
    solutions = np.load("data/very_easy_solution.npy")

    sudoku_solver(sudoku[0])
    # Print the first 9x9 sudoku...
    # print("First sudoku:")
    # print(sudoku[0], "\n")

    solution = sudoku_solver(sudoku[0])

    # print("Solution from code:")

    # print(solution)

    # # ...and its solution
    # print("Preset solution:")
    # print(solutions[14])
