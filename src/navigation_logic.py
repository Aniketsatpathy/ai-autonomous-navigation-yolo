from .config import Config
from .utils import clamp


def _lane_index_from_x(x, road_left_x, road_right_x):
    if road_right_x <= road_left_x:
        return 1

    lane_width = (road_right_x - road_left_x) / Config.LANE_COUNT
    idx = int((x - road_left_x) / lane_width)
    return clamp(idx, 0, Config.LANE_COUNT - 1)


def decide_navigation(lane_info, obstacles, plan, frame_width, frame_height):
    """
    Convert perception + planning into action
    """

    road_left_x = lane_info["road_left_x"]
    road_right_x = lane_info["road_right_x"]
    lane_offset = lane_info["lane_offset"]

    current_lane = 1
    next_lane = plan["next_lane"]

    # 🔴 Check for close obstacle
    for obj in obstacles:
        x1, y1, x2, y2 = obj["bbox"]
        cx, cy = obj["center"]

        lane_idx = _lane_index_from_x(cx, road_left_x, road_right_x)

        distance = frame_height - y2

        if lane_idx == current_lane and distance < Config.STOP_DISTANCE_PX:
            return {
                "action": "STOP",
                "steering": 0.0,
                "speed": 0.0,
                "reason": "Obstacle too close"
            }

    # 🟢 Planner-based decision
    if next_lane < current_lane:
        return {
            "action": "STEER_LEFT",
            "steering": -0.6,
            "speed": 0.6,
            "reason": "Planner chose left"
        }

    elif next_lane > current_lane:
        return {
            "action": "STEER_RIGHT",
            "steering": 0.6,
            "speed": 0.6,
            "reason": "Planner chose right"
        }

    # ⚖️ Lane correction
    if abs(lane_offset) > Config.LANE_OFFSET_TOLERANCE:
        if lane_offset < 0:
            return {
                "action": "ADJUST_LEFT",
                "steering": -0.3,
                "speed": 0.8,
                "reason": "Lane correction left"
            }
        else:
            return {
                "action": "ADJUST_RIGHT",
                "steering": 0.3,
                "speed": 0.8,
                "reason": "Lane correction right"
            }

    # ✅ Default
    return {
        "action": "FORWARD",
        "steering": 0.0,
        "speed": 1.0,
        "reason": "Path clear"
    }