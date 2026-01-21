#!/usr/bin/env python3
"""OV-Code CLI - Unified AI Code Management Tool.

A command-line interface for managing AI-generated code across multiple
providers including GitHub Copilot, Claude, and Gemini.

Usage:
    ov-code generate --provider openai --prompt "Create a REST API"
    ov-code validate path/to/file.py
    ov-code best-practices python
    ov-code security-check path/to/file.py
"""
import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

import click

# Lazy import for rich to save startup time
_console = None

def get_console():
    """Lazy load rich console."""
    global _console
    if _console is None:
        from rich.console import Console
        _console = Console()
    return _console


BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║     🕉️  OV-Code - AI Code Management CLI                      ║
║     Om Vinayaka - Making AI Code Maintainable                 ║
╚═══════════════════════════════════════════════════════════════╝
"""

PROVIDERS = ["openai", "anthropic", "gemini", "copilot"]


def get_client(provider: str, model: Optional[str] = None):
    """Get the appropriate LLM client for the provider (lazy loaded)."""
    if provider == "openai" or provider == "copilot":
        from src.llm.openai_client import OpenAIClient
        return OpenAIClient(model=model or "gpt-4")
    elif provider == "anthropic":
        from src.llm.anthropic_client import AnthropicClient
        return AnthropicClient(model=model or "claude-3-sonnet-20240229")
    elif provider == "gemini":
        from src.llm.gemini_client import GeminiClient
        return GeminiClient(model=model or "gemini-pro")
    else:
        raise ValueError(f"Unknown provider: {provider}")


@click.group()
@click.version_option(version="0.1.0", prog_name="ov-code")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """🕉️ OV-Code - Unified AI Code Management CLI.
    
    Manage AI-generated code across multiple providers including
    GitHub Copilot, Claude, and Gemini.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@cli.command()
