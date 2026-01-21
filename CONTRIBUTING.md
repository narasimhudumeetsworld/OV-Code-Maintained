# Contributing to OV-Code-Maintained

Om Vinayaka! 🙏 Thank you for your interest in contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [AI-Assisted Contributions](#ai-assisted-contributions)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Types of Contributions

1. **Bug Reports**: Open an issue describing the bug
2. **Feature Requests**: Open an issue with your feature proposal
3. **Documentation**: Improve or add documentation
4. **Code**: Submit pull requests with improvements
5. **Examples**: Add working examples for others to learn from
6. **Specifications**: Contribute specification templates

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test your changes
5. Commit with meaningful messages
6. Push to your fork
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/OV-Code-Maintained.git
cd OV-Code-Maintained

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

## Contribution Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and small

### Commit Messages

Use clear, descriptive commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(llm): add Claude client support`
- `fix(validator): handle empty responses`
- `docs(readme): update installation steps`

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for >80% code coverage

```bash
# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src
```

## AI-Assisted Contributions

We welcome AI-assisted contributions! When using AI tools:

### Requirements

1. **Disclose AI Usage**: Mention in your PR if AI was used to generate code
2. **Review AI Output**: Always review and validate AI-generated code
3. **Test Thoroughly**: AI-generated code needs comprehensive testing
4. **Document Prompts**: Consider sharing prompts that generated useful code

### Quality Checks for AI Code

- [ ] Code has been reviewed by a human
- [ ] All tests pass
- [ ] No security vulnerabilities introduced
- [ ] Code follows project style guidelines
- [ ] Documentation is accurate and complete

### Prompt Contributions

When contributing prompt templates:

1. Include the prompt in `templates/prompt_templates/`
2. Document expected inputs and outputs
3. Add examples of generated code
4. Include validation criteria

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Template

Your PR description should include:

1. **What**: Brief description of changes
2. **Why**: Motivation for the change
3. **How**: Implementation approach
4. **Testing**: How changes were tested
5. **AI Disclosure**: Whether AI tools were used

### Review Process

1. Automated checks run (linting, tests)
2. Maintainer reviews the code
3. Feedback addressed
4. Approval and merge

## Questions?

If you have questions, feel free to:

- Open a discussion on GitHub
- Ask in the issues section
- Review existing documentation

Thank you for contributing to OV-Code-Maintained! 🎉
