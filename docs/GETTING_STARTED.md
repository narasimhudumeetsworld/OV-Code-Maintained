# Getting Started Guide

Welcome to OV-Code-Maintained! This guide will help you set up the project and start managing AI-generated code.

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Git
- An API key from OpenAI or Anthropic (optional, for AI features)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/narasimhudumeetsworld/OV-Code-Maintained.git
cd OV-Code-Maintained
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Add your API keys for OpenAI or Anthropic
```

## Quick Start

### Using Specification Templates

1. Navigate to `specs/`
2. Copy `SPECIFICATION_TEMPLATE.md` to create your spec
3. Fill in the details for your project

```bash
cp specs/SPECIFICATION_TEMPLATE.md specs/my_project_spec.md
# Edit specs/my_project_spec.md with your requirements
```

### Using Prompt Templates

1. Find templates in `templates/prompt_templates/`
2. Use them with your preferred AI tool
3. Customize as needed

### Running Examples

Check out working examples in `examples/`:

```bash
# View minimal web app example
cd examples/minimal_web_app
# Open app.html in your browser
```

## Project Structure Quick Reference

| Directory | Purpose |
|-----------|---------|
| `config/` | Configuration files |
| `specs/` | Specification templates |
| `src/` | Source code |
| `docs/` | Documentation |
| `templates/` | Reusable templates |
| `examples/` | Working examples |
| `tests/` | Test suites |
| `scripts/` | Automation scripts |
| `standards/` | Coding standards |

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/unit/test_validators.py
```

## Next Steps

1. Read the [Architecture Overview](ARCHITECTURE.md)
2. Learn about [AI Workflow](AI_WORKFLOW.md)
3. Review [Maintenance Guide](MAINTENANCE.md)
4. Check [Coding Standards](../standards/CODING_STANDARDS.md)

## Getting Help

- Review existing documentation in `docs/`
- Check examples in `examples/`
- Open an issue on GitHub
- Review `CONTRIBUTING.md` for contribution guidelines

## Common Issues

### API Key Not Working

1. Verify your API key is correct in `.env`
2. Check that the key has the required permissions
3. Ensure you have sufficient credits/quota

### Tests Failing

1. Ensure all dependencies are installed
2. Check Python version (3.10+ required)
3. Run `pip install -r requirements.txt` again

### Import Errors

1. Verify virtual environment is activated
2. Install package in development mode:
   ```bash
   pip install -e .
   ```
