import typing as t
from datetime import datetime
import sys


class CustomException(Exception):
    default_user_message: t.ClassVar[str]
    default_status_code: t.ClassVar[int]
    default_description: t.ClassVar[t.Optional[str]]
    default_error_code: t.ClassVar[t.Optional[str]]

    def __init__(
        self,
        cause: t.Any = "",
        user_message: t.Optional[str] = None,
        status_code: t.Optional[int] = None,
        description: t.Optional[str] = None,
        error_code: t.Optional[str] = None,
    ) -> None:
        if not isinstance(cause, Exception):
            super().__init__(cause)
            self.__traceback__ = sys.exc_info()[2]
        else:
            self.__traceback__ = cause.__traceback__

        self._cause = cause
        self._user_message = user_message or self.default_user_message
        self._status_code = status_code or self.default_status_code
        self._description = description or self.default_description
        self._error_code = error_code or self.default_error_code

    @property
    def status_code(self):
        return self._status_code

    @property
    def description(self):
        return self._description

    @property
    def error_code(self):
        return self._error_code

    @property
    def cause(self):
        return self._cause

    @property
    def user_message(self):
        return self._user_message

    @property
    def formatted_data(self):
        error_code = self._error_code
        cause = self._cause
        dict_ = {
            "statusCode": self.status_code,
            "description": self.description,
            "dateTime": datetime.now().isoformat(),
            "cause": cause if isinstance(cause, dict) else str(cause),
            "errorCode": f"{error_code}",
            "userMessage": self.user_message,
        }
        return dict_


class ForbiddenException(CustomException):
    default_user_message = "Not enough permissions"
    default_status_code = 403
    default_description = "Not enough permissions"
    default_error_code = "forbidden"


class InternalErrorException(CustomException):
    default_user_message = "Something went wrong"
    default_status_code = 500
    default_description = "Something went wrong"
    default_error_code = "internal"


class CustomValidationError(CustomException):
    default_user_message = "Validation error"
    default_status_code = 422
    default_description = "Validation error"
    default_error_code = "validation_error"


class AlreadyExistsException(CustomException):
    default_user_message = "Object already exists"
    default_status_code = 422
    default_description = "Object already exists"
    default_error_code = "already_exists"


class ObjectDoesNotExist(CustomException):
    default_user_message = "Object does not exist"
    default_status_code = 404
    default_description = "Object does not exist"
    default_error_code = "not_found"


class AlreadyInUseException(CustomException):
    default_user_message = "Object already in use"
    default_status_code = 422
    default_description = "Object already in use"
    default_error_code = "already_in_use"


class RateLimitException(CustomException):
    default_user_message = "Too many requests"
    default_status_code = 429
    default_description = "Rate limit exceeded"
    default_error_code = "rate_limit"
