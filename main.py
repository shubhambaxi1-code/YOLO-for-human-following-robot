from ultralytics import YOLO
from classcamera import Camera
from classimage import Image

PURPLE = "\033[95m"
RESET = '\033[0m'

model = YOLO("yolov8n.pt") # Can change to higher model if the user's computer has GPU

# Define the source
src = 0 # For live Camera
#NOTE: ONLY ENTER A VALID NUMBER FOR SOURCE TO PREVENT ERRORS
# src = "ImagePath" For image

# Make camera and image instances
camera = Camera(model=model)
image = Image(model=model)

#Basic error handling
try:
    if type(src) == int: # If user uses camera
        camera.predict(src=src)
    else:
        image.predict(src=src)
except ConnectionError:
    print(f"{PURPLE}The src of the image cannot be opened. Please ensure that you have {src+1} camera(s) and system has given permission for usage of the camera{RESET}")
except FileNotFoundError:
    print(f"{PURPLE}The file \"{src}\" cannot be found. Please ensure that the file is valid and existing.{RESET}")
except KeyboardInterrupt:
    print(f"{PURPLE}\nTHE PROGRAM HAS STOPPED{RESET}")

