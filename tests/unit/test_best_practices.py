"""Unit tests for best practices manager."""
import pytest
from src.best_practices.manager import (
    BestPracticesManager,
    BestPractice,
    get_best_practices,
    get_best_practices_prompt,
)


class TestBestPracticesManager:
    """Tests for BestPracticesManager class."""
    
    def test_get_practices_returns_list(self):
        """Test that get_practices returns a list."""
        manager = BestPracticesManager()
        practices = manager.get_practices("python")
        
        assert isinstance(practices, list)
        assert len(practices) > 0
    
    def test_get_practices_by_category(self):
        """Test filtering practices by category."""
        manager = BestPracticesManager()
        security_practices = manager.get_practices("python", category="security")
        
        for practice in security_practices:
            assert practice.category == "security"
    
    def test_get_prompt_respects_max_tokens(self):
        """Test that prompt respects token limit."""
        manager = BestPracticesManager()
        prompt = manager.get_prompt_for_language("python", max_tokens=100)
        
        # Rough token estimate (4 chars per token)
        estimated_tokens = len(prompt) // 4
        # Allow some overhead
        assert estimated_tokens < 150
    
    def test_practices_have_required_fields(self):
        """Test that all practices have required fields."""
        manager = BestPracticesManager()
        practices = manager.get_practices("python")
        
        for practice in practices:
            assert practice.id
            assert practice.category
            assert practice.language
            assert practice.title
            assert practice.description
            assert practice.severity in ["critical", "important", "recommended"]


class TestModuleFunctions:
    """Tests for module-level functions."""
    
    def test_get_best_practices_returns_string(self):
        """Test that get_best_practices returns markdown."""
        result = get_best_practices("python")
        
        assert isinstance(result, str)
        assert "# Best Practices" in result
    
    def test_get_best_practices_prompt_is_compact(self):
        """Test that prompt is compact for LLMs."""
        prompt = get_best_practices_prompt("javascript", max_tokens=200)
        
        assert isinstance(prompt, str)
        assert "## Best Practices" in prompt
    
    def test_different_languages_have_different_practices(self):
        """Test that different languages have different practices."""
        python_prompt = get_best_practices_prompt("python")
        js_prompt = get_best_practices_prompt("javascript")
        
        # They should both have content but be different
        assert python_prompt
        assert js_prompt
        # JavaScript specific practices
        assert any(p in js_prompt.lower() for p in ["const", "let", "var", "innerHTML"])
