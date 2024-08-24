# cam9.py
#
# Description:
# Here's a concise summary of the code:
# Camera Setup: Configures the Raspberry Pi camera with 720x480 resolution and 180-degree rotation, allowing 2 seconds for stabilization.
# GPIO Configuration: Sets up GPIO pins for the PIR sensor and LED, initially turning off the LED.
# Motion Detection: Detects motion using the PIR sensor and toggles the LED when movement is sensed.
# Photo Timing: Manages photo capture intervals, ensuring photos are taken only after a set time has elapsed.
# Exception Handling: Cleans up GPIO settings upon script interruption for proper shutdown.
# 
# j3 @ August, 2024

import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2

PIR_PIN = 4
LED_PIN = 17


# Setup camera
camera = Picamera2()
camera.resolution = (720, 480)
camera.rotation = 180
print("Waiting 2 seconds to init the camera...")
time.sleep(2)
print("Camera setup ok.")

# Setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO. setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
print("GPIOs setup ok.")

MOV_DETECT_THRESHOLD = 3.0  # Time threshold for sustained motion
MIN_DURATION_BETWEEN_PHOTOS = 5.0  # Minimum time between two photos (in seconds)

last_pir_state = GPIO.input(PIR_PIN)
movement_timer = time.time()
last_time_photo_taken = 0  # Initialize last photo time to 0

print("Everything has been setup.")

try:
    while True:
        time.sleep(0.01)
        pir_state = GPIO.input(PIR_PIN)
        # Activate LED when movement is detected.
        if pir_state == GPIO.HIGH:
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        
        # Detecting the start of motion
        if last_pir_state == GPIO.LOW and pir_state == GPIO.HIGH:
            movement_timer = time.time()

        # Sustained motion detection
        if last_pir_state == GPIO.HIGH and pir_state == GPIO.HIGH:
            if time.time() - movement_timer > MOV_DETECT_THRESHOLD:
                # Check if enough time has passed since the last photo
                if time.time() - last_time_photo_taken > MIN_DURATION_BETWEEN_PHOTOS:
                    print("Take Photo and Send it by Email")
                    last_time_photo_taken = time.time()  # Update the last photo taken time
        
        last_pir_state = pir_state

except KeyboardInterrupt:
    GPIO.cleanup()