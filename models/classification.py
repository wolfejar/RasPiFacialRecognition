from models.sql import SQL


class Classification:
    def __init__(self, user_id, first_name, last_name, confidence, timestamp, image_path):
        self.user_id = user_id
        self.confidence = confidence
        self.timestamp = timestamp
        self.image_path = image_path
        self.first_name = first_name
        self.last_name = last_name


# this is NOT for classifications created during training
def save_classification(model_id, classification, is_train=False):
    sql_instance = SQL()
    sql_instance.add_classification(model_id, int(is_train), classification)
