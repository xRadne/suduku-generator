import suduku


def test_grid_size():
    suduku.size = 3
    assert suduku.grid_size() == 9


def test_is_contradiction():
    grid = [[[v for v in range(1, suduku.grid_size()+1)]
             for x in range(suduku.grid_size())] for y in range(suduku.grid_size())]
    grid[0][0] = []
    assert suduku.is_contradiction(grid)
    grid[0][0] = [1]
    assert not suduku.is_contradiction(grid)


def test_is_solved():
    grid = [[[1] for x in range(suduku.grid_size())]
            for y in range(suduku.grid_size())]
    assert suduku.is_solved(grid)
    grid[0][0] = [1, 2]
    assert not suduku.is_solved(grid)


def test_remove_possibility_line():
    suduku.size = 2
    grid = [[[1, 2, 3, 4]
             for x in range(suduku.grid_size())] for y in range(suduku.grid_size())]
    grid[0][0] = [1]
    suduku.remove_possibility_line(grid, 0, 0, 1)
    assert grid[0][0] == [1]
    assert grid[0][1] == [2, 3, 4]
    assert grid[0][2] == [2, 3, 4]
    assert grid[0][3] == [2, 3, 4]
    assert grid[1][0] == [2, 3, 4]
    assert grid[1][1] == [1, 2, 3, 4]
    assert grid[1][2] == [1, 2, 3, 4]
    assert grid[1][3] == [1, 2, 3, 4]
    assert grid[2][0] == [2, 3, 4]
    assert grid[2][1] == [1, 2, 3, 4]
    assert grid[2][2] == [1, 2, 3, 4]
    assert grid[2][3] == [1, 2, 3, 4]
    assert grid[3][0] == [2, 3, 4]
    assert grid[3][1] == [1, 2, 3, 4]
    assert grid[3][2] == [1, 2, 3, 4]
    assert grid[3][3] == [1, 2, 3, 4]


def test_remove_possibility_square():
    suduku.size = 2
    grid = [[[1, 2, 3, 4]
             for x in range(suduku.grid_size())] for y in range(suduku.grid_size())]
    grid[0][0] = [1]
    suduku.remove_possibility_square(grid, 0, 0, 1)
    assert grid[0][0] == [1]
    assert grid[0][1] == [2, 3, 4]
    assert grid[0][2] == [1, 2, 3, 4]
    assert grid[0][3] == [1, 2, 3, 4]
    assert grid[1][0] == [2, 3, 4]
    assert grid[1][1] == [2, 3, 4]
    assert grid[1][2] == [1, 2, 3, 4]
    assert grid[1][3] == [1, 2, 3, 4]
    assert grid[2][0] == [1, 2, 3, 4]
    assert grid[2][1] == [1, 2, 3, 4]
    assert grid[2][2] == [1, 2, 3, 4]
    assert grid[2][3] == [1, 2, 3, 4]
    assert grid[3][0] == [1, 2, 3, 4]
    assert grid[3][1] == [1, 2, 3, 4]
    assert grid[3][2] == [1, 2, 3, 4]
    assert grid[3][3] == [1, 2, 3, 4]


def test_get_possible_values():
    suduku.size = 2
    grid = [[[1],       [2, 3, 4],    [2, 3, 4],    [2, 3, 4]],
            [[2, 3, 4], [2, 3, 4],    [1, 2, 3, 4], [1, 2, 3, 4]],
            [[2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
            [[2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]]

    possible = suduku.get_possible_values(grid, 0, 0)
    assert possible == [1, 2, 3, 4]

    possible = suduku.get_possible_values(grid, 0, 1)
    assert possible == [2, 3, 4]


def test_min_entropy_cells():
    suduku.size = 2
    grid = [[[1],       [2, 3, 4],    [2, 3, 4],    [2, 3, 4]],
            [[2, 3, 4], [2, 3, 4],    [1, 2, 3, 4], [1, 2, 3, 4]],
            [[2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
            [[2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]]

    cells = suduku.min_entropy_cells(grid)
    assert cells == [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (2, 0), (3, 0)]


def test_observe_cell():
    grid = suduku.generate_initial_grid()
    suduku.observe_cell(grid)

    assert any(any(len(cell) == 1 for cell in row) for row in grid)

test_observe_cell()
