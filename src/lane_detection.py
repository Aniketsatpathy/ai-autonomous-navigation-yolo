import cv2
import numpy as np

from .config import Config
from .utils import road_bounds_at_y, clamp


def _region_of_interest(edges):
    """
    Keep only the road area.
    """
    mask = np.zeros_like(edges)

    height, width = edges.shape
    polygon = np.array(
        [
            [
                (int(width * 0.15), height),
                (int(width * 0.42), Config.ROAD_TOP_Y),
                (int(width * 0.58), Config.ROAD_TOP_Y),
                (int(width * 0.85), height),
            ]
        ],
        dtype=np.int32,
    )

    cv2.fillPoly(mask, polygon, 255)
    roi = cv2.bitwise_and(edges, mask)
    return roi


def _average_slope_intercept(lines):
    left_fits = []
    right_fits = []

    if lines is None:
        return None, None

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        if x2 == x1:
            continue

        slope = (y2 - y1) / (x2 - x1)
        if abs(slope) < 0.35:
            continue

        intercept = y1 - slope * x1

        if slope < 0:
            left_fits.append((slope, intercept))
        else:
            right_fits.append((slope, intercept))

    left_fit = np.mean(left_fits, axis=0) if left_fits else None
    right_fit = np.mean(right_fits, axis=0) if right_fits else None

    return left_fit, right_fit


def _make_line_points(y1, y2, fit):
    if fit is None:
        return None

    slope, intercept = fit
    if abs(slope) < 1e-6:
        return None

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return (x1, y1, x2, y2)


def detect_lanes(frame):
    """
    Detect lane lines and estimate the road center.
    Returns a dictionary with lane geometry.
    """
    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, Config.CANNY_LOW, Config.CANNY_HIGH)

    roi = _region_of_interest(edges)

    lines = cv2.HoughLinesP(
        roi,
        1,
        np.pi / 180,
        Config.HOUGH_THRESHOLD,
        minLineLength=Config.HOUGH_MIN_LINE_LENGTH,
        maxLineGap=Config.HOUGH_MAX_LINE_GAP,
    )

    left_fit, right_fit = _average_slope_intercept(lines)

    # Fallback to synthetic road geometry if Hough fails
    fallback_left, fallback_right, _ = road_bounds_at_y(height - 1)

    left_line = _make_line_points(height, int(height * 0.62), left_fit)
    right_line = _make_line_points(height, int(height * 0.62), right_fit)

    if left_line is None:
        left_line = (fallback_left, height, int(width * 0.42), Config.ROAD_TOP_Y)
    if right_line is None:
        right_line = (fallback_right, height, int(width * 0.58), Config.ROAD_TOP_Y)

    left_bottom_x = clamp(left_line[0], 0, width - 1)
    right_bottom_x = clamp(right_line[0], 0, width - 1)

    road_left_x = min(left_bottom_x, right_bottom_x)
    road_right_x = max(left_bottom_x, right_bottom_x)
    lane_center_x = int((road_left_x + road_right_x) / 2)
    lane_offset = lane_center_x - (width // 2)

    result = {
        "left_line": left_line,
        "right_line": right_line,
        "road_left_x": road_left_x,
        "road_right_x": road_right_x,
        "lane_center_x": lane_center_x,
        "lane_offset": lane_offset,
        "edges": edges,
        "roi_edges": roi,
    }

    return result