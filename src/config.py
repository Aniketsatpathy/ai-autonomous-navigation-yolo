class Config:
    # Frame / simulation settings
    FRAME_WIDTH = 960
    FRAME_HEIGHT = 540
    FPS = 30

    # Road geometry
    ROAD_TOP_Y = 110
    ROAD_TOP_WIDTH = 220
    ROAD_BOTTOM_WIDTH = 720
    LANE_COUNT = 3

    # Simulation colors (BGR)
    BACKGROUND_COLOR = (25, 25, 25)
    ROAD_COLOR = (55, 55, 55)
    ROAD_EDGE_COLOR = (90, 90, 90)
    LANE_MARKER_COLOR = (255, 255, 255)
    EGO_COLOR = (255, 140, 0)
    OBSTACLE_COLOR = (0, 0, 255)
    PATH_COLOR = (0, 255, 0)
    PANEL_BG_COLOR = (0, 0, 0)
    PANEL_TEXT_COLOR = (255, 255, 255)

    # Obstacles
    NUM_OBSTACLES = 3
    OBSTACLE_MIN_SPEED = 4.0
    OBSTACLE_MAX_SPEED = 7.0

    # Detection / planning
    CANNY_LOW = 50
    CANNY_HIGH = 150
    HOUGH_THRESHOLD = 35
    HOUGH_MIN_LINE_LENGTH = 30
    HOUGH_MAX_LINE_GAP = 15
    STOP_DISTANCE_PX = 90
    LANE_OFFSET_TOLERANCE = 25
    LOOKAHEAD_ROWS = 8

    # Output
    OUTPUT_DIR = "outputs"
    RESULT_VIDEO_PATH = "outputs/result_videos/demo_output.avi"
    LOG_PATH = "outputs/logs/run_log.csv"

    # Optional YOLO mode for later upgrade
    OBSTACLE_DETECTION_MODE = "color"  # "color" or "yolo"
    YOLO_MODEL_PATH = "yolov8n.pt"