import csv
import os
from datetime import datetime


class CSVLogger:
    """
    Simple CSV logger for frame-by-frame decisions.
    """

    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

        self.file = open(path, "w", newline="", encoding="utf-8")
        self.fieldnames = [
            "timestamp",
            "frame_index",
            "action",
            "speed",
            "steering",
            "lane_offset",
            "obstacle_count",
            "fallback_used",
            "reason",
        ]
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def log(self, frame_index, command, lane_info, obstacles, plan):
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "frame_index": frame_index,
            "action": command["action"],
            "speed": command["speed"],
            "steering": command["steering"],
            "lane_offset": lane_info["lane_offset"],
            "obstacle_count": len(obstacles),
            "fallback_used": plan["fallback_used"],
            "reason": command["reason"],
        }
        self.writer.writerow(row)
        self.file.flush()

    def close(self):
        if not self.file.closed:
            self.file.close()