import datetime


class AuditLogger:
    def log(self, user_id: str, action: str, resource: str):
        print({
            "user": user_id,
            "action": action,
            "resource": resource,
            "timestamp": datetime.datetime.utcnow().isoformat()
        })