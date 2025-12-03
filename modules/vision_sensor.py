import cv2
import sys
import os
import time
import random

# --- IMPORT FIX ---
# This allows the script to find 'config.py' in the parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import VIDEO_PATH

class TrafficEye:
    def __init__(self):
        print(f"\nPriyansh (Vision Sensor): Initializing...")
        
        # 1. Check if the video file exists
        if not os.path.exists(VIDEO_PATH):
            print(f" WARNING: Video file not found at: {VIDEO_PATH}")
            print("    -> Switching to 'Simulation Mode' (Random Data).")
            self.cap = None
        else:
            print(f"    Loading video source: {VIDEO_PATH}")
            self.cap = cv2.VideoCapture(VIDEO_PATH)
            
        # Placeholder for where the Real YOLO Model would load
        # self.model = YOLO("yolov8n.pt") 
        print("Vision System Ready!")

    def get_vehicle_count(self):
        """
        Reads the next video frame and counts the cars.
        """
        count = 0
        
        if self.cap:
            # A. REAL VIDEO MODE
            ret, frame = self.cap.read()
            
            # Loop the video if it ends
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            
            # --- YOLO LOGIC PLACEHOLDER ---
            # In the real version, you would pass 'frame' to the model here.
            # results = self.model(frame)
            # count = len(results[0].boxes)

            # --- SIMULATION LOGIC (For Testing) ---
            # We simulate a traffic jam pattern based on time
            # 0-10 seconds: Clear Traffic
            # 10-20 seconds: Heavy Traffic
            current_time_window = int(time.time()) % 20
            
            if current_time_window > 10:
                count = 45 # Simulate Jam
            else:
                count = 5  # Simulate Free Flow
                
        else:
            # B. NO VIDEO FOUND MODE (Random fallback)
            count = random.randint(5, 50)

        return count

    def get_congestion_factor(self, vehicle_count):
        """
        Converts raw car numbers into a 'Multiplier' for the Map Engine.
        """
        if vehicle_count < 10:
            status = "Free Flow 🟢"
            factor = 1.0  # Normal Speed (No penalty)
            
        elif vehicle_count < 30:
            status = "Moderate 🟡"
            factor = 1.5  # 1.5x slower
            
        else:
            status = "Heavy Jam 🔴"
            factor = 3.0  # 3x slower (Heavy penalty)
            
        return factor, status

# --- TEST BLOCK (Run this file directly to verify) ---
if __name__ == "__main__":
    eye = TrafficEye()
    
    print("\n Starting 5-second Surveillance Test...")
    for i in range(5):
        count = eye.get_vehicle_count()
        factor, status = eye.get_congestion_factor(count)
        
        print(f"    Frame {i+1}: Detected {count} cars -> Status: {status} (Factor: {factor}x)")
        time.sleep(1)