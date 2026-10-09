import unittest

from main import Maze 

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
            print(f"Expected {num_cols} columns, but got {len(m1._Maze__cells)} columns.")
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
            print(f"Expected {num_rows} rows, but got {len(m1._Maze__cells[0])} rows.")
        )

    def test_maze_create_cells_large(self):
        num_cols = 25
        num_rows = 30
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
            print(f"Expected {num_cols} columns, but got {len(m1._Maze__cells)} columns.")
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
            print(f"Expected {num_rows} rows, but got {len(m1._Maze__cells[0])} rows.")
        )

def test_maze_create_cells_single_cell(self):
    num_cols = 1
    num_rows = 1
    m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
    self.assertEqual(
        len(m1._Maze__cells),
        num_cols,
    )
    self.assertEqual(
        len(m1._Maze__cells[0]),
        num_rows,
    )

def test_maze_create_cells_asymmetric(self):
    num_cols = 1
    num_rows = 50
    m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
    self.assertEqual(
        len(m1._Maze__cells),
        num_cols,
    )
    self.assertEqual(
        len(m1._Maze__cells[0]),
        num_rows,
    )

def test_maze_no_window(self):
    num_cols = 10
    num_rows = 10
    # Omit the window parameter entirely
    m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
    
    # Assert that _win (or win) defaults to None
    self.assertEqual(m1._win, None)

def test_maze_explicit_none_window(self):
    num_cols = 5
    num_rows = 5
    m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win=None)
    
    self.assertIsNone(m1._win)

def test_maze_draw_cell_with_no_window(self):
    m1 = Maze(0, 0, 5, 5, 10, 10, win=None)
    
    # Should complete without raising an exception/error
    m1._draw_cell(0, 0)

def test_break_entrance_and_exit(self):
    num_cols = 5
    num_rows = 5
    m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
    
    # Break the entrance and exit walls
    m1._break_entrance_and_exit()
    
    # Check that the entrance wall is broken
    self.assertFalse(m1._Maze__cells[0][0].has_left_wall)
    
    # Check that the exit wall is broken
    self.assertFalse(m1._Maze__cells[num_cols - 1][num_rows - 1].has_right_wall)

def test_reset_cells_visited(self):
    num_cols = 12
    num_rows = 10
    m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
    
    # Iterate through every cell in the grid and check that _visited is False
    for col in range(num_cols):
        for row in range(num_rows):
            self.assertEqual(
                m1._Maze__cells[col][row]._visited,
                False,
            )

def main():
    if __name__ == "__main__":
        unittest.main()