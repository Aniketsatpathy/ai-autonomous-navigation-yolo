from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # auto downloads

results = model("https://ultralytics.com/images/bus.jpg", show=True)