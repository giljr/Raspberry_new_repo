# cam12.py
# 
# Description:
#
# The script uses a Raspberry Pi with a PIR sensor,
# LED, and camera to detect motion and capture photos.
# When motion is detected, the camera takes a photo with
# a timestamp overlay using OpenCV, and the image is saved
# to a specified directory.
# The script ensures necessary directories exist for image
# and log storage, and controls the LED based on motion detection.
# It continuously monitors the PIR sensor,
# taking a new photo only if a specified duration
# has passed since the last capture.
#
# j3 @ Aug, 2024

import RPi.GPIO as GPIO
import time, cv2
from picamera2 import Picamera2, MappedArray
from libcamera import Transform
import os
import yagmail

PIR_PIN = 4
LED_PIN = 17
resolution = (800, 600)
LOG_FILE_NAME = "/home/pi/Camera/log/photo_logs.txt"

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

def take_photo(picam2):
    # Ensure the directory exists
    if not os.path.exists("/home/pi/Camera"):
        os.makedirs("/home/pi/Camera")
    
    file_name = "/home/pi/Camera/img_" + str(time.time()) + ".jpg"
    #     picam2.capture_file(file_name)
    picam2.switch_mode_and_capture_file(capture_config, file_name)
    print(f"Photo saved: {file_name}")
    return file_name

# Ensure that the directory exists before attempting to write to the log file
def update_photo_log_file(photo_file_name):
    # Ensure the directory exists
    log_directory = os.path.dirname(LOG_FILE_NAME)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    with open(LOG_FILE_NAME, "a") as f:
        f.write(photo_file_name)
        f.write("\n")
        
def send_email_with_photo(yagmail_client, file_name):
    yagmail_client.send(to="giljr.2009@gmail.com",
                        subject="Movement detected!",
                        contents="Here's a photo taken by your Raspberry Pi",
                        attachments=file_name)
        
# Setup camera
picam2 = Picamera2()
# picam2.configure(picam2.create_still_configuration(transform=Transform(rotation=180)))
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
picam2.start(show_preview=False)
picam2.start()  # Start the camera

# Pause for 2 seconds to allow the camera to stabilize
time.sleep(2)
print("Camera setup ok.")

# Remove log file
if os.path.exists(LOG_FILE_NAME):
    os.remove(LOG_FILE_NAME)
    print("Log file removed.")
    
# Setup yagmail
password = "ogof orem rzqf dppx"
#with open("/home/pi/.local/share/.email_password", "r") as f:
#    password = f.read()
yag = yagmail.SMTP("giljr.2009@gmail.com", password)
print("Email sender setup OK.")

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
                    photo_file_name = take_photo(picam2)
                    update_photo_log_file(photo_file_name)
                    send_email_with_photo(yag, photo_file_name)
                    last_time_photo_taken = time.time()  # Update the last photo taken time

        last_pir_state = pir_state

except KeyboardInterrupt:
    GPIO.cleanup()
    picam2.stop()
