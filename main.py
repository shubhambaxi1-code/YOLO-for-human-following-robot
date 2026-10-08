from ultralytics import YOLO
from classcamera import Camera
from classimage import Image

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = "\033[95m"
RESET = '\033[0m'

model = YOLO("yolov8n.pt")

src = "Images/cup.png"
camera = Camera(model=model)
image = Image(model=model)

if type(src) == int:
    raise ValueError(f"{PURPLE}The src attribute MUST be a string{RESET}")
try:
    if int(src) == 0:
        camera.predict(src=src)
except ValueError:
    image.predict(src=src)