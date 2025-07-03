def is_vehicle_opposite_direction(vehicle_box, frame_width):
    """Check if the vehicle is moving in the opposite direction of the traffic signal"""
    x1, _, x2, _, _, _ = vehicle_box
    vehicle_center_x = (x1 + x2) // 2
    return vehicle_center_x < frame_width // 2
