from .classification import Classification
from .sql import SQL


class GraphData:
    def __init__(self, classifications):
        self.classifications = classifications

    def set_classifications(self, classifications):
        self.classifications = classifications

    def load_classifications_by_time_frame(self, time_frame):
        sql_instance = SQL()
        self.classifications = sql_instance.load_classifications_by_time_frame(time_frame=time_frame)
