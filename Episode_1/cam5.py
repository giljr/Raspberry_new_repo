# cam5.py
# This script captures an image with a Raspberry Pi camera, 
# flips it both horizontally and vertically, 
# and overlays the current date and time in the bottom-right corner.
# The apply_text function dynamically calculates 
# the text's position using OpenCV. 
# The camera is configured for preview and capture modes 
# with the same resolution to maintain overlay consistency. 
# The picam2.pre_callback inserts the timestamp before capturing the image, 
# which is then saved as timeOnPhoto.jpg.
# j3 @ Aug, 2024s

from picamera2 import Picamera2, MappedArray
from libcamera import Transform
import cv2, time

resolution = (800, 600)


def apply_text(request):
    # Text options
    colour = (255, 255, 255)
    origin = (0, 60)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    thickness = 1
    # text = "17082024 09:07"
    # Get the current time in the format "DDMMYYYY HH:MM"
    text = time.strftime("%d%m%Y %H:%M")
    # Calculate the text size
    text_size, _ = cv2.getTextSize(text, font, scale, thickness)
                    
    # Calculate the bottom-right origin
    x = resolution[0] - text_size[0] - 10  # 10 pixels padding from the right
    y = resolution[1] - 10  # 10 pixels padding from the bottom
                    
    origin = (x, y)
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, text, origin, font, scale, colour, thickness)


# Create camera object
picam2 = Picamera2()

# Create two separate configs - one for preview and one for capture.
# Make sure the preview is the same resolution as the capture, to make
# sure the overlay stays the same size
capture_config = picam2.create_still_configuration({"size": resolution}, transform=Transform(hflip=True, vflip=True))
preview_config = picam2.create_preview_configuration({"size": resolution}, transform=Transform(hflip=True, vflip=True))

# Set the current config as the preview config
picam2.configure(preview_config)

# Add the timestamp
picam2.pre_callback = apply_text
# Start the camera
picam2.start(show_preview=True)
time.sleep(2)

# Switch to the capture config and then take a picture
image = picam2.switch_mode_and_capture_file(capture_config, "timeOnPhoto.jpg")

# Close the camera
picam2.close()
