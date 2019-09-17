from classification import Classification

class GraphData:
    def __init__(self, classifications):
        self.classifications = classifications

    def set_classifications(self, classifications):
        self.classifications = classifications

    def load_classifications_by_time_frame(self, time_frame):
        return Classification.load_classifications(time_frame)