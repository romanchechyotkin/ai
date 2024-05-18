import math
import copy


class Point:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y
        self.parent = None
        self.cost = math.inf

    def set_parent(self, p):
        self.parent = p

    def set_cost(self, c):
        self.cost = c

    def print(self):
        print(self.x, ',', self.y)    

class MazePuzzle:
    def __init__(self, x_size=5, y_size=5):
        self.x_size = x_size
        self.y_size = y_size
        self.maze = [
            "*0000",
            "0###0",
            "0#0#0",
            "0#000",
            "00000",
        ]

    def get_current_point_value(self, point: Point) -> str:
        return self.maze[point.x][point.y]

    def get_neighbours(self, curr_point: Point) -> list[Point]:
        neighbours = []
        potential_neighbours = [[NORTH.x, NORTH.y], [SOUTH.x, SOUTH.y], [EAST.x, EAST.y], [WEST.x, WEST.y]]

        for pn in potential_neighbours:
            target_point = Point(curr_point.x+pn[0], curr_point.y+pn[1])
            if 0 <= target_point.x and target_point.x < self.x_size and 0 <= target_point.y and target_point.y < self.y_size:
                if self.get_current_point_value(target_point) != "#":
                    neighbours.append(target_point)

        return neighbours
    
    def overlay_points_on_map(self, points: list[Point]):
        overlay_map = copy.deepcopy(self.maze)
        for point in points:
            new_row = overlay_map[point.x][:point.y] + '@' + overlay_map[point.x][point.y + 1:]
            overlay_map[point.x] = new_row

        result = ''
        for x in range(0, self.x_size):
            for y in range(0, self.y_size):
                result += overlay_map[x][y]
            result += '\n'
            
        print(result)

# These constants are used to reference points on the maze that are in the respective direction of a point in question.
NORTH = Point(0, 1)
SOUTH = Point(0, -1)
EAST = Point(1, 0)
WEST = Point(-1, 0)

# Utility to get a path as a list of points by traversing the parents of a node until the root is reached.
def get_path(point):
    path = []
    current_point = point
    while current_point.parent is not None:
        path.append(current_point)
        current_point = current_point.parent
    return path
