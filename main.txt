from ultralytics import YOLO # Import YOLO

# Colours for printing
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = "\033[95m"
RESET = '\033[0m'

# Setting borders for left/right/up/down suggestions
BORDER_PADDING_PCT = 0.15
FAR = 0.40
CLOSE = 0.70

# Create instance of Model
model = YOLO("yolov8n.pt") # Can use higher model for better accuracy if computer has GPU

# Use src="0" for using camera 
# Use src="Image Path" for using image
#NOTE: Using src as False will allow left/right/up/down suggestions. Putting an image path will act similar to normal object detection. It is suggested to use a camera by entering src=False

# Set src
src="0" # For camera usage
if type(src) == int:
    raise ValueError(f"{PURPLE}The src attribute MUST be a string{RESET}")
# src="FilePath" For image usage

# Object Detection

if src == "0": # If 0 in src is entered
    results = model.predict(
        source=src, # Use Camera
        show=True, # Show Window
        save=True, # Save the file
        verbose=False, # Do not print statements automatically*
        stream=True # Allow to become python generator*
    )
else: # If image path is given in src
    try:
        results = model.predict(
                source=src, # Use Image
                show=True, # Show Image
                save=True, # Save Image
            )
    except FileNotFoundError:
        print(f"{PURPLE}The file \"{src}\" does not exist. Please change the src attribute{RESET}")
        
try:
    if src == "0":
        for result in results:
            if result:
                frame_height, frame_width = result.orig_shape # Set frame height and width

                #Border Definitions
                left_border = int(frame_width * BORDER_PADDING_PCT)
                right_border = int(frame_width * (1.0 - BORDER_PADDING_PCT))

                ids = []
                for box in result.boxes:
                    xmin, ymin, xmax, ymax = map(int,box.xyxy[0]) # Find positions of corners of Binding Box

                    person_height = ymax - ymin 

                    confidence = box.conf.item()
                    class_id = int(box.cls.item())
                    class_name = result.names[class_id]

                    ids.append(class_name)

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
                if "person" not in ids and ids:
                    print(f"{BLUE}No people found{RESET}")

except FileNotFoundError:
    print(f"{PURPLE}The src value is entered as \"{src}\". The image path may be incorrect or the src variable may be blank. Please fix this error{RESET}")
except ConnectionError:
    print(f"{PURPLE}The computer could not connect to the camera. Make sure the computer has a camera and permission is given by system to use the camera.{RESET}")