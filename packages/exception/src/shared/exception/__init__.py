import enum
from http import HTTPStatus


class ServiceErrorCode(enum.Enum):
    REQUEST_INVALID = (HTTPStatus.BAD_REQUEST, "RQ-1001", "REQUEST_INVALID")
    REQUEST_UNPROCESSABLE = (HTTPStatus.UNPROCESSABLE_ENTITY, "RQ-1002", "REQUEST_UNPROCESSABLE")
    REQUEST_TOO_MANY = (HTTPStatus.TOO_MANY_REQUESTS, "RQ-1003", "REQUEST_TOO_MANY")
    REQUEST_FORBIDDEN = (HTTPStatus.FORBIDDEN, "RQ-1004", "REQUEST_FORBIDDEN")

    ENTITY_NOT_FOUND = (HTTPStatus.NOT_FOUND, "RQ-2001", "ENTITY_NOT_FOUND")
    ENTITY_ALREADY_EXISTS = (HTTPStatus.CONFLICT, "RQ-2002", "ENTITY_ALREADY_EXISTS")
    ENTITY_DELETED = (HTTPStatus.GONE, "RQ-2003", "ENTITY_DELETED")
    ENTITY_NOT_DELETABLE = (HTTPStatus.CONFLICT, "RQ-2004", "ENTITY_NOT_DELETABLE")

    TOKEN_INVALID = (HTTPStatus.UNAUTHORIZED, "AC-1001", "TOKEN_INVALID")
    TOKEN_NOT_FOUND = (HTTPStatus.UNAUTHORIZED, "AC-1002", "TOKEN_NOT_FOUND")
    TOKEN_EXPIRED = (HTTPStatus.UNAUTHORIZED, "AC-1003", "TOKEN_EXPIRED")

    def __init__(self, http_status: HTTPStatus, code: str, detail: str):
        self.http_status = http_status
        self.code = code
        self.detail = detail

class ServiceException(Exception):
    def __init__(self, error_code: ServiceErrorCode, detail: str = None):
        self.error_code = error_code
        self.detail = detail

    def __str__(self):
        return f"{self.error_code.code} - {self.error_code.detail}"