class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class TimeExpiredError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 422
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid credentials",
        "status": 401
    },
    "TimeExpiredError": {
        "message": "Time has expired",
        "status": 401
    },
}
