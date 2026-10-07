from ultralytics import YOLO
from PIL import Image

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

model = YOLO("yolov8n.pt")

# relpath="Images/superman.png"
relpath=False
if relpath:
    image = Image.open(relpath)
else:
    image = "0"


results = model.predict(
    source=image,
    show=True,
    save=True,
    verbose=False,
    stream=True
)

if not relpath:
    for result in results:
        for box in result.boxes:
            xmin, ymin, xmax, ymax = map(int,box.xyxy[0])

            confidence = box.conf.item()
            class_id = int(box.cls.item())
            class_name = result.names[class_id]

            center_x = int((xmin + xmax) / 2)
            center_y = int((ymin + ymax) / 2)

            if class_name == "person":
                print(f"{RED}DETECTED {class_name} ({confidence:.2f}) at [{xmin},{ymin},{xmax},{ymax}]. CENTER:({center_x},{center_y}){RESET}")
            else:
                print(f"{BLUE}detected {class_name} ({confidence:.2f}) at [{xmin},{ymin},{xmax},{ymax}]. CENTER:{center_x},{center_y}{RESET}")