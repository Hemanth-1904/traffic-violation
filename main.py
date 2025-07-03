import cv2
import time
import os
import csv
from detections import detect_objects
from traffic_signals import detect_traffic_signal_color
from stopline_detector import detect_stop_line
from lane_violation import check_lane_violation
from violation_logger import log_violation
from utils import is_vehicle_opposite_direction
from config import *
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Use yolov8s.pt, yolov8m.pt etc. if needed

# Initialize variables
violation_count = 0
frame_rate = FRAME_RATE
recording = False
video_writer = None
frame_count = 0
key_frame_count = 0

# Open video file
cap = cv2.VideoCapture("sample_datasets/videos/sample2.mp4")

# Create required folders
os.makedirs(f"{VIOLATION_DIR}/images/red_light", exist_ok=True)
os.makedirs(f"{VIOLATION_DIR}/images/lane_violation", exist_ok=True)
os.makedirs(f"{VIOLATION_DIR}/videos/red_light", exist_ok=True)
os.makedirs(f"{VIOLATION_DIR}/videos/lane_violation", exist_ok=True)

# Ensure CSV log file exists
csv_file = f"{VIOLATION_DIR}/violation_log.csv"
try:
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Violation_ID", "Violation_Type", "Vehicle_Type", "Time", "Image_Path", "Video_Path"])
except PermissionError as e:
    print(f"[ERROR] Cannot write to CSV log file: {e}")
    exit(1)

# Main processing loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    annotated_frame = frame.copy()

    # Detect traffic signal state
    signal_state = detect_traffic_signal_color(frame)

    # Detect stop line position
    stop_line_y = detect_stop_line(frame)

    # Run YOLO detection
    detections = detect_objects(frame)

    for box in detections:
        x1, y1, x2, y2, conf, cls = box
        label = model.names[int(cls)]

        # Check direction and stop line crossing
        if is_vehicle_opposite_direction(box, frame.shape[1]) and y1 > stop_line_y:

            # Red light violation
            if signal_state == "RED":
                if not recording:
                    violation_count += 1
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    video_path = f"{VIOLATION_DIR}/videos/red_light/violation_{violation_count}_{timestamp}.mp4"
                    video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (frame.shape[1], frame.shape[0]))
                    recording = True
                    frame_count = 0
                    key_frame_count = 0

                video_writer.write(frame)
                frame_count += 1

                if frame_count % (frame_rate * 2) == 0 and key_frame_count < 5:
                    key_frame_count += 1
                    img_name = f"{VIOLATION_DIR}/images/red_light/violation_{violation_count}_{key_frame_count}.jpg"
                    cv2.imwrite(img_name, frame)
                    try:
                        log_violation(violation_count, "Red Light", label, timestamp, img_name, video_path)
                    except PermissionError as e:
                        print(f"[WARNING] Skipped logging: {e}")

                

            # Lane violation
            elif check_lane_violation(frame, x1, y1, x2, y2):
                violation_count += 1
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                img_name = f"{VIOLATION_DIR}/images/lane_violation/violation_{violation_count}_{timestamp}.jpg"
                video_path = f"{VIOLATION_DIR}/videos/lane_violation/violation_{violation_count}_{timestamp}.mp4"
                cv2.imwrite(img_name, frame)
                try:
                    log_violation(violation_count, "Lane Violation", label, timestamp, img_name, video_path)
                except PermissionError as e:
                    print(f"[WARNING] Skipped logging: {e}")
                cv2.putText(annotated_frame, "🚨 Lane Violation!", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Stop recording after 10 seconds
    if recording and frame_count > frame_rate * 10:
        if video_writer is not None:
            video_writer.release()
        recording = False

    # Show annotated frame
    cv2.imshow("Traffic Violation Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
if video_writer is not None:
    video_writer.release()
cap.release()
cv2.destroyAllWindows()
