"""Standard logging setup template for Python projects."""
import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    name: str = "app",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    max_bytes: int = 10_485_760,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        name: Logger name.
        level: Logging level (default: INFO).
        log_file: Optional path to log file.
        log_format: Custom log format string.
        max_bytes: Maximum log file size before rotation.
        backup_count: Number of backup files to keep.
        
    Returns:
        Configured logger instance.
        
    Example:
        >>> logger = setup_logging("myapp", level=logging.DEBUG)
        >>> logger.info("Application started")
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Default format
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )
    
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name, typically __name__.
        
    Returns:
        Logger instance.
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    return logging.getLogger(name)


# Context manager for logging operation timing
class LogTimer:
    """Context manager to log operation timing.
    
    Example:
        >>> with LogTimer(logger, "database query"):
        ...     result = db.query()
        # Logs: "database query completed in 0.123s"
    """
    
    def __init__(
        self,
        logger: logging.Logger,
        operation: str,
        level: int = logging.INFO
    ) -> None:
        """Initialize log timer.
        
        Args:
            logger: Logger instance to use.
            operation: Description of the operation.
            level: Log level for the message.
        """
        self.logger = logger
        self.operation = operation
        self.level = level
        self.start_time: float = 0
    
    def __enter__(self) -> "LogTimer":
        """Start timing."""
        import time
        self.start_time = time.perf_counter()
        self.logger.log(self.level, f"Starting: {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Log completion time."""
        import time
        elapsed = time.perf_counter() - self.start_time
        
        if exc_type is not None:
            self.logger.error(
                f"{self.operation} failed after {elapsed:.3f}s: {exc_val}"
            )
        else:
            self.logger.log(
                self.level,
                f"{self.operation} completed in {elapsed:.3f}s"
            )
