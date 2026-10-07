from ultralytics import YOLO # Import YOLO
from PIL import Image # Import Image from Pillow module

# Colours for printing
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

# Setting borders for left/right/up/down suggestions
BORDER_PADDING_PCT = 0.15
FAR = 0.40
CLOSE = 0.70

# Create instance of Model
model = YOLO("yolov8n.pt") # Can use higher model for better accuracy if computer has GPU

# Use relpath=False for using camera 
# Use relpath="Image Path" for using image
#NOTE: Using relpath as False will allow left/right/up/down suggestions. Putting an image path will act similar to normal object detection. It is suggested to use a camera by entering relpath=False

# Set relpath
relpath=False

# Automatically set relpath as 0 if no value/False entered, to work with YOLO.
if not relpath:
    image = "0"

# Object Detection

if not relpath: # If no value in relpath is entered
    results = model.predict(
        source=image, # Use Camera
        show=True, # Show Window
        save=True, # Save the file
        verbose=False, # Do not print statements automatically*
        stream=True # Allow to become python generator*
    )
else: # If image path is given in relpath
    with Image.open(relpath) as image:
        results = model.predict(
                source=image, # Use Image
                show=True, # Show Image
                save=True, # Save Image
            )

if not relpath:
    for result in results:
        frame_height, frame_width = result.orig_shape # Set frame height and width

        #Border Definitions
        left_border = int(frame_width * BORDER_PADDING_PCT)
        right_border = int(frame_width * (1.0 - BORDER_PADDING_PCT))

        for box in result.boxes:
            xmin, ymin, xmax, ymax = map(int,box.xyxy[0]) # Find positions of corners of Binding Box

            person_height = ymax - ymin 

            confidence = box.conf.item()
            class_id = int(box.cls.item())
            class_name = result.names[class_id]

            # Find bounding box's center (x,y)
            center_x = int((xmin + xmax) / 2) 
            center_y = int((ymin + ymax) / 2)

            if class_name == "person": # If person is detected
                action = f"{BLUE}Idle{RESET}" # Set default value of action to stay idle

                if person_height < (frame_height * FAR):
                    action = f"{GREEN}FORWARD{RESET}"
                elif person_height > (frame_height * CLOSE):
                    action = f"{GREEN}BACKWARD{RESET}"

                elif center_x < left_border:
                    action = f"{GREEN}TURN LEFT{RESET}"
                elif center_x > right_border:
                    action = f"{GREEN}TURN RIGHT{RESET}"

                # Print Statement
                print(f"{RED}DETECTED {class_name} ({confidence:.2f}) CENTER:({center_x},{center_y}) {action}{RESET}")