# cam8.py
#
# Description:
# This script sets up a Raspberry Pi to use a PIR sensor
# and an LED for motion detection.
# It initializes GPIO pins for the PIR sensor and LED,
# and continuously checks for motion.
# When motion is detected and sustained for a specified duration,
# it prints a message to take a photo and simulates a sending it by email,
# ensuring photos are taken at least a set interval apart.
# The LED lights up when motion is detected, providing a visual alert.
# 
# j3 @ August, 2024

import RPi.GPIO as GPIO
import time

PIR_PIN = 4
LED_PIN = 17

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