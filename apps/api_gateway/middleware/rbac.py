from fastapi import HTTPException, Request


class RBAC:
    """Role-based access control utility."""

    @staticmethod
    def enforce(
        request: Request,
        required_role: str,
    ) -> None:
        user = getattr(
            request.state,
            "user",
            None,
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
            )

        roles = user.get("roles", [])

        if not isinstance(roles, list):
            raise HTTPException(
                status_code=403,
                detail="Invalid roles format",
            )

        normalized_roles = {
            role.lower().strip()
            for role in roles
            if isinstance(role, str)
        }

        if (
            required_role.lower().strip()
            not in normalized_roles
        ):
            raise HTTPException(
                status_code=403,
                detail="Forbidden",
            )