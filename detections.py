from ultralytics import YOLO

# Load the model
model = YOLO("yolov8n.pt")

def detect_objects(frame):
    """Detect objects using YOLO and return detections"""
    results = model(frame)
    return results[0].boxes.data
