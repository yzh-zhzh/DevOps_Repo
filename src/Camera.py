from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import time
import RPi.GPIO as GPIO
from datetime import datetime
import os

# --- Configuration ---
FIRE_SENSOR_PIN = 17  # Change this to the GPIO pin you're using for fire sensor
SAVE_PATH = "/home/pi/fire_videos"  # Make sure this path exists or gets created
RECORD_DURATION = 10  # Seconds

# --- Setup GPIO ---
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FIRE_SENSOR_PIN, GPIO.IN)

# --- Setup camera ---
def initialize_camera():
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(
        main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores"
    )
    picam2.configure(video_config)
    return picam2

# --- Monitor for fire detection and record ---
def monitor_and_record(picam2):
    print("[INFO] Monitoring for fire...")

    try:
        while True:
            fire_detected = GPIO.input(FIRE_SENSOR_PIN)
            if fire_detected:
                print("[ALERT] Fire detected! Starting recording...")

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(SAVE_PATH, f"fire_{timestamp}.h264")

                encoder = H264Encoder(bitrate=10000000)

                picam2.start_preview(Preview.QTGL)
                picam2.start_recording(encoder, output_file)
                time.sleep(RECORD_DURATION)
                picam2.stop_recording()
                picam2.stop_preview()

                print(f"[INFO] Video saved: {output_file}")
                time.sleep(5)  # delay to prevent multiple triggers

            else:
                time.sleep(1)

    except KeyboardInterrupt:
        print("[INFO] Stopped by user.")
    finally:
        picam2.stop()
        GPIO.cleanup()

# --- Main ---
if __name__ == "__main__":
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    setup_gpio()
    camera = initialize_camera()
    monitor_and_record(camera)
