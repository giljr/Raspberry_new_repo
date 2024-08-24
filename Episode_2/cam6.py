# cam6.py
#
# Description:
# This script uses a Raspberry Pi GPIO pin
# to monitor a PIR sensor for motion detection.
# It sets up the PIR sensor on pin 4,
# continuously checks the sensor's state,
# and measures the duration of detected motion.
# If motion is sustained beyond a defined threshold (MOV_DETECT_THRESHOLD),
# it triggers a photo capture and email notification.
# The GPIO.cleanup() call ensures that GPIO settings
# are reset if the script is interrupted.
#
# j3 @ Aug, 2024

import RPi.GPIO as GPIO
import time

PIR_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

MOV_DETECT_THREASHOLD = 3.0
last_pir_state = GPIO.input(PIR_PIN)
movement_timer = time.time()

try:
    while True:
        time.sleep(0.01)
        pir_state = GPIO.input(PIR_PIN)
        if last_pir_state == GPIO.LOW and pir_state == GPIO.HIGH:
            movement_timer = time.time()
        if last_pir_state == GPIO.HIGH and pir_state == GPIO.HIGH:
            if time.time() - movement_timer > MOV_DETECT_THREASHOLD:
                print("Take Photo and Send it by Email")
        last_pir_state = pir_state
except KeyboardInterrupt:
    GPIO.cleanup()