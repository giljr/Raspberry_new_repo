# cam10.py
#
# The code sets up a Raspberry Pi with a PIR sensor and camera.
# It initializes the camera with a 180-degree rotation and
# ensures the PIR sensor and LED are correctly configured.
# The script detects motion and triggers the camera
# to take a photo if sustained motion is detected,
# ensuring a minimum time between photos.
# The LED lights up when motion is detected,
# and photos are saved to a directory with a timestamp.
# The setup waits for 2 seconds
# for stabilization and handles keyboard interrupts for cleanup.
# 
# j3 @ August, 2024


import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from libcamera import Transform
import os

PIR_PIN = 4
LED_PIN = 17

def take_photo(picam2):
    # Ensure the directory exists
    if not os.path.exists("/home/pi/Camera"):
        os.makedirs("/home/pi/Camera")
    
    file_name = "/home/pi/Camera/img_" + str(time.time()) + ".jpg"
    picam2.capture_file(file_name)
    print(f"Photo saved: {file_name}")
    return file_name

# Setup camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(transform=Transform(rotation=180)))
picam2.start()  # Start the camera

# Pause for 2 seconds to allow the camera to stabilize
time.sleep(2)
print("Camera setup ok.")

# Setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
print("GPIOs setup ok.")

MOV_DETECT_THRESHOLD = 3.0  # Time threshold for sustained motion
MIN_DURATION_BETWEEN_PHOTOS = 60.0  # Minimum time between two photos (in seconds)

last_pir_state = GPIO.input(PIR_PIN)
movement_timer = time.time()
last_time_photo_taken = 0  # Initialize last photo time to 0

print("Everything has been set up.")

try:
    while True:
        time.sleep(0.01)
        pir_state = GPIO.input(PIR_PIN)
        
        # Activate LED when movement is detected.
        GPIO.output(LED_PIN, GPIO.HIGH if pir_state == GPIO.HIGH else GPIO.LOW)

        # Detecting the start of motion
        if last_pir_state == GPIO.LOW and pir_state == GPIO.HIGH:
            movement_timer = time.time()

        # Sustained motion detection
        if last_pir_state == GPIO.HIGH and pir_state == GPIO.HIGH:
            if time.time() - movement_timer > MOV_DETECT_THRESHOLD:
                # Check if enough time has passed since the last photo
                if time.time() - last_time_photo_taken > MIN_DURATION_BETWEEN_PHOTOS:
                    print("Take Photo and Send it by Email")
                    take_photo(picam2)
                    last_time_photo_taken = time.time()  # Update the last photo taken time

        last_pir_state = pir_state

except KeyboardInterrupt:
    GPIO.cleanup()
    picam2.stop()
