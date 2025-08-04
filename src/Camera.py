from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import time
import RPi.GPIO as GPIO
from datetime import datetime
import os
SAVE_PATH = "/home/pi/fire_videos"
def camera_thread(system_state):
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(
        main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores"
    )
    picam2.configure(video_config)
    encoder = H264Encoder(bitrate=10000000)
    recording = False

    while True:
        if system_state['fire_detected'] and not system_state.get('motor_locked', False):
            if not recording:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(SAVE_PATH, f"fire_{timestamp}.h264")
                print("[Camera] Fire detected! Starting recording...")
                picam2.start_preview(Preview.QTGL)
                picam2.start_recording(encoder, output_file)
                recording = True
        else:
            if recording:
                print("[Camera] Stopping recording...")
                picam2.stop_recording()
                picam2.stop_preview()
                recording = False
        time.sleep(0.5)