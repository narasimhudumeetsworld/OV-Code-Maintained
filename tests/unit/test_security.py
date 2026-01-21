"""Unit tests for security analyzer."""
import pytest
import tempfile
from pathlib import Path
from src.security.analyzer import SecurityAnalyzer, SecurityFinding, AnalysisResult


class TestSecurityAnalyzer:
    """Tests for SecurityAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = SecurityAnalyzer()
    
    def test_analyzer_initializes(self):
        """Test that analyzer initializes properly."""
        assert self.analyzer is not None
        assert self.analyzer.last_updated is not None
    
    def test_detect_hardcoded_secret(self, sample_python_code):
        """Test detection of hardcoded secrets."""
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(sample_python_code)
                f.flush()
                temp_path = f.name
            
            result = self.analyzer.analyze_file(temp_path, "python")
            
            # Should find the hardcoded password
            secret_findings = [f for f in result.findings if f.category == "secrets"]
            assert len(secret_findings) > 0
        finally:
            if temp_path:
                Path(temp_path).unlink(missing_ok=True)
    
    def test_detect_xss_in_javascript(self, sample_javascript_code):
        """Test detection of XSS vulnerabilities in JavaScript."""
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(sample_javascript_code)
                f.flush()
                temp_path = f.name
            
            result = self.analyzer.analyze_file(temp_path, "javascript")
            
            # Should find innerHTML usage
            xss_findings = [f for f in result.findings if f.category == "xss"]
            assert len(xss_findings) > 0
        finally:
            if temp_path:
                Path(temp_path).unlink(missing_ok=True)
    
    def test_clean_code_has_no_findings(self):
        """Test that clean code has no security findings."""
        clean_code = '''
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(clean_code)
                f.flush()
                temp_path = f.name
            
            result = self.analyzer.analyze_file(temp_path, "python")
            
            # Filter out LOW severity (like TODO comments)
            high_medium = [f for f in result.findings if f.severity in ["HIGH", "MEDIUM"]]
            assert len(high_medium) == 0
        finally:
            if temp_path:
                Path(temp_path).unlink(missing_ok=True)
    
    def test_result_summary(self):
        """Test that result provides correct summary."""
        result = AnalysisResult(
            file_path="test.py",
            language="python",
            findings=[
                SecurityFinding("HIGH", "secrets", "test", "test.py:1"),
                SecurityFinding("MEDIUM", "xss", "test", "test.py:2"),
                SecurityFinding("LOW", "style", "test", "test.py:3"),
            ]
        )
        
        summary = result.summary
        assert summary["HIGH"] == 1
        assert summary["MEDIUM"] == 1
        assert summary["LOW"] == 1
        assert result.has_critical is True


class TestSecurityFinding:
    """Tests for SecurityFinding dataclass."""
    
    def test_finding_creation(self):
        """Test creating a security finding."""
        finding = SecurityFinding(
            severity="HIGH",
            category="injection",
            description="SQL injection detected",
            location="app.py:42",
            cwe_id="CWE-89",
            fix_suggestion="Use parameterized queries"
        )
        
        assert finding.severity == "HIGH"
        assert finding.cwe_id == "CWE-89"
        assert finding.fix_suggestion is not None
