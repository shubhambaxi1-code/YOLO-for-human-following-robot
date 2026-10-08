RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = "\033[95m"
RESET = '\033[0m'

class Image:
    def __init__(self, model):
        self.model = model
    def predict(self, src:str, show=True, save=True, verbose=True):
        self.show = show
        self.save = save
        self.verbose = verbose
        self.results = self.model.predict(
            source = src,
            show = self.show,
            save = self.save,
            verbose = self.verbose
        )