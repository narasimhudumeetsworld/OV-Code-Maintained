"""Standard error handling template for Python projects."""
from typing import Any, Optional


class BaseError(Exception):
    """Base exception for all custom errors."""
    
    def __init__(
        self,
        message: str,
        code: str = "UNKNOWN_ERROR",
        details: Optional[dict[str, Any]] = None
    ) -> None:
        """Initialize the error.
        
        Args:
            message: Human-readable error message.
            code: Machine-readable error code.
            details: Additional error context.
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
    
    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for API responses."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


class ValidationError(BaseError):
    """Raised when input validation fails."""
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        details: Optional[dict[str, Any]] = None
    ) -> None:
        """Initialize validation error.
        
        Args:
            message: Description of the validation failure.
            field: The field that failed validation.
            details: Additional context.
        """
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"field": field, **(details or {})}
        )


class NotFoundError(BaseError):
    """Raised when a requested resource is not found."""
    
    def __init__(
        self,
        resource_type: str,
        resource_id: Any,
        message: Optional[str] = None
    ) -> None:
        """Initialize not found error.
        
        Args:
            resource_type: Type of resource (e.g., "User", "Task").
            resource_id: Identifier of the missing resource.
            message: Optional custom message.
        """
        default_message = f"{resource_type} with id '{resource_id}' not found"
        super().__init__(
            message=message or default_message,
            code="NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": str(resource_id)}
        )


class AuthenticationError(BaseError):
    """Raised when authentication fails."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[dict[str, Any]] = None
    ) -> None:
        """Initialize authentication error."""
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            details=details
        )


class AuthorizationError(BaseError):
    """Raised when user lacks permission for an action."""
    
    def __init__(
        self,
        action: str,
        resource: Optional[str] = None,
        message: Optional[str] = None
    ) -> None:
        """Initialize authorization error.
        
        Args:
            action: The action that was denied.
            resource: The resource being accessed.
            message: Optional custom message.
        """
        default_message = f"Permission denied for action: {action}"
        if resource:
            default_message += f" on {resource}"
        
        super().__init__(
            message=message or default_message,
            code="AUTHORIZATION_ERROR",
            details={"action": action, "resource": resource}
        )
