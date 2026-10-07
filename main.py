from ultralytics import YOLO
from PIL import Image

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

BORDER_PADDING_PCT = 0.15
FAR = 0.40
CLOSE = 0.70

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
        frame_height, frame_width = result.orig_shape

        left_border = int(frame_width * BORDER_PADDING_PCT)
        right_border = int(frame_width * (1.0 - BORDER_PADDING_PCT))

        for box in result.boxes:
            xmin, ymin, xmax, ymax = map(int,box.xyxy[0])

            person_height = ymax - ymin

            confidence = box.conf.item()
            class_id = int(box.cls.item())
            class_name = result.names[class_id]

            center_x = int((xmin + xmax) / 2)
            center_y = int((ymin + ymax) / 2)

            if class_name == "person":
                action = f"{BLUE}Nothing yet{RESET}"
                if center_x < left_border:
                    action = f"{GREEN}TURN LEFT{RESET}"
                elif center_x > right_border:
                    action = f"{GREEN}TURN RIGHT{RESET}"

                elif person_height < (frame_height * FAR):
                    action = f"{GREEN}FORWARD{RESET}"
                elif person_height > (frame_height * CLOSE):
                    action = f"{GREEN}BACKWARD{RESET}"
                print(f"{RED}DETECTED {class_name} ({confidence:.2f}) CENTER:({center_x},{center_y}) {action}{RESET}")
            # else:
            #     print(f"{BLUE}detected {class_name} ({confidence:.2f}) at [{xmin},{ymin},{xmax},{ymax}]. CENTER:{center_x},{center_y}{RESET}")