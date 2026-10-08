class Image:
    def __init__(self, model):
        self.model = model
    def predict(self, src:str, show=True, save=True, verbose=True):
        """
        Function to determine objects in a picture
        src:str - path of image
        show=True - determines whether to show preview of image
        save=True
        """
        #Set variables
        self.show = show
        self.save = save
        self.verbose = verbose
        #Start prediction
        self.results = self.model.predict(
            source = src,
            show = self.show,
            save = self.save,
            verbose = self.verbose
        )