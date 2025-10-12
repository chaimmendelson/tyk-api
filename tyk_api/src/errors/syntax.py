from .base import TykAPIError

class TykAPISyntaxError(TykAPIError):
    """Exception raised for syntax errors in Tyk API requests."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)

class TykAPIInvalidParameterError(TykAPIError):
    """Exception raised for invalid parameters in Tyk API requests."""

    def __init__(self, message: str, status_code: int = 422):
        super().__init__(message, status_code)