RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = "\033[95m"
RESET = '\033[0m'

class Camera:
    def __init__(self, model, padding=0.15, far=0.40, close=0.70, show=True, save=True, verbose=False):
        self.window_padding = padding
        self.human_far = far
        self.human_close = close
        self.model = model
        self.window_show = show
        self.window_save = save
        self.verbose = verbose

    def predict(self,src:str,confidence_threshold:float=0.35):
        self.results = self.model.predict(
            source = src,
            show = self.window_show,
            save = self.window_save,
            verbose = self.verbose,
            stream = True
        )

        for result in self.results:
            frame_height, frame_width = result.orig_shape

            self.window_left_border = int(frame_width * self.window_padding)
            self.window_right_border = int(frame_width * (1.0 - self.window_padding))

            names = []

            for box in result.boxes:
                xmin, ymin, xmax, ymax = map(int,box.xyxy[0])

                person_height = ymax-ymin

                confidence = box.conf.item()
                class_id = int(box.cls.item())
                class_name = result.names[class_id]

                names.append(class_name)

                center_x = int((xmin + xmax) / 2)
                center_y = int((ymin + ymax) / 2)

                if "person" in names:
                    if class_name == "person" and confidence > confidence_threshold:
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