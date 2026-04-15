import heapq
import numpy as np

class LanePathPlanner:
    """
    Simple A* path planner for lane-based navigation.
    Grid:
        rows = forward distance
        cols = lanes (0,1,2)
    """

    def __init__(self, rows=10, lanes=3):
        self.rows = rows
        self.lanes = lanes

    def heuristic(self, node, goal):
        r, c = node
        gr, gc = goal
        return abs(gr - r) + abs(gc - c)

    def astar(self, grid, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            r, c = current

            for dc in [-1, 0, 1]:
                nr = r + 1
                nc = c + dc

                if nr >= self.rows or nc < 0 or nc >= self.lanes:
                    continue

                if grid[nr][nc] == 1:  # obstacle
                    continue

                new_cost = g_score[current] + 1
                neighbor = (nr, nc)

                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

        return []

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def plan(self, frame_width, frame_height, lane_info, obstacles):
        """
        Create grid and compute path
        """
        grid = np.zeros((self.rows, self.lanes))

        # Mark obstacles in grid
        for obj in obstacles:
            cx, cy = obj["center"]

            lane = int(cx / (frame_width / self.lanes))
            row = int((frame_height - cy) / (frame_height / self.rows))

            lane = max(0, min(self.lanes - 1, lane))
            row = max(0, min(self.rows - 1, row))

            grid[row][lane] = 1

        start = (0, 1)
        goal = (self.rows - 1, 1)

        path = self.astar(grid, start, goal)

        if not path:
            # fallback: choose safest lane
            lane_counts = np.sum(grid, axis=0)
            best_lane = int(np.argmin(lane_counts))
            path = [(r, best_lane) for r in range(self.rows)]
        else:
            best_lane = path[-1][1]

        next_lane = path[1][1] if len(path) > 1 else 1

        return {
            "grid": grid,
            "path": path,
            "next_lane": next_lane,
            "best_lane": best_lane,
            "fallback_used": len(path) == 0
        }