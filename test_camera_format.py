from picamera2 import Picamera2
from time import sleep
import argparse


def create_config(main_width, main_height):
    config = camera.create_video_configuration(
        main={"size": (main_width, main_height)},
    )
    return config

parser = argparse.ArgumentParser(prog="Test Camera Format")
parser.add_argument("-W", "--width", type=int, default=1920, required=False)
parser.add_argument("-H", "--height", type=int, default=1080, required=False)
args = parser.parse_args()

camera = Picamera2()

config = create_config(args.width,  args.height)
try:
    camera.configure(config)
    camera.start()
    sleep(3)
    print(f"working at {args.width} {args.height}")
    camera.stop()
except:
    print(f"error")