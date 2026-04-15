import random
import numpy as np
import cv2

from .config import Config
from .utils import road_bounds_at_y, lane_x_at_y, lane_centers_at_y, clamp


class SyntheticObstacle:
    """
    A simple obstacle that moves downward in the road scene.
    """

    def __init__(self, lane_index, y, speed):
        self.lane_index = lane_index
        self.y = float(y)
        self.speed = float(speed)

    def update(self):
        self.y += self.speed

    def respawn(self):
        self.lane_index = random.randint(0, Config.LANE_COUNT - 1)
        self.y = random.uniform(Config.ROAD_TOP_Y - 220, Config.ROAD_TOP_Y - 60)
        self.speed = random.uniform(Config.OBSTACLE_MIN_SPEED, Config.OBSTACLE_MAX_SPEED)

    def get_bbox(self):
        """
        Return the obstacle bounding box in image coordinates.
        """
        center_x = lane_x_at_y(self.y, self.lane_index)
        lane_centers = lane_centers_at_y(self.y)
        left_x, right_x, road_width = road_bounds_at_y(self.y)

        box_w = max(34, int(road_width * 0.13))
        box_h = max(46, int(box_w * 1.4))

        x1 = int(center_x - box_w / 2)
        y1 = int(self.y - box_h / 2)
        x2 = int(center_x + box_w / 2)
        y2 = int(self.y + box_h / 2)

        x1 = clamp(x1, 0, Config.FRAME_WIDTH - 1)
        y1 = clamp(y1, 0, Config.FRAME_HEIGHT - 1)
        x2 = clamp(x2, 0, Config.FRAME_WIDTH - 1)
        y2 = clamp(y2, 0, Config.FRAME_HEIGHT - 1)

        return x1, y1, x2, y2

    def is_out_of_frame(self):
        _, _, _, y2 = self.get_bbox()
        return y2 >= Config.FRAME_HEIGHT - 1


class SyntheticRoadSimulator:
    """
    Generates a front-view road simulation with lane markers and moving obstacles.
    """

    def __init__(self, seed=42, num_obstacles=Config.NUM_OBSTACLES):
        random.seed(seed)
        np.random.seed(seed)
        self.frame_index = 0
        self.obstacles = [
            self._spawn_obstacle(initial=True) for _ in range(num_obstacles)
        ]

    def _spawn_obstacle(self, initial=False):
        lane_index = random.randint(0, Config.LANE_COUNT - 1)
        if initial:
            y = random.uniform(Config.ROAD_TOP_Y + 25, Config.FRAME_HEIGHT - 140)
        else:
            y = random.uniform(Config.ROAD_TOP_Y - 250, Config.ROAD_TOP_Y - 80)
        speed = random.uniform(Config.OBSTACLE_MIN_SPEED, Config.OBSTACLE_MAX_SPEED)
        return SyntheticObstacle(lane_index, y, speed)

    def step(self):
        self.frame_index += 1

        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.is_out_of_frame():
                obstacle.respawn()

        return self.render()

    def _draw_road(self, frame):
        top_left, top_right, _ = road_bounds_at_y(Config.ROAD_TOP_Y)
        bottom_left, bottom_right, _ = road_bounds_at_y(Config.FRAME_HEIGHT - 1)

        road_polygon = np.array(
            [
                [top_left, Config.ROAD_TOP_Y],
                [top_right, Config.ROAD_TOP_Y],
                [bottom_right, Config.FRAME_HEIGHT - 1],
                [bottom_left, Config.FRAME_HEIGHT - 1],
            ],
            dtype=np.int32,
        )

        cv2.fillPoly(frame, [road_polygon], Config.ROAD_COLOR)

        # Road edge lines
        cv2.line(
            frame,
            (top_left, Config.ROAD_TOP_Y),
            (bottom_left, Config.FRAME_HEIGHT - 1),
            Config.ROAD_EDGE_COLOR,
            2,
        )
        cv2.line(
            frame,
            (top_right, Config.ROAD_TOP_Y),
            (bottom_right, Config.FRAME_HEIGHT - 1),
            Config.ROAD_EDGE_COLOR,
            2,
        )

        # Lane markers (dashed)
        for y in range(Config.ROAD_TOP_Y + 10, Config.FRAME_HEIGHT - 15, 22):
            y2 = min(y + 12, Config.FRAME_HEIGHT - 1)

            left_x1, right_x1, _ = road_bounds_at_y(y)
            left_x2, right_x2, _ = road_bounds_at_y(y2)

            road_width1 = right_x1 - left_x1
            road_width2 = right_x2 - left_x2

            lane1_x1 = int(left_x1 + road_width1 / 3)
            lane1_x2 = int(left_x2 + road_width2 / 3)

            lane2_x1 = int(left_x1 + 2 * road_width1 / 3)
            lane2_x2 = int(left_x2 + 2 * road_width2 / 3)

            cv2.line(
                frame,
                (lane1_x1, y),
                (lane1_x2, y2),
                Config.LANE_MARKER_COLOR,
                2,
            )
            cv2.line(
                frame,
                (lane2_x1, y),
                (lane2_x2, y2),
                Config.LANE_MARKER_COLOR,
                2,
            )

    def _draw_ego_vehicle(self, frame):
        """
        Draw the ego vehicle at the bottom center for demo purposes.
        """
        car_w = 54
        car_h = 86
        x_center = Config.FRAME_WIDTH // 2
        y_bottom = Config.FRAME_HEIGHT - 28

        x1 = x_center - car_w // 2
        y1 = y_bottom - car_h
        x2 = x_center + car_w // 2
        y2 = y_bottom

        cv2.rectangle(frame, (x1, y1), (x2, y2), Config.EGO_COLOR, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (20, 20, 20), 2)

        # Windshield / detail
        cv2.rectangle(
            frame,
            (x1 + 10, y1 + 10),
            (x2 - 10, y1 + 34),
            (230, 230, 230),
            -1,
        )

    def _draw_obstacles(self, frame):
        for obstacle in self.obstacles:
            x1, y1, x2, y2 = obstacle.get_bbox()
            cv2.rectangle(frame, (x1, y1), (x2, y2), Config.OBSTACLE_COLOR, -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 120), 2)

    def render(self):
        frame = np.full(
            (Config.FRAME_HEIGHT, Config.FRAME_WIDTH, 3),
            Config.BACKGROUND_COLOR,
            dtype=np.uint8,
        )

        self._draw_road(frame)
        self._draw_obstacles(frame)
        self._draw_ego_vehicle(frame)

        cv2.putText(
            frame,
            "Synthetic Autonomous Navigation Simulation",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (240, 240, 240),
            2,
            cv2.LINE_AA,
        )

        return frame