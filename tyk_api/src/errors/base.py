

class TykAPIError(Exception):
    """Base class for Tyk API errors."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code
    
class TykNotFoundError(TykAPIError):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with identifier '{identifier}' not found.", status_code=404)
        
class TykBadRequestError(TykAPIError):
    """Raised when a bad request is made to the Tyk API."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=400)

class TykMultiOperationError(TykAPIError):
    """Raised when multiple operations fail."""

    def __init__(self, message: str, errors: dict[str, str]):
        self.errors = errors
        super().__init__(f"{message}. Errors: {errors}", status_code=500)