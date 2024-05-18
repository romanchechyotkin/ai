from collections import deque
import math

# implementation of A* algorithm

class Node:
    def __init__(self, x=0, y=0, cost=0) -> None:
        self.parent = None
        self.x = x
        self.y = y
        self.cost = cost

    def info(self):
        print(f"x: {self.x}; y: {self.y}; cost: {self.cost}")        

    def set_parent(self, point):
        self.parent = point

    def set_cost(self, cost):
        self.cost = cost    


NORTH = Node(-1, 0, 5)
SOUTH = Node(1, 0, 5)
EAST = Node(0, 1, 1)
WEST = Node(0, -1, 1)

class Maze:
    def __init__(self):
        # '#' - wall; '*' - finish
        self.maze = [
            "*0000",
            "0###0",
            "0#0#0",
            "0#000",
            "00000",
        ]
        self.x = len(self.maze)
        self.y = len(self.maze[0])

    def get_current_point_value(self, point: Node) -> str:
        return self.maze[point.x][point.y]

    def get_neighbours(self, current_point: Node) -> list[Node]:
        neighbours = []
        potential = [NORTH, SOUTH, WEST, EAST]

        for p in potential:
            target_point = Node(x=current_point.x+p.x, y=current_point.y+p.y, cost=p.cost)

            if 0 <= target_point.x < self.x and 0 <= target_point.y < self.y:
                if self.get_current_point_value(target_point) != "#":
                    neighbours.append(target_point)

        return neighbours

def calculate_cost(target: Node):
    distance_to_root = get_path(target)[1]
    cost = target.cost
    
    return cost + distance_to_root     


def run_a_star(maze: Maze, current_point: Node, visited: list[Node]):
    stack = [current_point]

    while stack:
        current_point = stack.pop()

        if not is_in_visited(current_point, visited):
            visited.append(current_point)
            
            if maze.get_current_point_value(current_point) == "*":
                return current_point
            
            else:
                neighbours = maze.get_neighbours(current_point)

                for n in neighbours:
                    n.set_parent(current_point)
                    n.set_cost(calculate_cost(n))
                    stack.append(n)

                stack.sort(key=lambda x: x.cost, reverse=True)

    return "NO PATH"


def is_in_visited(current_point: Node, visited: list[Node]) -> bool:
    for p in visited:
        if p.x == current_point.x and p.y == current_point.y:
            return True
        
    return False

def get_path(point: Node):
    res = []
    l = 0
    cost = 0
    tmp = point

    while tmp.parent is not None:
        res.append(tmp)
        l += 1
        cost += tmp.cost
        tmp = tmp.parent
    
    return res, l, cost


maze = Maze()
node = Node(2, 2)

outcome = run_a_star(maze, node, [])
if not isinstance(outcome, str):
    res = get_path(outcome)

    for p in res[0]:
        p.info()

    print(res[2])    
else:
    print(outcome)