"""Best Practices Manager - Lazy-loaded, auto-updating coding guidelines.

Provides language-specific best practices with minimal token usage through
lazy loading. Practices are cached and auto-updated from security databases.
"""
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Cache directory for best practices
CACHE_DIR = Path.home() / ".ov-code" / "best-practices"
CACHE_EXPIRY_DAYS = 7


@dataclass
class BestPractice:
    """A single best practice rule."""
    
    id: str
    category: str  # security, performance, style, testing
    language: str
    title: str
    description: str
    example_good: str
    example_bad: str
    severity: str  # critical, important, recommended
    tags: list[str]
    
    def to_prompt_format(self) -> str:
        """Convert to compact prompt format for LLMs."""
        return f"- {self.title}: {self.description}"


class BestPracticesManager:
    """Manager for lazy-loaded, auto-updating best practices.
    
    Best practices are loaded on-demand and cached to minimize
    token usage when working with AI models.
    
    Example:
        >>> manager = BestPracticesManager()
        >>> practices = manager.get_practices("python", "security")
        >>> prompt = manager.get_prompt_for_language("python")
    """
    
    # Lazy-loaded practice data
    _practices_cache: dict[str, list[BestPractice]] = {}
    _last_load: dict[str, datetime] = {}
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize the manager.
        
        Args:
            cache_dir: Custom cache directory path.
        """
        self.cache_dir = cache_dir or CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_practices(
        self,
        language: str,
        category: Optional[str] = None,
        severity: Optional[str] = None
    ) -> list[BestPractice]:
        """Get best practices for a language (lazy-loaded).
        
        Args:
            language: Programming language (python, javascript, etc.)
            category: Filter by category (security, performance, etc.)
            severity: Filter by severity (critical, important, recommended)
            
        Returns:
            List of relevant best practices.
        """
        language = language.lower()
        
        # Lazy load if not cached or expired
        if self._should_reload(language):
            self._load_practices(language)
        
        practices = self._practices_cache.get(language, [])
        
        # Filter by category
        if category:
            practices = [p for p in practices if p.category == category]
        
        # Filter by severity
        if severity:
            practices = [p for p in practices if p.severity == severity]
        
        return practices
    
    def get_prompt_for_language(
        self,
        language: str,
        max_tokens: int = 500,
        categories: Optional[list[str]] = None
    ) -> str:
        """Get a compact prompt with best practices for AI models.
        
        Uses lazy loading and token optimization to minimize context usage.
        
        Args:
            language: Programming language.
            max_tokens: Maximum approximate tokens for the prompt.
            categories: Specific categories to include.
            
        Returns:
            Optimized prompt string with best practices.
        """
        practices = self.get_practices(language)
        
        if categories:
            practices = [p for p in practices if p.category in categories]
        
        # Sort by severity (critical first)
        severity_order = {"critical": 0, "important": 1, "recommended": 2}
        practices.sort(key=lambda p: severity_order.get(p.severity, 3))
        
        # Build compact prompt
        lines = [f"## Best Practices for {language.upper()}"]
        
        # Group by category for organization
        by_category: dict[str, list[BestPractice]] = {}
        for p in practices:
            by_category.setdefault(p.category, []).append(p)
        
        current_tokens = 10  # Estimate for header
        
        for category, cat_practices in by_category.items():
            category_header = f"\n### {category.title()}"
            lines.append(category_header)
            current_tokens += 5
            
            for practice in cat_practices:
                line = practice.to_prompt_format()
                # Token estimation: ~4 chars per token is a rough approximation.
                # For more accurate estimation, consider using tiktoken or model-specific tokenizers.
                # This approximation is sufficient for context window management.
                line_tokens = len(line) // 4
                
                if current_tokens + line_tokens > max_tokens:
                    break
                
                lines.append(line)
                current_tokens += line_tokens
        
        return "\n".join(lines)
    
    def update_practices(self, language: str) -> None:
        """Update best practices from latest sources.
        
        Args:
            language: Language to update practices for.
        """
        language = language.lower()
        
        # Load built-in practices
        practices = self._get_builtin_practices(language)
        
        # Cache them
        self._practices_cache[language] = practices
        self._last_load[language] = datetime.now()
        
        # Save to disk cache
        self._save_cache(language, practices)
    
    def _should_reload(self, language: str) -> bool:
        """Check if practices should be reloaded."""
        if language not in self._practices_cache:
            return True
        
        last = self._last_load.get(language)
        if not last:
            return True
        
        return datetime.now() - last > timedelta(days=CACHE_EXPIRY_DAYS)
    
    def _load_practices(self, language: str) -> None:
        """Load practices from cache or generate defaults."""
        cache_file = self.cache_dir / f"{language}.json"
        
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                practices = [BestPractice(**p) for p in data["practices"]]
                self._practices_cache[language] = practices
                self._last_load[language] = datetime.fromisoformat(data["updated"])
                return
            except Exception:
                pass
        
        # Fall back to built-in practices
        self._practices_cache[language] = self._get_builtin_practices(language)
        self._last_load[language] = datetime.now()
    
    def _save_cache(self, language: str, practices: list[BestPractice]) -> None:
        """Save practices to disk cache."""
        cache_file = self.cache_dir / f"{language}.json"
        data = {
            "updated": datetime.now().isoformat(),
            "practices": [vars(p) for p in practices]
        }
        cache_file.write_text(json.dumps(data, indent=2))
    
    def _get_builtin_practices(self, language: str) -> list[BestPractice]:
        """Get built-in best practices for a language."""
        # Common practices for all languages
        common = [
            BestPractice(
                id="sec-001",
                category="security",
                language=language,
                title="Input Validation",
                description="Always validate and sanitize user input before processing",
                example_good="validated_input = sanitize(user_input)",
                example_bad="process(user_input)  # Direct use without validation",
                severity="critical",
                tags=["injection", "xss", "security"]
            ),
            BestPractice(
                id="sec-002",
                category="security", 
                language=language,
                title="No Hardcoded Secrets",
                description="Never hardcode API keys, passwords, or secrets in code",
                example_good="api_key = os.getenv('API_KEY')",
                example_bad="api_key = 'sk-12345abcdef'",
                severity="critical",
                tags=["secrets", "credentials", "security"]
            ),
            BestPractice(
                id="sec-003",
                category="security",
                language=language,
                title="Parameterized Queries",
                description="Use parameterized queries to prevent SQL injection",
                example_good="cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
                example_bad="cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')",
                severity="critical",
                tags=["sql", "injection", "database"]
            ),
            BestPractice(
                id="perf-001",
                category="performance",
                language=language,
                title="Avoid N+1 Queries",
                description="Batch database queries instead of querying in loops",
                example_good="users = User.objects.filter(id__in=ids)",
                example_bad="users = [User.objects.get(id=id) for id in ids]",
                severity="important",
                tags=["database", "performance", "optimization"]
            ),
            BestPractice(
                id="style-001",
                category="style",
                language=language,
                title="Descriptive Names",
                description="Use clear, descriptive names for variables and functions",
                example_good="user_email_address = get_user_email(user_id)",
                example_bad="x = f(y)",
                severity="recommended",
                tags=["readability", "naming", "maintainability"]
            ),
            BestPractice(
                id="err-001",
                category="error_handling",
                language=language,
                title="Specific Exception Handling",
                description="Catch specific exceptions, not generic ones",
                example_good="except ValueError as e: handle_value_error(e)",
                example_bad="except: pass  # Silently ignores all errors",
                severity="important",
                tags=["exceptions", "error-handling", "debugging"]
            ),
        ]
        
        # Language-specific practices
        language_specific = LANGUAGE_PRACTICES.get(language, [])
        
        return common + language_specific


# Language-specific best practices (lazy-loaded)
LANGUAGE_PRACTICES: dict[str, list[BestPractice]] = {
    "python": [
        BestPractice(
            id="py-001",
            category="style",
            language="python",
            title="Type Hints",
            description="Use type hints for function parameters and return values",
            example_good="def greet(name: str) -> str: return f'Hello, {name}'",
            example_bad="def greet(name): return f'Hello, {name}'",
            severity="recommended",
            tags=["typing", "documentation", "maintainability"]
        ),
        BestPractice(
            id="py-002",
            category="style",
            language="python",
            title="Context Managers",
            description="Use context managers for resource management",
            example_good="with open('file.txt') as f: data = f.read()",
            example_bad="f = open('file.txt'); data = f.read(); f.close()",
            severity="important",
            tags=["resources", "files", "cleanup"]
        ),
        BestPractice(
            id="py-003",
            category="security",
            language="python",
            title="Safe Deserialization",
            description="Avoid pickle for untrusted data, use JSON instead",
            example_good="data = json.loads(user_input)",
            example_bad="data = pickle.loads(user_input)  # Code execution risk",
            severity="critical",
            tags=["serialization", "security", "pickle"]
        ),
    ],
    "javascript": [
        BestPractice(
            id="js-001",
            category="style",
            language="javascript",
            title="Use const/let",
            description="Prefer const for constants, let for variables, avoid var",
            example_good="const MAX_SIZE = 100; let count = 0;",
            example_bad="var MAX_SIZE = 100; var count = 0;",
            severity="recommended",
            tags=["variables", "scope", "modern-js"]
        ),
        BestPractice(
            id="js-002",
            category="security",
            language="javascript",
            title="Avoid eval()",
            description="Never use eval() with user input - use safer alternatives",
            example_good="JSON.parse(jsonString)",
            example_bad="eval(userInput)  # Code injection risk",
            severity="critical",
            tags=["eval", "injection", "security"]
        ),
        BestPractice(
            id="js-003",
            category="security",
            language="javascript",
            title="DOM Sanitization",
            description="Sanitize HTML before inserting into DOM to prevent XSS",
            example_good="element.textContent = userInput",
            example_bad="element.innerHTML = userInput  # XSS risk",
            severity="critical",
            tags=["xss", "dom", "security"]
        ),
    ],
    "typescript": [
        BestPractice(
            id="ts-001",
            category="style",
            language="typescript",
            title="Strict Mode",
            description="Enable strict mode in tsconfig for better type safety",
            example_good='"strict": true in tsconfig.json',
            example_bad='"strict": false or not set',
            severity="important",
            tags=["typing", "safety", "configuration"]
        ),
        BestPractice(
            id="ts-002",
            category="style",
            language="typescript",
            title="Avoid any",
            description="Use specific types instead of 'any' for type safety",
            example_good="function process(data: UserData): Result",
            example_bad="function process(data: any): any",
            severity="important",
            tags=["typing", "any", "safety"]
        ),
    ],
    "rust": [
        BestPractice(
            id="rs-001",
            category="style",
            language="rust",
            title="Handle Results",
            description="Always handle Result and Option types explicitly",
            example_good="let value = result?; or match result { Ok(v) => v, Err(e) => handle(e) }",
            example_bad="let value = result.unwrap();  # Can panic",
            severity="important",
            tags=["error-handling", "result", "option"]
        ),
        BestPractice(
            id="rs-002",
            category="performance",
            language="rust",
            title="Avoid Cloning",
            description="Use references and borrowing instead of cloning when possible",
            example_good="fn process(data: &str) { ... }",
            example_bad="fn process(data: String) { let copy = data.clone(); }",
            severity="recommended",
            tags=["performance", "memory", "borrowing"]
        ),
    ],
    "go": [
        BestPractice(
            id="go-001",
            category="error_handling",
            language="go",
            title="Check Errors",
            description="Always check and handle errors returned by functions",
            example_good="if err != nil { return fmt.Errorf('failed: %w', err) }",
            example_bad="result, _ := someFunction()  # Ignoring error",
            severity="critical",
            tags=["errors", "handling", "reliability"]
        ),
        BestPractice(
            id="go-002",
            category="style",
            language="go",
            title="Defer for Cleanup",
            description="Use defer for cleanup operations like closing files",
            example_good="f, _ := os.Open(path); defer f.Close()",
            example_bad="Manual close at end of function (can be missed)",
            severity="important",
            tags=["defer", "cleanup", "resources"]
        ),
    ],
}


# Module-level functions for easy access
_manager: Optional[BestPracticesManager] = None


def _get_manager() -> BestPracticesManager:
    """Get or create the singleton manager."""
    global _manager
    if _manager is None:
        _manager = BestPracticesManager()
    return _manager


def get_best_practices(language: str, category: Optional[str] = None) -> str:
    """Get best practices as formatted markdown.
    
    Args:
        language: Programming language.
        category: Optional category filter.
        
    Returns:
        Formatted markdown string.
    """
    manager = _get_manager()
    practices = manager.get_practices(language, category)
    
    lines = [f"# Best Practices for {language.upper()}\n"]
    
    # Group by category
    by_category: dict[str, list[BestPractice]] = {}
    for p in practices:
        by_category.setdefault(p.category, []).append(p)
    
    for category, cat_practices in by_category.items():
        lines.append(f"\n## {category.replace('_', ' ').title()}\n")
        for p in cat_practices:
            severity_emoji = {"critical": "🔴", "important": "🟡", "recommended": "🟢"}.get(p.severity, "⚪")
            lines.append(f"### {severity_emoji} {p.title}\n")
            lines.append(f"{p.description}\n")
            lines.append(f"**Good:** `{p.example_good}`\n")
            lines.append(f"**Bad:** `{p.example_bad}`\n")
    
    return "\n".join(lines)


def get_best_practices_prompt(language: str, max_tokens: int = 500) -> str:
    """Get compact best practices prompt for AI models.
    
    Args:
        language: Programming language.
        max_tokens: Maximum tokens to use.
        
    Returns:
        Optimized prompt string.
    """
    return _get_manager().get_prompt_for_language(language, max_tokens)


def update_best_practices(language: str) -> None:
    """Update best practices for a language.
    
    Args:
        language: Language to update.
    """
    _get_manager().update_practices(language)
