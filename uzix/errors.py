class UzixError(Exception):
    """Base error for the Uzix public API."""


class ValidationError(UzixError):
    def __init__(self, message: str, *, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


class ConfigurationError(UzixError):
    """Raised when Uzix settings are invalid."""


class ModelUnavailableError(UzixError):
    """Raised when the ML layer cannot be initialized or loaded."""


class UnauthorizedError(UzixError):
    def __init__(self, message: str = "Unauthorized", *, status_code: int = 401):
        super().__init__(message)
        self.status_code = status_code


class RateLimitError(UzixError):
    def __init__(self, message: str = "Rate limit exceeded", *, retry_after: int = 0, status_code: int = 429):
        super().__init__(message)
        self.retry_after = retry_after
        self.status_code = status_code