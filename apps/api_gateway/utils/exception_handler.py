from fastapi.responses import JSONResponse


def http_error(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": status_code,
                "message": message
            }
        }
    )