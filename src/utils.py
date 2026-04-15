import os
import cv2
from .config import Config


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def ensure_directories():
    """Create the output folders if they do not exist."""
    folders = [
        Config.OUTPUT_DIR,
        "outputs/result_videos",
        "outputs/logs",
        "outputs/annotated_frames",
        "outputs/metrics",
        "images/screenshots",
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def road_bounds_at_y(y):
    """
    Return the left and right road boundaries at a given y-position.
    The road is a trapezoid: narrow at the top, wide at the bottom.
    """
    y = clamp(y, Config.ROAD_TOP_Y, Config.FRAME_HEIGHT - 1)
    t = (y - Config.ROAD_TOP_Y) / (Config.FRAME_HEIGHT - Config.ROAD_TOP_Y)

    road_width = Config.ROAD_TOP_WIDTH + t * (Config.ROAD_BOTTOM_WIDTH - Config.ROAD_TOP_WIDTH)
    center_x = Config.FRAME_WIDTH / 2.0

    left_x = int(center_x - road_width / 2.0)
    right_x = int(center_x + road_width / 2.0)

    return left_x, right_x, int(road_width)


def lane_centers_at_y(y):
    """
    Return the x-coordinates of the 3 lane centers at a given y-position.
    """
    left_x, right_x, road_width = road_bounds_at_y(y)
    lane_width = road_width / Config.LANE_COUNT
    centers = [int(left_x + lane_width * (i + 0.5)) for i in range(Config.LANE_COUNT)]
    return centers


def lane_x_at_y(y, lane_index):
    """
    Return the x-coordinate of the center of a lane at a given y-position.
    """
    lane_index = clamp(lane_index, 0, Config.LANE_COUNT - 1)
    return lane_centers_at_y(y)[lane_index]


def draw_multiline_panel(img, lines, x=15, y=15, padding=10, line_gap=8,
                         font_scale=0.58, thickness=2,
                         bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    """
    Draw a clean text panel with multiple lines.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX

    if not lines:
        return img

    sizes = [cv2.getTextSize(line, font, font_scale, thickness)[0] for line in lines]
    widths = [s[0] for s in sizes]
    heights = [s[1] for s in sizes]

    box_w = max(widths) + padding * 2
    box_h = sum(heights) + line_gap * (len(lines) - 1) + padding * 2

    cv2.rectangle(img, (x, y), (x + box_w, y + box_h), bg_color, -1)
    cv2.rectangle(img, (x, y), (x + box_w, y + box_h), (70, 70, 70), 1)

    current_y = y + padding + heights[0]
    for i, line in enumerate(lines):
        cv2.putText(
            img,
            line,
            (x + padding, current_y),
            font,
            font_scale,
            text_color,
            thickness,
            cv2.LINE_AA,
        )
        if i < len(lines) - 1:
            current_y += heights[i] + line_gap

    return img