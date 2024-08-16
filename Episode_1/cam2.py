# cam2.py
# This code initializes the Raspberry Pi camera using the Picamera2 library. 
# It creates a video configuration with both horizontal and 
# vertical flipping applied via the Transform class. 
# The camera is configured with this setup and then starts recording 
# a 5-second video saved as "new_video.mp4", with an optional preview display. 
# After recording, the camera is closed to stop the session and release resources.
# j3 @ Aug, 2024

from picamera2 import Picamera2
from libcamera import Transform

picam2 = Picamera2()

# Create a video configuration and apply the transform for flipping
video_config = picam2.create_video_configuration(transform=Transform(hflip=True, vflip=True))
picam2.configure(video_config)

picam2.start_and_record_video("new_video.mp4", duration=5, show_preview=True)
picam2.close()