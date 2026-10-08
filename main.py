from tkinter import Tk, BOTH, Canvas
from turtle import undo

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
    def __init__(self, window):
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

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.has_left_wall:
            left_line = Line(Point(x1, y1), Point(x1, y2))
            self.lines.append(left_line)
            self.__win.draw_line(left_line)

        if self.has_right_wall:
            right_line = Line(Point(x2, y1), Point(x2, y2))
            self.lines.append(right_line)
            self.__win.draw_line(right_line)

        if self.has_top_wall:
            top_line = Line(Point(x1, y1), Point(x2, y1))
            self.lines.append(top_line)
            self.__win.draw_line(top_line)

        if self.has_bottom_wall:
            bottom_line = Line(Point(x1, y2), Point(x2, y2))
            self.lines.append(bottom_line)
            self.__win.draw_line(bottom_line)

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
            win: Window,
    ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win    
        self.__cells = []

        self.__create_cells()

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
                self.__draw_cell(self, col, row)

    def __draw_cell(self, col: int, row: int) -> None:
        x1 = self.__x1 + col * self.__cell_size_x
        y1 = self.__y1 + row * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        cell = self.__cells[col][row]
        cell.draw(x1, y1, x2, y2)
        
    def __animate(self) -> None:
        self.__win.redraw()
        # Sleep for 0.05 seconds to create an animation effect
        self.__win.canvas.after(50)

# Create a main entrypoint function, and in it, create a window and wait for it to close:
def main():
    window = Window(800, 600)

    # Create a maze with 5 rows and 6 columns, starting at (50, 50), with each cell being 50x50 pixels
    maze = Maze(50, 50, 5, 6, 50, 50, window)

    window.wait_for_close()

if __name__ == "__main__":
    main()