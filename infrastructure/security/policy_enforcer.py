class PolicyEnforcer:
    def check(self, user_role: str, action: str):
        if user_role != "admin":
            raise PermissionError("Access denied")