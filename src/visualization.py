import cv2

from .config import Config
from .utils import draw_multiline_panel, road_bounds_at_y, lane_x_at_y


def _draw_obstacles(frame, obstacles):
    for det in obstacles:
        x1, y1, x2, y2 = det["bbox"]
        label = det["label"]
        conf = det["confidence"]

        cv2.rectangle(frame, (x1, y1), (x2, y2), Config.OBSTACLE_COLOR, 2)
        cv2.putText(
            frame,
            f"{label} {conf:.2f}",
            (x1, max(20, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )


def _draw_lane_guides(frame, lane_info):
    left_line = lane_info["left_line"]
    right_line = lane_info["right_line"]

    cv2.line(frame, (left_line[0], left_line[1]), (left_line[2], left_line[3]), (0, 255, 255), 2)
    cv2.line(frame, (right_line[0], right_line[1]), (right_line[2], right_line[3]), (0, 255, 255), 2)

    center_x = lane_info["lane_center_x"]
    cv2.line(
        frame,
        (center_x, Config.FRAME_HEIGHT - 1),
        (center_x, Config.ROAD_TOP_Y),
        (255, 0, 255),
        1,
    )


def _draw_path(frame, plan):
    path = plan["path"]
    if not path:
        return

    points = []
    for row, lane_idx in path:
        y = Config.FRAME_HEIGHT - int(
            (row / max(1, Config.LOOKAHEAD_ROWS - 1))
            * (Config.FRAME_HEIGHT - Config.ROAD_TOP_Y - 40)
        )
        y = max(Config.ROAD_TOP_Y, min(Config.FRAME_HEIGHT - 1, y))
        left_x, right_x, road_width = road_bounds_at_y(y)
        lane_width = road_width / Config.LANE_COUNT
        x = int(left_x + lane_width * (lane_idx + 0.5))
        points.append((x, y))

    for i in range(len(points) - 1):
        cv2.line(frame, points[i], points[i + 1], Config.PATH_COLOR, 3)

    for pt in points:
        cv2.circle(frame, pt, 5, Config.PATH_COLOR, -1)


def draw_dashboard(frame, lane_info, obstacles, plan, command, frame_index=0):
    annotated = frame.copy()  # ✅ FIX: define annotated first

    # ===== DRAW SYSTEM ELEMENTS =====
    _draw_lane_guides(annotated, lane_info)
    _draw_obstacles(annotated, obstacles)
    _draw_path(annotated, plan)

    # ===== HUD SETTINGS =====
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.45
    font_thickness = 1
    line_height = 16
    padding = 8

    info_lines = [
        f"Frame: {frame_index}",
        f"Action: {command['action']}",
        f"Speed: {command['speed']:.2f}",
        f"Steering: {command['steering']:.2f}",
        f"Offset: {lane_info['lane_offset']}px",
        f"Objs: {len(obstacles)}",
        f"FB: {plan['fallback_used']}",
    ]

    # ===== BOX SIZE =====
    text_sizes = [cv2.getTextSize(line, font, font_scale, font_thickness)[0] for line in info_lines]
    max_width = max([w for (w, h) in text_sizes])
    box_width = max_width + padding * 2
    box_height = len(info_lines) * line_height + padding

    # ===== TRANSPARENT BOX =====
    overlay = annotated.copy()

    cv2.rectangle(
        overlay,
        (10, 10),
        (10 + box_width, 10 + box_height),
        (0, 0, 0),
        -1
    )

    alpha = 0.6
    cv2.addWeighted(overlay, alpha, annotated, 1 - alpha, 0, annotated)

    # ===== DRAW TEXT =====
    y = 10 + padding + 12
    for line in info_lines:
        cv2.putText(
            annotated,
            line,
            (10 + padding, y),
            font,
            font_scale,
            (255, 255, 255),
            font_thickness,
            cv2.LINE_AA
        )
        y += line_height

    return annotated