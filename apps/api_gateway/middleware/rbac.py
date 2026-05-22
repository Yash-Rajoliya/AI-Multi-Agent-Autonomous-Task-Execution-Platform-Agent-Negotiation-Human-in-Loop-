from fastapi import Request, HTTPException


class RBAC:

    @staticmethod
    def enforce(request: Request, required_role: str):
        user = getattr(request.state, "user", None)

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        roles = user.get("roles", [])

        if required_role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")