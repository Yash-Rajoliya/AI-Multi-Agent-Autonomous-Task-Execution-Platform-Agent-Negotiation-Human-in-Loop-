class ComplianceChecker:
    def check_data_privacy(self, data: dict):
        if "ssn" in data:
            raise ValueError("Sensitive data detected")

    def check_policy(self, action: str):
        allowed = ["read", "write", "execute"]
        if action not in allowed:
            raise ValueError("Policy violation")