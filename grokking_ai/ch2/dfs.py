import maze as mp
from collections import deque

def run_dfs(maze_puzzle: mp.MazePuzzle, current_point: mp.Point, visited: list[mp.Point]):
    stack = deque() # append // pop

    stack.append(current_point)

    while stack: 
        current_point = stack.pop()
        
        print(current_point.x, current_point.y)

        if not is_in_visited(current_point, visited):
            visited.append(current_point)

            if maze_puzzle.get_current_point_value(current_point) == "*":
                    return current_point
            else:
                neighbours = maze_puzzle.get_neighbours(current_point)

                for n in neighbours:
                    n.set_parent(current_point)
                    stack.append(n)
    
    return "NO PATH"

def is_in_visited(curr_point: mp.Point, visited: list[mp.Point]) -> bool:
    for visited_point in visited:
        if curr_point.x == visited_point.x and curr_point.y == visited_point.y:
            return True
        
    return False

maze = mp.MazePuzzle()

print("---Depth-first Search---")

start_point = mp.Point(2, 2)

outcome = run_dfs(maze, start_point, [])

dfs_path = mp.get_path(outcome)
for p in dfs_path:
    print("POINT: ", p.x, ",", p.y)