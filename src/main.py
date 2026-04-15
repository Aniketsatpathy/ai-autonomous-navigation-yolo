import cv2
import os

from .config import Config
from .utils import ensure_directories
from .lane_detection import detect_lanes
from .obstacle_detection import ObstacleDetector
from .path_planning import LanePathPlanner
from .navigation_logic import decide_navigation
from .visualization import draw_dashboard
from .logger import CSVLogger


def run(num_frames=600, display=True, save_video=True, obstacle_mode=Config.OBSTACLE_DETECTION_MODE):
    ensure_directories()

    # 🔥 Optimization settings
    FRAME_WIDTH = 480
    FRAME_HEIGHT = 270
    DISPLAY_WIDTH = 960
    DISPLAY_HEIGHT = 540
    FRAME_SKIP = 2   # 🔥 Process every 2nd frame

    # 🔥 Initialize YOLO detector
    detector = ObstacleDetector()

    # 🔥 Initialize planner & logger
    planner = LanePathPlanner(rows=Config.LOOKAHEAD_ROWS, lanes=Config.LANE_COUNT)
    logger = CSVLogger(Config.LOG_PATH)

    # 🔥 Load video
    cap = cv2.VideoCapture("data/test_videos/road.mp4")

    if not cap.isOpened():
        print("❌ Error: Cannot open video file")
        return

    writer = None
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        writer = cv2.VideoWriter(
            Config.RESULT_VIDEO_PATH,
            fourcc,
            Config.FPS,
            (DISPLAY_WIDTH, DISPLAY_HEIGHT),  # ✅ FIXED SIZE
        )

        if not writer.isOpened():
            print("[WARN] Could not open video writer.")
            writer = None

    print("\n🚀 Optimized REAL VIDEO simulation...")
    print("Press Q to quit.\n")

    frame_index = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("✅ End of video reached.")
                break

            # 🔥 Resize once (used everywhere)
            original_frame = frame.copy()

            # Resize for processing
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

            # 🔥 FRAME SKIPPING (MAJOR SPEED BOOST)
            if frame_index % FRAME_SKIP != 0:
                frame_index += 1
                continue

            # ================= PIPELINE =================

            # Lane Detection
            lane_info = detect_lanes(frame)

            # YOLO Detection
            obstacles = detector.detect(frame)

            # Path Planning
            plan = planner.plan(FRAME_WIDTH, FRAME_HEIGHT, lane_info, obstacles)

            # Navigation Decision
            command = decide_navigation(
                lane_info=lane_info,
                obstacles=obstacles,
                plan=plan,
                frame_width=FRAME_WIDTH,
                frame_height=FRAME_HEIGHT,
            )

            # Visualization
            annotated = draw_dashboard(frame, lane_info, obstacles, plan, command, frame_index)
            # 🔥 Upscale for better visibility
            display_frame = cv2.resize(annotated, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
           
            # Save video
            if writer is not None:
                writer.write(display_frame)

            # Logging
            logger.log(frame_index, command, lane_info, obstacles, plan)

            # Display
            if display:
                cv2.imshow("AI-Based Autonomous Navigation System", display_frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print("⛔ Stopped by user.")
                    break

            # Debug logs
            if frame_index % 30 == 0:
                print(
                    f"Frame {frame_index:04d} | Action={command['action']:<12} "
                    f"| Objects={len(obstacles)} | Fallback={plan['fallback_used']}"
                )

            frame_index += 1

            if frame_index >= num_frames:
                break

    finally:
        logger.close()
        cap.release()

        if writer is not None:
            writer.release()

        if display:
            cv2.destroyAllWindows()

    print("\n✅ Simulation finished.")
    if save_video:
        print(f"🎥 Saved video: {Config.RESULT_VIDEO_PATH}")
    print(f"📊 Saved logs:   {Config.LOG_PATH}")