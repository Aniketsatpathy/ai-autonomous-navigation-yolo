from src.main import run

if __name__ == "__main__":
    print("🔥 Starting project...")

    run(
        num_frames=600,
        display=True,
        save_video=True,
        obstacle_mode="color"
    )