# cam7.py
#
# Description:
# The script sets up a Raspberry Pi to detect
# motion using a PIR sensor connected to GPIO pin 4.
# It monitors the sensor for changes in state and
# triggers an action if sustained motion is detected
# for longer than a specified threshold (MOV_DETECT_THRESHOLD).
# It also ensures that photos are only taken if a minimum
# interval (MIN_DURATION_BETWEEN_PHOTOS) has passed since
# the last photo was taken. The script prints a message
# when these conditions are met. On interruption,
# it cleans up the GPIO setup.
# 
# j3 @ August, 2024

import RPi.GPIO as GPIO
import time

PIR_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

MOV_DETECT_THRESHOLD = 3.0  # Time threshold for sustained motion
MIN_DURATION_BETWEEN_PHOTOS = 5.0  # Minimum time between two photos (in seconds)

last_pir_state = GPIO.input(PIR_PIN)
movement_timer = time.time()
last_time_photo_taken = 0  # Initialize last photo time to 0

try:
    while True:
        time.sleep(0.01)
        pir_state = GPIO.input(PIR_PIN)
        
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