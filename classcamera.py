# Color Values

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = "\033[95m"
RESET = '\033[0m'

class Camera:
    def __init__(self, model, padding=0.15, far=0.40, close=0.70):
        # Defining starting variables
        self.window_padding = padding
        self.human_far = far
        self.human_close = close
        self.model = model

    def predict(self,src:str,confidence_threshold:float=0.35, show=True, save=True, verbose=False):
        """
        Function for identifying and following human
        src:str - the source for identification (0 for camera)
        confidence_threshold:float=0.35 - the defined confidence level to consider an object human
        show=True - define whether window should be shown
        save=True - define whether video should be saved
        verbose=False - define whether to print automatically lines (by YOLO)
        """

        #Setting Variables
        self.window_show = show
        self.window_save = save
        self.verbose = verbose

        #Prediction
        self.results = self.model.predict(
            source = src,
            show = self.window_show,
            save = self.window_save,
            verbose = self.verbose,
            stream = True
        )

        #Parsing through results
        for result in self.results:
            frame_height, frame_width = result.orig_shape #Define frame border,width

            #Define window borders to print actions
            self.window_left_border = int(frame_width * self.window_padding)
            self.window_right_border = int(frame_width * (1.0 - self.window_padding))

            names = []

            for box in result.boxes:
                xmin, ymin, xmax, ymax = map(int,box.xyxy[0]) #map box coordinates

                person_height = ymax-ymin #calculate height of person

                confidence = box.conf.item()
                class_id = int(box.cls.item())
                class_name = result.names[class_id]

                names.append(class_name)

                #Find center point
                center_x = int((xmin + xmax) / 2)
                center_y = int((ymin + ymax) / 2)

                if "person" in names: # If human is detected
                    if class_name == "person" and confidence > confidence_threshold: #If YOLO is sure the object is human
                        self.action = f"{BLUE}Idle{RESET}" 

                        if person_height < (frame_height * self.human_far):
                            self.action = f"{GREEN}FORWARD{RESET}"
                        elif person_height > (frame_height * self.human_close):
                            self.action = f"{GREEN}BACKWARD{RESET}"

                        elif center_x < self.window_left_border:
                            self.action = f"{GREEN}TURN LEFT{RESET}"
                        elif center_x > self.window_right_border:
                            self.action = f"{GREEN}TURN RIGHT{RESET}"

                        if not self.verbose:
                            print(f"{RED}DETECTED {class_name} ({confidence:.2f}) CENTER:({center_x},{center_y}) {self.action}{RESET}")
                elif "person" not in names:
                    print(f"{BLUE}No people detected{RESET}")