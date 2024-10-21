# Status codes and messages
STATUS_CODES = {
    200: "Success",
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error"
}

def format_response(status_code: int, err_code: str = None, message: dict = {}):
    if err_code is None:
        err_code = STATUS_CODES.get(status_code, "Unknown status code")
    return {
        "status_code": status_code,
        "code": err_code,
        "message": message
    }