@click.option("--provider", "-p", type=click.Choice(PROVIDERS), default="openai", help="AI provider")
@click.option("--model", "-m", help="Specific model to use")
@click.option("--prompt", "-t", required=True, help="Prompt for code generation")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--language", "-l", default="python", help="Target programming language")
@click.option("--stream", is_flag=True, help="Stream output in real-time")
@click.pass_context
def generate(ctx, provider, model, prompt, output, language, stream):
    """Generate code using AI providers with automatic best practices."""
    console = get_console()
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.progress import Progress, SpinnerColumn, TextColumn
    
    console.print(BANNER, style="cyan")
    
    # Lazy load best practices for the language
    from src.best_practices import get_best_practices_prompt
    best_practices = get_best_practices_prompt(language)
    
    # Enhance prompt with best practices
    enhanced_prompt = f"""
{best_practices}

User Request: {prompt}

Generate clean, maintainable, production-quality code following the best practices above.
"""
    
    console.print(f"\n[bold]Provider:[/bold] {provider}")
    console.print(f"[bold]Language:[/bold] {language}")
    console.print(f"[bold]Best Practices:[/bold] Automatically applied ✓")
    console.print()
    
    async def run_generation():
        client = get_client(provider, model)
        
        if stream:
            console.print("[bold green]Generated Code:[/bold green]\n")
            full_content = ""
            async for chunk in client.generate_stream(enhanced_prompt):
                console.print(chunk, end="")
                full_content += chunk
            console.print()
            return full_content
        else:
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
                progress.add_task("Generating code with best practices...", total=None)
                result = await client.generate(enhanced_prompt)
            
            console.print(Panel(
                Syntax(result.content, language, theme="monokai"),
                title="[bold green]Generated Code[/bold green]",
                border_style="green"
            ))
            return result.content
    
    try:
        content = asyncio.run(run_generation())
        if output:
            Path(output).write_text(content)
            console.print(f"\n[green]✓ Code saved to {output}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command("best-practices")
@click.argument("language")
@click.option("--category", "-c", help="Specific category (security, performance, style)")
@click.option("--update", is_flag=True, help="Update to latest best practices")
@click.pass_context
def best_practices(ctx, language, category, update):
    """Show or update best practices for a programming language.
    
    Examples:
        ov-code best-practices python
        ov-code best-practices javascript --category security
        ov-code best-practices rust --update
    """
    console = get_console()
    from rich.markdown import Markdown
    from rich.panel import Panel
    
    console.print(BANNER, style="cyan")
    
    if update:
        from src.best_practices import update_best_practices
        console.print(f"\n[bold]Updating best practices for {language}...[/bold]")
        update_best_practices(language)
        console.print("[green]✓ Best practices updated![/green]")
        return
    
    from src.best_practices import get_best_practices
    practices = get_best_practices(language, category)
    
    console.print(Panel(
        Markdown(practices),
        title=f"[bold blue]Best Practices: {language.upper()}[/bold blue]",
        border_style="blue"
    ))


@cli.command("security-check")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--language", "-l", help="Override language detection")
@click.option("--fix", is_flag=True, help="Suggest fixes for issues")
@click.pass_context
def security_check(ctx, file_path, language, fix):
    """Run security analysis with latest vulnerability database.
    
    Examples:
        ov-code security-check app.py
        ov-code security-check src/ --fix
    """
    console = get_console()
    from rich.table import Table
    from rich.panel import Panel
    
    console.print(BANNER, style="cyan")
    console.print(f"\n[bold]Security Analysis:[/bold] {file_path}\n")
    
    # Lazy load security module
    from src.security import SecurityAnalyzer
    
    analyzer = SecurityAnalyzer()
    results = analyzer.analyze_file(file_path, language)
    
    # Display results
    table = Table(title="Security Findings")
    table.add_column("Severity", style="bold")
    table.add_column("Issue")
    table.add_column("Location")
    table.add_column("CWE")
    
    for finding in results.findings:
        severity_color = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "blue"}.get(finding.severity, "white")
        table.add_row(
            f"[{severity_color}]{finding.severity}[/{severity_color}]",
            finding.description,
            finding.location,
            finding.cwe_id or "-"
        )
    
    if results.findings:
        console.print(table)
        if fix:
            console.print("\n[bold]Suggested Fixes:[/bold]")
            for finding in results.findings:
                if finding.fix_suggestion:
                    console.print(f"  • {finding.fix_suggestion}")
    else:
        console.print("[green]✓ No security issues found![/green]")
    
    console.print(f"\n[dim]Security database last updated: {analyzer.last_updated}[/dim]")


@cli.command()
@click.option("--host", default="localhost", help="Server host")
@click.option("--port", default=3000, help="Server port")
@click.pass_context
def serve(ctx, host, port):
    """Start the MCP server for IDE integration.
    
    Starts a Model Context Protocol server with lazy-loaded tools
    for efficient token usage.
    """
    console = get_console()
    console.print(BANNER, style="cyan")
    console.print(f"\n[bold]Starting MCP Server (lazy-loading enabled)...[/bold]")
    console.print(f"Host: {host}:{port}")
    console.print("[dim]Tools are lazy-loaded to minimize token usage[/dim]\n")
    
    from src.mcp.server import run_server
    run_server(host, port)


@cli.command()
@click.pass_context
def providers(ctx):
    """List available AI providers and their status."""
    console = get_console()
    from rich.table import Table
    
    console.print(BANNER, style="cyan")
    
    table = Table(title="Available Providers")
    table.add_column("Provider")
    table.add_column("API Key")
    table.add_column("Model")
    table.add_column("Status")
    
    provider_info = [
        ("OpenAI/Copilot", "OPENAI_API_KEY", "gpt-4"),
        ("Anthropic/Claude", "ANTHROPIC_API_KEY", "claude-3-sonnet"),
        ("Google Gemini", "GOOGLE_API_KEY", "gemini-pro"),
    ]
    
    for name, env_var, model in provider_info:
        has_key = bool(os.getenv(env_var))
        status = "[green]✓ Ready[/green]" if has_key else f"[yellow]Set {env_var}[/yellow]"
        key_status = "[green]✓[/green]" if has_key else "[red]✗[/red]"
        table.add_row(name, key_status, model, status)
    
    console.print(table)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
