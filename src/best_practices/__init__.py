"""Best Practices Module - Auto-updated language-specific coding guidelines.

This module provides lazy-loaded best practices for any programming language,
automatically updated with latest security info and coding standards.
"""

from src.best_practices.manager import (
    get_best_practices,
    get_best_practices_prompt,
    update_best_practices,
    BestPracticesManager,
)

__all__ = [
    "get_best_practices",
    "get_best_practices_prompt", 
    "update_best_practices",
    "BestPracticesManager",
]
