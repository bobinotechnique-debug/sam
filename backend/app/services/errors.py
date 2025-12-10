class ServiceError(Exception):
    """Base class for service layer errors."""


class NotFoundError(ServiceError):
    """Raised when a requested entity is not found."""


class ConflictError(ServiceError):
    """Raised when an operation conflicts with existing data."""


class ValidationError(ServiceError):
    """Raised when validation fails at the service layer."""
