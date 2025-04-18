# === MOTION DETECTION + DISCORD VIDEO UPLOAD ===
import cv2
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
import os
from Discord_Bot import send_video_to_discord

# === LOAD SECRETS FROM .ENV ===
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

cap = cv2.VideoCapture(0)       # Opens the default webcam
last_mean = 0       # Sets the first mean brightness as zero (so motion is not immediately registered)
frame_rec_count = 0  # Counts number of frames recorded
# Starting everything as empty:
motion_started = False      # Check for whether motion is currently being recorded
video_object = None         # Object that video will be captured to 
filename = None       # Stores the filename of the current video
save_to_folder = r"C:\Users\Erin\webcam website\videos"     # Save videos to their own folder
video_data = []

# === Main loop: continuously capture and process webcam frames ===
while(True):

    ret, frame = cap.read()     # Read each new frame from the webcam
    if not ret:
        break       # Stop loop if the webcam fails

    # Convert the frame to grayscale and compare brightness with the previous frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    result = np.abs(np.mean(gray) - last_mean) 
    last_mean = np.mean(gray) 

    # === Motion Detected: start recording ===
    if not motion_started and result > 0.35: 
        print("motion detected")
        motion_started = True

        # logic for creating each new video:
        video_id = datetime.now().strftime("%Y%m%d_%H%M%S")         # Unique filename based on timestamp
        filename = f'{video_id}.avi'      # Create a .avi file
        video_timestamp = datetime.now().strftime("%B-%d-%Y-at-%I:%M:%S %p")       # Displays the timestamp in a readable string format
        video_data = video_timestamp      # Add the filename and full time stamp to a list

        # creating the videos and saving them to the /videos folder
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        save_path = os.path.join(save_to_folder, filename)      # Save videos to their own folder
        video_object = cv2.VideoWriter(save_path, fourcc, 20.0, (640, 480))

    # === If the recording is still active, keep writing frames ===
    if motion_started and video_object is not None:
        video_object.write(frame)       # Capture New Video
        frame_rec_count += 1 
        print(f"recording frame: {frame_rec_count}")

         # === Every 300 frames (15 sec), check if motion has stopped ===
        if frame_rec_count >= 300: 
            print("300 frames passed. Checking for continued motion")
            if result < 0.35:       # Motion has stopped
                print("motion stopped. Stopping the video")
                video_object.release()      # Save the video
                send_video_to_discord(save_path, DISCORD_TOKEN, CHANNEL_ID, video_data)        # Discord Bot uploads video
                # Reset the tracking variables:
                video_object = None
                motion_started = False
                frame_rec_count = 0
            else:       # Motion is still ongoing
                ("there is still motion. resetting the frame count")
                frame_rec_count = 0     # Reset the counter (continuing the 15 sec loop)

# === Ending the program if the webcam fails ===
cap.release()
cv2.destroyAllWindows()