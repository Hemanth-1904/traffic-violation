import os
import csv
from config import *

def log_violation(violation_id, violation_type, vehicle_label, timestamp, img_path, video_path):
    """Log the violation details and store images/videos"""
    with open(f"{VIOLATION_DIR}/violation_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([violation_id, violation_type, vehicle_label, timestamp, img_path, video_path])
