import cv2
import numpy as np

def detect_traffic_signal_color(frame):
    """Detect the color of the traffic light (Red/Green)"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Red and green color ranges for traffic light detection
    lower_red = np.array([0, 120, 120])
    upper_red = np.array([10, 255, 255])
    
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    red_area = np.sum(mask_red)
    green_area = np.sum(mask_green)

    if red_area > green_area:
        return "RED"
    elif green_area > red_area:
        return "GREEN"
    return "UNKNOWN"
