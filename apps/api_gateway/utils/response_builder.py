def success(data=None, meta=None):
    return {
        "status": "success",
        "data": data,
        "meta": meta or {}
    }


def failure(message: str, code: int = 400):
    return {
        "status": "error",
        "error": {
            "message": message,
            "code": code
        }
    }