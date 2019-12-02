def get_graph_data_point_from_classifications(classifications):
    data_points = []
    for classification in classifications:
        # greatest_confidence_index = classification.output.index(max(classification.output))
        data_points.append(
            TableDataPoint(timestamp=classification.timestamp,
                           user=classification.user_id,
                           confidence=classification.confidence,
                           firstname=classification.first_name,
                           lastname=classification.last_name))
    return data_points


class TableData:
    def __init__(self, classifications, time_frame):
        self.classifications = classifications
        self.data_points = get_graph_data_point_from_classifications(classifications)
        self.time_frame = time_frame


class TableDataPoint:
    def __init__(self, timestamp, user, confidence, firstname, lastname):
        self.timestamp = timestamp
        self.user = user
        self.confidence = confidence
        self.firstname = firstname,
        self.lastname = lastname
