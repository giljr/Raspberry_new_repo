# cam1.py
# This code opens a camera preview, applies flipping transformations, 
# displays it for 2 seconds, and then closes the camera
# j3 @ Aug, 2024

from picamera2 import Picamera2, Preview
from time import sleep
from libcamera import Transform

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, transform=Transform(hflip=True, vflip=True))
picam2.start()
sleep(2)
picam2.close()