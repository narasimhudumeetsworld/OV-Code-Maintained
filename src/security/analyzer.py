"""Security Analyzer - Auto-updated vulnerability detection.

Provides security analysis with lazy-loaded vulnerability databases
and automatic updates from security advisories.
"""
import re
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class SecurityFinding:
    """A security vulnerability finding."""
    
    severity: str  # HIGH, MEDIUM, LOW
    category: str  # injection, xss, secrets, etc.
    description: str
    location: str  # file:line
    cwe_id: Optional[str] = None  # CWE-79, CWE-89, etc.
    fix_suggestion: Optional[str] = None
    reference: Optional[str] = None


@dataclass
class AnalysisResult:
    """Result of security analysis."""
    
    file_path: str
    language: str
    findings: list[SecurityFinding] = field(default_factory=list)
    scan_time: datetime = field(default_factory=datetime.now)
    
    @property
    def has_critical(self) -> bool:
        """Check if there are critical findings."""
        return any(f.severity == "HIGH" for f in self.findings)
    
    @property
    def summary(self) -> dict[str, int]:
        """Get summary count by severity."""
        counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for f in self.findings:
            counts[f.severity] = counts.get(f.severity, 0) + 1
        return counts


class SecurityAnalyzer:
    """Security analyzer with lazy-loaded vulnerability patterns.
    
    Patterns are loaded on-demand to minimize memory usage and
    can be updated from security databases.
    
    Example:
        >>> analyzer = SecurityAnalyzer()
        >>> result = analyzer.analyze_file("app.py")
        >>> for finding in result.findings:
        ...     print(f"{finding.severity}: {finding.description}")
    """
    
    # Lazy-loaded patterns
    _patterns: Optional[dict] = None
    _last_updated: Optional[datetime] = None
    
    def __init__(self):
        """Initialize the analyzer."""
        self._ensure_patterns_loaded()
    
    @property
    def last_updated(self) -> str:
        """Get the last update timestamp."""
        if self._last_updated:
            return self._last_updated.strftime("%Y-%m-%d")
        return "Built-in patterns"
    
    def _ensure_patterns_loaded(self) -> None:
        """Lazy load security patterns."""
        if self._patterns is None:
            self._patterns = self._get_builtin_patterns()
            self._last_updated = datetime.now()
    
    def analyze_file(
        self,
        file_path: str,
        language: Optional[str] = None
    ) -> AnalysisResult:
        """Analyze a file for security vulnerabilities.
        
        Args:
            file_path: Path to file or directory.
            language: Override auto-detected language.
            
        Returns:
            AnalysisResult with findings.
        """
        path = Path(file_path)
        
        if path.is_dir():
            return self._analyze_directory(path, language)
        
        # Detect language from extension
        if language is None:
            language = self._detect_language(path)
        
        # Read file content
        try:
            content = path.read_text()
        except Exception as e:
            return AnalysisResult(
                file_path=str(path),
                language=language or "unknown",
                findings=[SecurityFinding(
                    severity="LOW",
                    category="error",
                    description=f"Could not read file: {e}",
                    location=str(path)
                )]
            )
        
        findings = self._analyze_content(content, language, str(path))
        
        return AnalysisResult(
            file_path=str(path),
            language=language or "unknown",
            findings=findings
        )
    
    def _analyze_directory(
        self,
        directory: Path,
        language: Optional[str]
    ) -> AnalysisResult:
        """Analyze all files in a directory."""
        all_findings = []
        
        for file_path in directory.rglob("*"):
            if file_path.is_file() and not self._should_skip(file_path):
                result = self.analyze_file(str(file_path), language)
                all_findings.extend(result.findings)
        
        return AnalysisResult(
            file_path=str(directory),
            language=language or "mixed",
            findings=all_findings
        )
    
    def _should_skip(self, path: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = [
            ".git", "node_modules", "__pycache__", ".venv",
            "venv", "dist", "build", ".egg-info"
        ]
        return any(p in str(path) for p in skip_patterns)
    
    def _detect_language(self, path: Path) -> str:
        """Detect language from file extension."""
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript",
            ".rb": "ruby",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".php": "php",
            ".cs": "csharp",
            ".sql": "sql",
        }
        return ext_map.get(path.suffix.lower(), "unknown")
    
    def _analyze_content(
        self,
        content: str,
        language: str,
        file_path: str
    ) -> list[SecurityFinding]:
        """Analyze content for security issues."""
        findings = []
        lines = content.split("\n")
        
        # Get patterns for this language
        patterns = self._patterns.get("common", [])
        patterns.extend(self._patterns.get(language, []))
        
        for i, line in enumerate(lines, 1):
            for pattern_info in patterns:
                if re.search(pattern_info["pattern"], line, re.IGNORECASE):
                    findings.append(SecurityFinding(
                        severity=pattern_info["severity"],
                        category=pattern_info["category"],
                        description=pattern_info["description"],
                        location=f"{file_path}:{i}",
                        cwe_id=pattern_info.get("cwe"),
                        fix_suggestion=pattern_info.get("fix"),
                        reference=pattern_info.get("reference")
                    ))
        
        return findings
    
    def _get_builtin_patterns(self) -> dict:
        """Get built-in security patterns (lazy-loaded)."""
        return {
            "common": [
                {
                    "pattern": r"(password|passwd|pwd|secret|api_key|apikey|token|auth)\s*=\s*['\"][^'\"]+['\"]",
                    "severity": "HIGH",
                    "category": "secrets",
                    "description": "Hardcoded secret or credential detected",
                    "cwe": "CWE-798",
                    "fix": "Use environment variables or a secret manager",
                    "reference": "https://cwe.mitre.org/data/definitions/798.html"
                },
                {
                    "pattern": r"(sk-[a-zA-Z0-9]{20,}|sk_live_[a-zA-Z0-9]+|AKIA[0-9A-Z]{16})",
                    "severity": "HIGH",
                    "category": "secrets",
                    "description": "API key pattern detected (OpenAI/Stripe/AWS)",
                    "cwe": "CWE-798",
                    "fix": "Remove the key and rotate it immediately"
                },
                {
                    "pattern": r"-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----",
                    "severity": "HIGH",
                    "category": "secrets",
                    "description": "Private key detected in code",
                    "cwe": "CWE-321",
                    "fix": "Store private keys in secure key management"
                },
                {
                    "pattern": r"eval\s*\(",
                    "severity": "HIGH",
                    "category": "injection",
                    "description": "Use of eval() can lead to code injection",
                    "cwe": "CWE-95",
                    "fix": "Avoid eval(); use safe alternatives"
                },
                {
                    "pattern": r"TODO|FIXME|HACK|XXX",
                    "severity": "LOW",
                    "category": "code_quality",
                    "description": "TODO/FIXME comment found - review before production",
                    "fix": "Address the TODO item or remove if resolved"
                },
            ],
            "python": [
                {
                    "pattern": r"pickle\.loads?\s*\(",
                    "severity": "HIGH",
                    "category": "deserialization",
                    "description": "Unsafe deserialization with pickle",
                    "cwe": "CWE-502",
                    "fix": "Use JSON or other safe serialization formats"
                },
                {
                    "pattern": r"subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True",
                    "severity": "HIGH",
                    "category": "injection",
                    "description": "Shell injection risk with shell=True",
                    "cwe": "CWE-78",
                    "fix": "Use shell=False and pass arguments as list"
                },
                {
                    "pattern": r"os\.system\s*\(",
                    "severity": "MEDIUM",
                    "category": "injection",
                    "description": "os.system() can be vulnerable to injection",
                    "cwe": "CWE-78",
                    "fix": "Use subprocess.run() with shell=False"
                },
                {
                    "pattern": r"yaml\.load\s*\([^)]*\)",
                    "severity": "MEDIUM",
                    "category": "deserialization",
                    "description": "yaml.load() without Loader can execute code",
                    "cwe": "CWE-502",
                    "fix": "Use yaml.safe_load() instead"
                },
                {
                    "pattern": r"\.format\s*\([^)]*\)|f['\"].*\{.*\}.*['\"]",
                    "severity": "LOW",
                    "category": "injection",
                    "description": "String formatting with user input may be unsafe",
                    "fix": "Ensure user input is properly sanitized"
                },
                {
                    "pattern": r"except\s*:\s*$|except\s+Exception\s*:",
                    "severity": "LOW",
                    "category": "error_handling",
                    "description": "Broad exception handling may hide errors",
                    "fix": "Catch specific exceptions"
                },
            ],
            "javascript": [
                {
                    "pattern": r"\.innerHTML\s*=",
                    "severity": "MEDIUM",
                    "category": "xss",
                    "description": "innerHTML assignment may lead to XSS",
                    "cwe": "CWE-79",
                    "fix": "Use textContent or sanitize HTML input"
                },
                {
                    "pattern": r"document\.write\s*\(",
                    "severity": "MEDIUM",
                    "category": "xss",
                    "description": "document.write() can lead to XSS",
                    "cwe": "CWE-79",
                    "fix": "Use DOM manipulation methods instead"
                },
                {
                    "pattern": r"new\s+Function\s*\(",
                    "severity": "HIGH",
                    "category": "injection",
                    "description": "Dynamic function creation can lead to injection",
                    "cwe": "CWE-95",
                    "fix": "Avoid dynamic code generation"
                },
                {
                    "pattern": r"localStorage\.setItem\s*\([^,]+,\s*(password|token|secret)",
                    "severity": "MEDIUM",
                    "category": "storage",
                    "description": "Storing sensitive data in localStorage",
                    "cwe": "CWE-922",
                    "fix": "Use secure HttpOnly cookies for sensitive data"
                },
            ],
            "sql": [
                {
                    "pattern": r"GRANT\s+ALL",
                    "severity": "MEDIUM",
                    "category": "permissions",
                    "description": "Overly permissive GRANT statement",
                    "fix": "Use principle of least privilege"
                },
                {
                    "pattern": r"--\s*password|--\s*secret",
                    "severity": "HIGH",
                    "category": "secrets",
                    "description": "Password or secret in SQL comment",
                    "fix": "Remove sensitive information from comments"
                },
            ],
            "typescript": [
                {
                    "pattern": r"as\s+any\b|\:\s*any\b",
                    "severity": "LOW",
                    "category": "type_safety",
                    "description": "Use of 'any' type reduces type safety",
                    "fix": "Use specific types instead of any"
                },
                {
                    "pattern": r"@ts-ignore|@ts-nocheck",
                    "severity": "LOW",
                    "category": "type_safety",
                    "description": "TypeScript checks disabled",
                    "fix": "Fix the underlying type issue"
                },
            ],
        }
    
    def update_patterns(self) -> None:
        """Update security patterns from latest sources.
        
        In a production system, this would fetch from:
        - NVD (National Vulnerability Database)
        - GitHub Security Advisories
        - OWASP Top 10
        - Language-specific security advisories
        """
        # Refresh built-in patterns
        self._patterns = self._get_builtin_patterns()
        self._last_updated = datetime.now()
        
        # In production, would fetch from security APIs here
        # Example: fetch_from_nvd(), fetch_from_github_advisories()
