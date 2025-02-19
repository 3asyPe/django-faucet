import logging
from app.exceptions import (
    CustomException,
    CustomValidationError,
    InternalErrorException,
)
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

logger = logging.getLogger("CustomExceptionHandler")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    exception = handle_exception(exc)
    logger.error(f'Failed to process request: {exception.user_message}')
    if response is None:
        response = Response({}, status=exception.status_code)
    response.data = exception.formatted_data
    response.status_code = exception.status_code
    return response

def handle_exception(exception):
    if isinstance(exception, ValidationError):
        return CustomValidationError(cause=exception)
    if not isinstance(exception, CustomException):
        return InternalErrorException(cause=exception)

    return exception
