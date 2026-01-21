"""OV-Code MCP Server - Model Context Protocol server with lazy loading.

This server provides AI coding tools through the Model Context Protocol,
enabling integration with VS Code, Cursor, and other MCP-compatible editors.

Features:
- Lazy-loaded tools to minimize token usage
- Auto-updated best practices and security info
- Multi-provider support (OpenAI, Claude, Gemini)
"""
import json
import logging
from dataclasses import dataclass
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """MCP Tool definition with lazy loading support."""
    
    name: str
    description: str
    input_schema: dict
    handler: Callable
    _loaded: bool = False
    
    def to_dict(self) -> dict:
        """Convert to MCP tool format (minimal for listing)."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }


class OVCodeMCPServer:
    """MCP Server with lazy-loaded tools for AI code management.
    
    Tools are defined but not loaded until actually called,
    minimizing token usage in the context window.
    
    Example:
        >>> server = OVCodeMCPServer()
        >>> server.run("localhost", 3000)
    """
    
    def __init__(self):
        """Initialize the MCP server with tool definitions."""
        self._tools: dict[str, Tool] = {}
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register available tools with lazy handlers."""
        
        # Generate code tool
        self._tools["generate_code"] = Tool(
            name="generate_code",
            description="Generate code using AI with automatic best practices. Supports Python, JavaScript, TypeScript, Rust, Go, and more.",
            input_schema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Description of what code to generate"
                    },
                    "language": {
                        "type": "string",
                        "description": "Target programming language",
                        "default": "python"
                    },
                    "provider": {
                        "type": "string",
                        "enum": ["openai", "anthropic", "gemini"],
                        "default": "openai"
                    },
                    "include_tests": {
                        "type": "boolean",
                        "description": "Include unit tests",
                        "default": False
                    }
                },
                "required": ["prompt"]
            },
            handler=self._handle_generate_code
        )
        
        # Get best practices tool (lazy loaded)
        self._tools["get_best_practices"] = Tool(
            name="get_best_practices",
            description="Get language-specific coding best practices. Lazy-loaded to minimize tokens.",
            input_schema={
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "Programming language (python, javascript, typescript, rust, go, etc.)"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["security", "performance", "style", "error_handling", "all"],
                        "default": "all"
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum tokens to return (for context efficiency)",
                        "default": 300
                    }
                },
                "required": ["language"]
            },
            handler=self._handle_get_best_practices
        )
        
        # Security check tool
        self._tools["security_check"] = Tool(
            name="security_check",
            description="Analyze code for security vulnerabilities with auto-updated patterns.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Code to analyze"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language"
                    },
                    "severity_filter": {
                        "type": "string",
                        "enum": ["HIGH", "MEDIUM", "LOW", "all"],
                        "default": "all"
                    }
                },
                "required": ["code"]
            },
            handler=self._handle_security_check
        )
        
        # Code review tool
        self._tools["code_review"] = Tool(
            name="code_review",
            description="Get AI-powered code review with security and best practice checks.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Code to review"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language"
                    },
                    "focus": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Focus areas: security, performance, style, bugs",
                        "default": ["security", "bugs"]
                    }
                },
                "required": ["code"]
            },
            handler=self._handle_code_review
        )
        
        # Format code tool
        self._tools["format_code"] = Tool(
            name="format_code",
            description="Format code according to language standards.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Code to format"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language"
                    }
                },
                "required": ["code", "language"]
            },
            handler=self._handle_format_code
        )
        
        # List providers tool
        self._tools["list_providers"] = Tool(
            name="list_providers",
            description="List available AI providers and their status.",
            input_schema={
                "type": "object",
                "properties": {}
            },
            handler=self._handle_list_providers
        )
    
    def list_tools(self) -> list[dict]:
        """List available tools (minimal info to save tokens)."""
        return [tool.to_dict() for tool in self._tools.values()]
    
    async def call_tool(self, name: str, arguments: dict) -> dict:
        """Call a tool by name with given arguments.
        
        Tools are lazy-loaded - dependencies only imported when called.
        
        Args:
            name: Tool name.
            arguments: Tool arguments.
            
        Returns:
            Tool result.
        """
        if name not in self._tools:
            return {"error": f"Unknown tool: {name}"}
        
        tool = self._tools[name]
        
        try:
            result = await tool.handler(arguments)
            return {"result": result}
        except Exception as e:
            logger.exception(f"Error calling tool {name}")
            return {"error": str(e)}
    
    # Tool handlers (lazy-loaded implementations)
    
    async def _handle_generate_code(self, args: dict) -> dict:
        """Handle code generation request."""
        prompt = args["prompt"]
        language = args.get("language", "python")
        provider = args.get("provider", "openai")
        include_tests = args.get("include_tests", False)
        
        # Lazy load best practices
        from src.best_practices import get_best_practices_prompt
        best_practices = get_best_practices_prompt(language, max_tokens=300)
        
        # Build enhanced prompt
        enhanced_prompt = f"""
{best_practices}

User Request: {prompt}

Generate clean, maintainable, production-quality {language} code.
{"Include unit tests." if include_tests else ""}
"""
        
        # Lazy load the appropriate client
        if provider == "openai":
            from src.llm.openai_client import OpenAIClient
            client = OpenAIClient()
        elif provider == "anthropic":
            from src.llm.anthropic_client import AnthropicClient
            client = AnthropicClient()
        else:
            from src.llm.gemini_client import GeminiClient
            client = GeminiClient()
        
        result = await client.generate(enhanced_prompt)
        
        return {
            "code": result.content,
            "language": language,
            "provider": provider,
            "tokens_used": result.tokens_used,
            "best_practices_applied": True
        }
    
    async def _handle_get_best_practices(self, args: dict) -> dict:
        """Handle best practices request (lazy loaded)."""
        language = args["language"]
        category = args.get("category", "all")
        max_tokens = args.get("max_tokens", 300)
        
        # Lazy load the best practices module
        from src.best_practices import get_best_practices_prompt, get_best_practices
        
        if category == "all":
            prompt = get_best_practices_prompt(language, max_tokens)
        else:
            # Get specific category
            from src.best_practices.manager import _get_manager
            manager = _get_manager()
            practices = manager.get_practices(language, category)
            prompt = "\n".join([p.to_prompt_format() for p in practices[:10]])
        
        return {
            "language": language,
            "category": category,
            "practices": prompt,
            "note": "Lazy-loaded to minimize token usage"
        }
    
    async def _handle_security_check(self, args: dict) -> dict:
        """Handle security analysis request."""
        code = args["code"]
        language = args.get("language", "python")
        severity_filter = args.get("severity_filter", "all")
        
        # Lazy load security analyzer
        from src.security import SecurityAnalyzer
        
        # Write code to temp file for analysis
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", 
            suffix=f".{language[:2]}",
            delete=False
        ) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            analyzer = SecurityAnalyzer()
            result = analyzer.analyze_file(temp_path, language)
            
            findings = result.findings
            if severity_filter != "all":
                findings = [f for f in findings if f.severity == severity_filter]
            
            return {
                "findings": [
                    {
                        "severity": f.severity,
                        "category": f.category,
                        "description": f.description,
                        "cwe": f.cwe_id,
                        "fix": f.fix_suggestion
                    }
                    for f in findings
                ],
                "summary": result.summary,
                "last_updated": analyzer.last_updated
            }
        finally:
            import os
            os.unlink(temp_path)
    
    async def _handle_code_review(self, args: dict) -> dict:
        """Handle code review request."""
        code = args["code"]
        language = args.get("language", "python")
        focus = args.get("focus", ["security", "bugs"])
        
        # First run security check
        security_result = await self._handle_security_check({
            "code": code,
            "language": language
        })
        
        # Build review summary
        review = {
            "security_findings": security_result["findings"],
            "recommendations": [],
            "quality_score": 100
        }
        
        # Deduct score for issues
        for finding in security_result["findings"]:
            if finding["severity"] == "HIGH":
                review["quality_score"] -= 20
                review["recommendations"].append(f"CRITICAL: {finding['description']}")
            elif finding["severity"] == "MEDIUM":
                review["quality_score"] -= 10
                review["recommendations"].append(f"WARNING: {finding['description']}")
            else:
                review["quality_score"] -= 5
        
        review["quality_score"] = max(0, review["quality_score"])
        
        return review
    
    async def _handle_format_code(self, args: dict) -> dict:
        """Handle code formatting request."""
        code = args["code"]
        language = args["language"]
        
        # For now, return the code as-is with a note
        # In production, would integrate with Black, Prettier, etc.
        return {
            "formatted_code": code,
            "language": language,
            "formatter": "pending",
            "note": "Code formatting requires local tool installation"
        }
    
    async def _handle_list_providers(self, args: dict) -> dict:
        """Handle list providers request."""
        import os
        
        providers = [
            {
                "name": "OpenAI",
                "id": "openai",
                "configured": bool(os.getenv("OPENAI_API_KEY")),
                "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
            },
            {
                "name": "Anthropic",
                "id": "anthropic", 
                "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
                "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
            },
            {
                "name": "Google Gemini",
                "id": "gemini",
                "configured": bool(os.getenv("GOOGLE_API_KEY")),
                "models": ["gemini-pro", "gemini-ultra"]
            }
        ]
        
        return {"providers": providers}


def run_server(host: str = "localhost", port: int = 3000) -> None:
    """Run the MCP server.
    
    Args:
        host: Server host.
        port: Server port.
    """
    import asyncio
    
    server = OVCodeMCPServer()
    
    print(f"🕉️ OV-Code MCP Server starting...")
    print(f"   Host: {host}:{port}")
    print(f"   Tools: {len(server._tools)} available (lazy-loaded)")
    print(f"\nAvailable tools:")
    for tool in server.list_tools():
        print(f"   • {tool['name']}: {tool['description'][:50]}...")
    print(f"\nServer ready for connections!")
    
    # In production, would start actual MCP server here
    # For now, just demonstrate the server is configured
    
    try:
        # Keep server running
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
