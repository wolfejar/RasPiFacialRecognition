class OwnerUser:
    def __init__(self, user_id, first_name, last_name):
        self.user_id = user_id
        self.role = 'owner'
        self.first_name = first_name
        self.last_name = last_name


class GuestUser:
    def __init__(self, user_id, first_name, last_name):
        self.user_id = user_id
        self.role = 'guest'
        self.first_name = first_name
        self.last_name = last_name
