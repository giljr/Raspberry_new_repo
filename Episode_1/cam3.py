# cam3.py
# This code configures the Raspberry Pi camera 
# with maximum resolution (2592x1944), 
# flips the image both horizontally and vertically, 
# and sets the preview size to 800x600. 
# The camera starts in preview mode, waits 2 seconds, 
# captures an image named "img2.jpg," and then closes the camera.
# j3 @ Aug, 2024

from picamera2 import Picamera2
from libcamera import Transform
from time import sleep

picam2 = Picamera2()

# Sets the resolution of the sensor output to the maximum
# resolution of the camera sensor, which is 2592x1944 pixels.
# This ensures that the captured image will be of high quality.
picam2.preview_configuration.sensor.output_size = (2592, 1944)

# Sets the size of the preview window to 800x600 pixels.
# This controls the size of the image displayed on the screen
# while the camera is running in preview mode.
picam2.preview_configuration.main.size = (800, 600)

# Apply the transform to flip the image horizontally and vertically
picam2.preview_configuration.transform = Transform(hflip=True, vflip=True)

# Configure the camera for preview
picam2.configure("preview")

# Start the camera with the preview
picam2.start(show_preview=True)

# Pause for 2 seconds to allow the camera to stabilize
sleep(2)

# Capture the image and save it as 'max.jpg'
picam2.capture_file("img2.jpg")

# Close the camera
picam2.close()