class HackerAbuseException(Exception):
    def __init__(self, user, model):
        self.user = user
        self.model = model
        super().__init__()
