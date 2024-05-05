import maze as mp
from collections import deque

def run_bfs(maze_puzzle: mp.MazePuzzle, current_point: mp.Point, visited: list[mp.Point]): 
    queue = deque()

    queue.append(current_point)
    visited.append(current_point)

    while queue:
        current_point = queue.popleft()
        neighnours = maze_puzzle.get_neighbours(curr_point=current_point)
        
        for neighbour in neighnours:
            if not is_in_visited(neighbour, visited):
                neighbour.set_parent(current_point)
                queue.append(neighbour)
                visited.append(neighbour)

                if maze_puzzle.get_current_point_value(neighbour) == "*":
                    return neighbour

    return "NO PATH"


def is_in_visited(curr_point: mp.Point, visited: list[mp.Point]) -> bool:
    for visited_point in visited:
        if curr_point.x == visited_point.x and curr_point.y == visited_point.y:
            return True
        
    return False

maze = mp.MazePuzzle()

print('---Breadth-first Search---')

start_point = mp.Point(2, 2)

outcome = run_bfs(maze, start_point, [])

bfs_path = mp.get_path(outcome)

maze.overlay_points_on_map(bfs_path)
for point in bfs_path:
    print('Point: ', point.x, ',', point.y)