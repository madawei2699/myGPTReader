import time

class RateLimiter:
    def __init__(self, limit=10, period=3600):
        self.limit = limit
        self.period = period
        self.users = {}

    def allow_request(self, user_id):
        now = time.time()
        user_requests = self.users.get(user_id, [])
        user_requests = [req for req in user_requests if req > now - self.period]
        if len(user_requests) < self.limit:
            user_requests.append(now)
            self.users[user_id] = user_requests
            return True
        return False
