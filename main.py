from tkinter import Tk, BOTH, Canvas
from turtle import undo
import random

class Window:
    def __init__(self, width, height, title="Maze Solver"):
        # Create the root widget and set its title
        self.__root = Tk()
        self.__root.title(title)
        
        # Create the canvas widget and pack it
        self.canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        
        self.running = False

        # Connect the close method to the "delete window" action
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )

# Create a Cell class that takes an instance of a Window
class Cell:
    def __init__(self, window: Window=None):
        self.lines = []
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = 0
        self.__x2 = 0
        self.__y1 = 0
        self.__y2 = 0
        self.__win = window
        self._visited = False # Track whether cell has had it's walls broken

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        left_line = Line(Point(x1, y1), Point(x1, y2))
        self.lines.append(left_line)
        if self.__win:
            if self.has_left_wall:
                self.__win.draw_line(left_line)
            else:
                self.__win.draw_line(left_line, fill_color="white")

        right_line = Line(Point(x2, y1), Point(x2, y2))
        self.lines.append(right_line)
        if self.__win:
            if self.has_right_wall:
                self.__win.draw_line(right_line)
            else:
                self.__win.draw_line(right_line, fill_color="white")

        top_line = Line(Point(x1, y1), Point(x2, y1))
        self.lines.append(top_line)
        if self.__win:
            if self.has_top_wall:
                self.__win.draw_line(top_line)
            else:
                self.__win.draw_line(top_line, fill_color="white")

        bottom_line = Line(Point(x1, y2), Point(x2, y2))
        self.lines.append(bottom_line)
        if self.__win:
            if self.has_bottom_wall:
                self.__win.draw_line(bottom_line)
            else:
                self.__win.draw_line(bottom_line, fill_color="white")

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        if not undo:
            color = "red"
        else:
            color = "gray"
        center_x1 = (self.__x1 + self.__x2) / 2
        center_y1 = (self.__y1 + self.__y2) / 2
        center_x2 = (to_cell.__x1 + to_cell.__x2) / 2
        center_y2 = (to_cell.__y1 + to_cell.__y2) / 2
        move_line = Line(Point(center_x1, center_y1), Point(center_x2, center_y2))
        if self.__win:
            self.__win.draw_line(move_line, fill_color=color)

class Maze:
    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x: float,
            cell_size_y: float,
            win: Window=None,
            seed: int=None
    ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win    
        self.__cells = []
        if seed is not None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()  # Break the entrance and exit walls
        self.__break_walls_r(0, 0)  # Start breaking walls from the top-left cell
        self._reset_cells_visited()  # Reset visited status for all cells after maze generation

    def __create_cells(self) -> None:
        for col in range(self.__num_cols):
            cell_column = []
            for row in range(self.__num_rows):
                cell = Cell(self.__win)
                cell_column.append(cell)
            self.__cells.append(cell_column)

        # Draw the cells after they have been created
        for col in range(self.__num_cols):
            for row in range(self.__num_rows):
                self.__draw_cell(col, row)

    def __draw_cell(self, col: int, row: int) -> None:
        x1 = self.__x1 + col * self.__cell_size_x
        y1 = self.__y1 + row * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        cell = self.__cells[col][row]
        if self.__win:
            cell.draw(x1, y1, x2, y2)
            self.__animate()
        
    def __animate(self) -> None:
        if self.__win:
            self.__win.redraw()
            # Sleep for 0.05 seconds to create an animation effect
            self.__win.canvas.after(50)

    def __break_entrance_and_exit(self) -> None:
        # Break the left wall of the first cell (entrance)
        self.__cells[0][0].has_left_wall = False

        # Redraw the first cell to reflect the broken wall
        self.__draw_cell(0, 0)  

        # Break the right wall of the last cell (exit)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_right_wall = False

        # Redraw the last cell to reflect the broken wall
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)  

    def __break_walls_r(self, i, j):
        # 1. Mark current cell as visited
        self.__cells[i][j]._visited = True

        # 2. Infinite loop to keep breaking walls until all reachable neighbors are visited
        while True:
            unvisited_neighbors = []

            # Check UP (i, j - 1)
            if j > 0 and not self.__cells[i][j - 1]._visited:
                unvisited_neighbors.append((i, j - 1))

            # Check DOWN (i, j + 1)
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1]._visited:
                unvisited_neighbors.append((i, j + 1))

            # Check LEFT (i - 1, j)
            if i > 0 and not self.__cells[i - 1][j]._visited:
                unvisited_neighbors.append((i - 1, j))

            # Check RIGHT (i + 1, j)
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j]._visited:
                unvisited_neighbors.append((i + 1, j))

            # If no unvisited neighbors, draw cell and return to backtrack
            if len(unvisited_neighbors) == 0:
                self.__draw_cell(i, j)
                return

            # Pick random direction
            next_i, next_j = random.choice(unvisited_neighbors)

            # Knock down walls between (i, j) and (next_i, next_j)
            if next_i == i - 1:  # Left
                self.__cells[i][j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
            elif next_i == i + 1:  # Right
                self.__cells[i][j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            elif next_j == j - 1:  # Up
                self.__cells[i][j].has_top_wall = False
                self.__cells[next_i][next_j].has_bottom_wall = False
            elif next_j == j + 1:  # Down
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False

            # Recurse into chosen neighbor
            self.__break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for col in range(self.__num_cols):
            for row in range(self.__num_rows):
                self.__cells[col][row]._visited = False
            for row in range(self.__num_rows):
                self.__cells[col][row]._visited = False

    def solve(self) -> bool:
        self._reset_cells_visited()  # Reset visited status before solving
        return self._solve_r(0, 0)

    def _solve_r(self, i, j) -> bool:
        self.__animate()
        self.__cells[i][j]._visited = True
        # Base case: if we are at the exit cell, return True
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True
        # Explore neighbors in the order: UP, DOWN, LEFT, RIGHT
        # UP
        if j > 0 and not self.__cells[i][j - 1]._visited and not self.__cells[i][j].has_top_wall:
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1], undo=True)
        # DOWN
        if j < self.__num_rows - 1 and not self.__cells[i][j + 1]._visited and not self.__cells[i][j].has_bottom_wall:
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1], undo=True)
        # LEFT
        if i > 0 and not self.__cells[i - 1][j]._visited and not self.__cells[i][j].has_left_wall:
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i - 1][j], undo=True)
        # RIGHT
        if i < self.__num_cols - 1 and not self.__cells[i + 1][j]._visited and not self.__cells[i][j].has_right_wall:
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j], undo=True)
        return False
        

# Create a main entrypoint function, and in it, create a window and wait for it to close:
def main():
    window = Window(800, 600)

    # Create a maze
    maze = Maze(50, 50, 10, 12, 50, 50, win=window)
    maze.solve()

    window.wait_for_close()

if __name__ == "__main__":
    main()