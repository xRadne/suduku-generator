"""Create a suduko puzzle using wave function collapse algorithm."""

import random
from time import sleep

size = 3  # size of suduko puzzle size 3 means 9x9 suduko


def grid_size():
    return size*size


def display_grid(grid):
    for i in range(grid_size()):
        for j in range(grid_size()):
            if len(grid[i][j]) == 1:
                print(grid[i][j][0], end=" ")
            else:
                print("x", end=" ")

            if j % size == size-1 and j != grid_size()-1:
                print("|", end=" ")

        if i % size == size-1 and i != grid_size()-1:
            print("\n------+-------+------", end="")
        print()


def display_grid_possibilities(grid):
    for i in range(grid_size()):
        for j in range(grid_size()):
            print(len(grid[i][j]), end=" ")

            if j % size == size-1 and j != grid_size()-1:
                print("|", end=" ")

        if i % size == size-1 and i != grid_size()-1:
            print("\n------+-------+------", end="")
        print()


def remove_possibility_line(grid, row, column, value):
    new_single_value_cells = []
    for i in range(grid_size()):
        if i != column:
            if value in grid[row][i]:
                grid[row][i].remove(value)
                if len(grid[row][i]) == 1:
                    new_single_value_cells.append((row, i))

    for i in range(grid_size()):
        if i != row:
            if value in grid[i][column]:
                grid[i][column].remove(value)
                if len(grid[i][column]) == 1:
                    new_single_value_cells.append((i, column))

    return new_single_value_cells


def remove_possibility_square(grid, row, column, value):
    new_single_value_cells = []
    for i in range(row - row % size, row - row % size + size):
        for j in range(column - column % size, column - column % size + size):
            if i == row and j == column:
                continue

            if value in grid[i][j]:
                grid[i][j].remove(value)
                if len(grid[i][j]) == 1:
                    new_single_value_cells.append((i, j))

    return new_single_value_cells


def min_entropy_cells(grid):
    """Selects the indices (i, j) of the cells with the fewest possibilities (lowest entropy)."""
    min_possibilities = grid_size()

    cells_with_min_possibilities = []
    for i in range(grid_size()):
        for j in range(grid_size()):
            if 1 < len(grid[i][j]) < min_possibilities:
                min_possibilities = len(grid[i][j])
                cells_with_min_possibilities = [(i, j)]
            elif len(grid[i][j]) == min_possibilities:
                cells_with_min_possibilities.append((i, j))
    return cells_with_min_possibilities


def observe_cell(grid, position=None):
    if position is not None:
        i, j = position
    else:
        # Select a cell with the fewest possibilities at random
        cells_with_min_possibilities = min_entropy_cells(grid)
        i, j = random.choice(cells_with_min_possibilities)

    # Select a random value from the cell
    value = random.choice(grid[i][j])
    grid[i][j] = [value]

    new_single_value_cells = []

    # Propagate the value to the rest of the grid rows and columns
    new_single_value_cells += remove_possibility_line(grid, i, j, value)

    # Propagate the value to the rest of the grid square
    new_single_value_cells += remove_possibility_square(grid, i, j, value)

    for i, j in new_single_value_cells:
        try:
            observe_cell(grid, (i, j))
        except IndexError:
            return False

    return True


def generate_initial_grid():
    return [[[v for v in range(1, grid_size()+1)]
             for x in range(grid_size())] for y in range(grid_size())]


def deep_copy(grid):
    return [[grid[i][j][:] for j in range(grid_size())] for i in range(grid_size())]


def generate_solved_puzzle(initial_grid=None, seed=None, max_allowed_contradictions=100, display=False, wait_time=0.01, wait_for_input=False):
    grid = initial_grid
    if initial_grid is None:
        grid = generate_initial_grid()

    if isinstance(seed, int):
        random.seed(seed)

    # Randomly remove possible values from the grid
    condtradiction_count = 0
    observations = 0
    while True:
        previous_grid = deep_copy(grid)

        # Observe a single cell
        ok = observe_cell(grid)
        observations += 1

        if not ok:
            # Observation led to contradiction - backtrack
            grid = previous_grid
            condtradiction_count += 1
            if condtradiction_count > max_allowed_contradictions:
                return grid

        if display:
            print("Observed a cell ({})".format(observations))
            display_grid(grid)

            if wait_for_input:
                s = input("Press enter to continue...")
                if s == "q":
                    return grid
                elif s == "s":
                    display = False
            else:
                sleep(wait_time)

        # Check if the grid is solved (all cells contain only a single value)
        if is_solved(grid):
            if display:
                print("Created a puzzle in {} observations".format(observations))
                display_grid(grid)
            return grid

        if is_contradiction(grid):
            # If the grid became a contradiction, undo the last observed cell
            condtradiction_count += 1
            if condtradiction_count < max_allowed_contradictions:
                grid = previous_grid
                continue

            if display:
                print("Contradiction:")
                display_grid(grid)
                print("No solution found.")
                display_grid_possibilities(grid)
            return grid


def is_contradiction(grid):
    if grid is None:
        return True
    return any(len(grid[i][j]) < 1 for i in range(grid_size()) for j in range(grid_size()))


def is_solved(grid):
    if grid is None:
        return False
    return all(len(grid[i][j]) == 1 for i in range(grid_size()) for j in range(grid_size()))


if __name__ == "__main__":
    # Generate a suduko puzzle
    import timeit
    start = timeit.default_timer()
    tries = 0
    for i in range(100):
        puzzle = generate_solved_puzzle()
        tries += 1
        if is_solved(puzzle):
            break
    end = timeit.default_timer()

    status = "Found solution" if is_solved(puzzle) else "Contradiction"
    tries_description = "in {} tries".format(
        tries) if tries > 1 else "in 1 try"
    print(f"Puzzle: {status} in {end - start:.2f} seconds {tries_description}")
    display_grid(puzzle)
