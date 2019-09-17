from sql import SQL
from time_frame_enum import TimeFrameEnum

class Classification:
    def __init__(self, friends, output):
        self.friends = friends
        self.output = output

    def get_classification(self):
        return tuple(zip(self.friends, self.output))

    def load_classifications(self, time_frame):
        return SQL.fetch_classifications_by_time_frame(time_frame)