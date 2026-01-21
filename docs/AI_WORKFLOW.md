# AI Workflow Guide

This guide explains how to effectively use AI tools for code generation while maintaining code quality and human oversight.

## Overview

The AI workflow follows a structured process:

```
Specification → Context → Generation → Validation → Review → Integration
```

## Step 1: Write Specifications

Before generating any code, write a clear specification.

### Using the Template

1. Copy the specification template:
   ```bash
   cp specs/SPECIFICATION_TEMPLATE.md specs/my_feature_spec.md
   ```

2. Fill in all sections:
   - Executive Summary
   - Functional Requirements
   - Non-Functional Requirements
   - Technical Specifications
   - Data Models
   - API Endpoints

### Best Practices

- Be specific and detailed
- Include acceptance criteria
- Define edge cases
- Reference existing patterns

## Step 2: Build Context

Good context leads to better code generation.

### Using Context Engineering

Follow the CRISP framework (see `specs/CONTEXT_ENGINEERING.md`):

- **C**ontext: Project background
- **R**equirements: What needs to be done
- **I**nput/Output: Expected data formats
- **S**tyle: Coding conventions
- **P**atterns: Examples to follow

### Gathering Context

1. Review existing code patterns
2. Note relevant configuration
3. List constraints and requirements
4. Prepare examples of good code

## Step 3: Generate Code

Use AI tools with your prepared context.

### Using Prompt Templates

Find templates in `config/prompt_templates.yaml`:

```yaml
# Example usage
task_templates:
  backend_api:
    variables:
      - name
      - endpoints
      - database
```

### Generation Process

1. Select appropriate template
2. Fill in template variables
3. Add specific context
4. Submit to AI tool
5. Receive generated code

### Tips for Better Results

- Break large tasks into smaller pieces
- Provide examples of desired output
- Specify error handling requirements
- Include test requirements

## Step 4: Validate Output

All AI-generated code must be validated.

### Automated Validation

Run these checks on generated code:

```bash
# Syntax check
python -m py_compile generated_code.py

# Type checking
mypy generated_code.py

# Linting
ruff check generated_code.py

# Security scan
bandit generated_code.py

# Format code
black generated_code.py
```

### Validation Checklist

- [ ] Code compiles without errors
- [ ] Passes type checking
- [ ] Follows coding standards
- [ ] No security vulnerabilities
- [ ] Has appropriate error handling
- [ ] Includes documentation

## Step 5: Human Review

AI-generated code requires human review.

### Review Focus Areas

1. **Logic**: Does the code do what's intended?
2. **Security**: Are there any vulnerabilities?
3. **Performance**: Is it efficient?
4. **Maintainability**: Is it readable and maintainable?
5. **Testing**: Are there adequate tests?

### Review Checklist

- [ ] Requirements are met
- [ ] Code follows project patterns
- [ ] No hardcoded secrets
- [ ] Error handling is appropriate
- [ ] Tests cover main functionality
- [ ] Documentation is accurate

## Step 6: Integration

Integrate validated code into the project.

### Integration Steps

1. Create feature branch
2. Add generated code
3. Run full test suite
4. Update documentation
5. Create pull request
6. Complete code review
7. Merge to main

### Documentation

Track AI-generated code:

- Note which files were AI-generated
- Record prompts used (optional)
- Document any manual modifications

## Quality Gates

All AI code must pass these gates:

| Gate | Tool | Requirement |
|------|------|-------------|
| Lint | ruff | No errors |
| Types | mypy | No errors |
| Security | bandit | No high severity |
| Tests | pytest | 80% coverage |
| Review | Human | Approved |

## Common Patterns

### Pattern 1: Feature Development

```
1. Write spec → 2. Generate code → 3. Generate tests →
4. Validate → 5. Review → 6. Integrate
```

### Pattern 2: Bug Fix

```
1. Identify bug → 2. Write test case → 3. Generate fix →
4. Validate fix → 5. Review → 6. Integrate
```

### Pattern 3: Refactoring

```
1. Identify code → 2. Write spec for improvement →
3. Generate refactored code → 4. Verify behavior unchanged →
5. Review → 6. Integrate
```

## Troubleshooting

### Poor Code Quality

- Add more context to prompts
- Provide better examples
- Break task into smaller pieces

### Missing Requirements

- Review specification completeness
- Add acceptance criteria
- Include edge cases

### Security Issues

- Always run security scans
- Review external dependencies
- Check for hardcoded values
