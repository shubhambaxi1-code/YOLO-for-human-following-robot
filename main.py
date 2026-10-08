from ultralytics import YOLO
from classcamera import Camera
from classimage import Image

PURPLE = "\033[95m"
RESET = '\033[0m'

model = YOLO("yolov8n.pt") # Can change to higher model if the user's computer has GPU

# Define the source
src = "0" # For live Camera
# src = "ImagePath" For image

# Make camera and image instances
camera = Camera(model=model)
image = Image(model=model)

#Basic error handling
if type(src) == int:
    raise ValueError(f"{PURPLE}The src attribute MUST be a string{RESET}")
try:
    if int(src) == 0: # If user uses camera
        camera.predict(src=src)
except ValueError: # If the above fails, telling us that the user wants to use image
    image.predict(src=src)