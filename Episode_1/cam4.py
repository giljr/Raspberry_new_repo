# cam4.py
# This code captures an image using the Raspberry Pi camera,
# flips it, and saves it as "toProcess.jpg."
# It then reads the image with OpenCV,
# converts it to a sketch-like image
# using grayscale, inversion, and blurring techniques,
# and saves the result as "sketchImage.jpg."
# The camera configuration includes a flipped preview with specified dimensions.
# j3 @ Aug, 2024

from picamera2 import Picamera2
from time import sleep
from libcamera import Transform
import cv2

picam2 = Picamera2()

# Create a video configuration and apply the transform for flipping
video_config = picam2.create_video_configuration(transform=Transform(hflip=True, vflip=True))
picam2.configure(video_config)

# Set the resolution for 800 x 600
picam2.preview_configuration.size = (800, 600)
picam2.start(show_preview=True)

sleep(2)

picam2.capture_file("toProcess.jpg")
picam2.close()

img = cv2.imread("toProcess.jpg")

# Convert to sketch
greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
inverted = 255 - greyscale
blur_inverted = cv2.GaussianBlur(inverted, (125, 125), 0)
inverted_blur = 255 - blur_inverted
sketch = cv2.divide(greyscale, inverted_blur, scale=256)
cv2.imwrite("sketchImage.jpg", sketch)
