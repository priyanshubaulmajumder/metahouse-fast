'''
from wealthy_commons.exceptions import AppException

class WealthyValidationError(AppException):
    def __init__(self, message='Something went wrong', params=None):
        super(WealthyValidationError, self).__init__(message, ExceptionCodes.VALIDATION_ERROR_CODE, params=params)
'''
from fastapi import HTTPException

class Http400(HTTPException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=400, detail=detail)

class Http401(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)

class Http403(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail)

class Http404(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=404, detail=detail)

class ExceptionCodes:
    VALIDATION_ERROR_CODE = 'VAL001'

class WealthyValidationError(HTTPException):
    def __init__(self, detail: str = "Something went wrong", params: dict = None):
        super().__init__(status_code=400, detail={"message": detail, "code": ExceptionCodes.VALIDATION_ERROR_CODE, "params": params})