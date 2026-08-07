class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create(self, user_id):
        self.sessions[user_id] = {}
        return self.sessions[user_id]