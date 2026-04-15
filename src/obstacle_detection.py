from ultralytics import YOLO

class ObstacleDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        results = self.model(frame, verbose=False)

        detections = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                label = self.model.names[cls_id]

                if conf < 0.5:
                    continue

                # Filter useful objects
                if label in ["car", "truck", "bus", "person", "motorcycle", "bicycle"]:
                    detections.append({
                        "label": label,
                        "confidence": conf,
                        "bbox": (x1, y1, x2, y2),
                        "center": ((x1+x2)//2, (y1+y2)//2)
                    })

        return detections