from .base import TykAPIError

class TykAPIWrapperError(TykAPIError):
    """Base class for all Tyk API Wrapper errors."""
    pass

class TykNameConflictError(TykAPIWrapperError):
    """Raised when there is a name conflict for an API."""
    
    def __init__(self, object: str, name: str):
        self.object = object
        self.name = name
        super().__init__(f"{object} with name '{name}' already exists.", status_code=409)