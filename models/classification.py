from .time_frame_enum import TimeFrameEnum


class Classification:
    def __init__(self, friends, output, timestamp):
        self.friends = friends
        self.output = output
        self.timestamp = timestamp

    def get_classification(self):
        return tuple(zip(self.friends, self.output))
