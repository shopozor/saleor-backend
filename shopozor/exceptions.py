class HackerAbuseException(Exception):
    def __init__(self, user, instance):
        self.user = user
        self.instance = instance
        super().__init__()
