"""Standard validation helpers template for Python projects."""
import re
from typing import Any, Callable, Optional, TypeVar
from dataclasses import dataclass


T = TypeVar("T")


@dataclass
class ValidationResult:
    """Result of a validation check."""
    
    is_valid: bool
    message: str = ""
    field: str = ""
    
    def __bool__(self) -> bool:
        """Allow use in boolean context."""
        return self.is_valid


def validate_email(email: str) -> ValidationResult:
    """Validate email address format.
    
    Args:
        email: Email address to validate.
        
    Returns:
        ValidationResult indicating success or failure.
        
    Example:
        >>> result = validate_email("user@example.com")
        >>> result.is_valid
        True
    """
    if not email:
        return ValidationResult(False, "Email is required", "email")
    
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return ValidationResult(False, "Invalid email format", "email")
    
    return ValidationResult(True)


def validate_required(value: Any, field_name: str) -> ValidationResult:
    """Validate that a value is not None or empty.
    
    Args:
        value: Value to validate.
        field_name: Name of the field for error messages.
        
    Returns:
        ValidationResult indicating success or failure.
    """
    if value is None:
        return ValidationResult(False, f"{field_name} is required", field_name)
    
    if isinstance(value, str) and not value.strip():
        return ValidationResult(False, f"{field_name} cannot be empty", field_name)
    
    return ValidationResult(True)


def validate_length(
    value: str,
    field_name: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> ValidationResult:
    """Validate string length is within bounds.
    
    Args:
        value: String to validate.
        field_name: Name of the field for error messages.
        min_length: Minimum allowed length.
        max_length: Maximum allowed length.
        
    Returns:
        ValidationResult indicating success or failure.
    """
    if min_length is not None and len(value) < min_length:
        return ValidationResult(
            False,
            f"{field_name} must be at least {min_length} characters",
            field_name
        )
    
    if max_length is not None and len(value) > max_length:
        return ValidationResult(
            False,
            f"{field_name} must be at most {max_length} characters",
            field_name
        )
    
    return ValidationResult(True)


def validate_range(
    value: int | float,
    field_name: str,
    min_value: Optional[int | float] = None,
    max_value: Optional[int | float] = None
) -> ValidationResult:
    """Validate number is within range.
    
    Args:
        value: Number to validate.
        field_name: Name of the field for error messages.
        min_value: Minimum allowed value.
        max_value: Maximum allowed value.
        
    Returns:
        ValidationResult indicating success or failure.
    """
    if min_value is not None and value < min_value:
        return ValidationResult(
            False,
            f"{field_name} must be at least {min_value}",
            field_name
        )
    
    if max_value is not None and value > max_value:
        return ValidationResult(
            False,
            f"{field_name} must be at most {max_value}",
            field_name
        )
    
    return ValidationResult(True)


def validate_password(
    password: str,
    min_length: int = 8,
    require_uppercase: bool = True,
    require_lowercase: bool = True,
    require_digit: bool = True,
    require_special: bool = False
) -> ValidationResult:
    """Validate password strength.
    
    Args:
        password: Password to validate.
        min_length: Minimum password length.
        require_uppercase: Require at least one uppercase letter.
        require_lowercase: Require at least one lowercase letter.
        require_digit: Require at least one digit.
        require_special: Require at least one special character.
        
    Returns:
        ValidationResult indicating success or failure.
    """
    if len(password) < min_length:
        return ValidationResult(
            False,
            f"Password must be at least {min_length} characters",
            "password"
        )
    
    if require_uppercase and not re.search(r"[A-Z]", password):
        return ValidationResult(
            False,
            "Password must contain at least one uppercase letter",
            "password"
        )
    
    if require_lowercase and not re.search(r"[a-z]", password):
        return ValidationResult(
            False,
            "Password must contain at least one lowercase letter",
            "password"
        )
    
    if require_digit and not re.search(r"\d", password):
        return ValidationResult(
            False,
            "Password must contain at least one digit",
            "password"
        )
    
    if require_special and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return ValidationResult(
            False,
            "Password must contain at least one special character",
            "password"
        )
    
    return ValidationResult(True)


class Validator:
    """Chainable validator for multiple validations.
    
    Example:
        >>> validator = Validator()
        >>> validator.add(validate_required, email, "email")
        >>> validator.add(validate_email, email)
        >>> if not validator.is_valid:
        ...     print(validator.errors)
    """
    
    def __init__(self) -> None:
        """Initialize validator."""
        self.errors: list[ValidationResult] = []
    
    def add(
        self,
        validation_func: Callable[..., ValidationResult],
        *args: Any,
        **kwargs: Any
    ) -> "Validator":
        """Add a validation check.
        
        Args:
            validation_func: Validation function to run.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
            
        Returns:
            Self for chaining.
        """
        result = validation_func(*args, **kwargs)
        if not result.is_valid:
            self.errors.append(result)
        return self
    
    @property
    def is_valid(self) -> bool:
        """Check if all validations passed."""
        return len(self.errors) == 0
    
    def get_error_messages(self) -> list[str]:
        """Get all error messages."""
        return [e.message for e in self.errors]
