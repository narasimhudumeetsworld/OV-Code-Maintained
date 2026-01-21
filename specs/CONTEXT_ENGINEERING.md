# Context Engineering Guide

## Introduction

Context Engineering is the practice of structuring information provided to AI systems to maximize the quality and relevance of generated outputs. This guide covers best practices for crafting effective prompts and context.

## The CRISP Framework

Use the CRISP framework for structuring prompts:

### C - Context
Provide background information about the project, codebase, and environment.

```markdown
Context:
- This is a Python FastAPI application
- We use SQLAlchemy for ORM
- The codebase follows PEP 8 style guide
- Existing patterns: Repository pattern, Dependency Injection
```

### R - Requirements
Clearly state what needs to be done.

```markdown
Requirements:
- Create a user registration endpoint
- Validate email format
- Hash passwords using bcrypt
- Return JWT token on success
```

### I - Input/Output
Define expected inputs and outputs with examples.

```markdown
Input:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

Output:
{
  "user_id": "uuid",
  "token": "jwt_token",
  "expires_in": 3600
}
```

### S - Style
Specify coding style and conventions.

```markdown
Style:
- Use type hints
- Include docstrings (Google style)
- Error handling with custom exceptions
- Logging for important operations
```

### P - Patterns
Reference existing patterns or examples to follow.

```markdown
Patterns:
- Follow the existing user service pattern in `src/services/user_service.py`
- Use the base repository class from `src/repositories/base.py`
- Error handling similar to `src/exceptions/handlers.py`
```

## Prompt Templates

### Code Generation Prompt

```
You are generating code for [PROJECT NAME].

## Context
[Project background, tech stack, existing patterns]

## Task
[What needs to be created]

## Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Expected Output
[Description of expected code structure]

## Examples
[Code examples from existing codebase]

## Quality Criteria
- [ ] Follows coding standards
- [ ] Includes error handling
- [ ] Has unit tests
- [ ] Is documented
```

### Code Review Prompt

```
Review the following code for:

## Code
```[language]
[code to review]
```

## Criteria
1. Security vulnerabilities
2. Performance issues
3. Code quality
4. Best practice violations
5. Potential bugs

## Context
- Language: [language]
- Framework: [framework]
- Purpose: [what the code does]

Provide:
1. Issues found (severity: high/medium/low)
2. Specific line references
3. Suggested fixes
```

### Refactoring Prompt

```
Refactor the following code to improve [specific aspect].

## Current Code
```[language]
[current code]
```

## Refactoring Goals
- [Goal 1]
- [Goal 2]

## Constraints
- Maintain existing behavior
- Keep public interface unchanged
- [Other constraints]

## Style Guide
[Link to or excerpt from style guide]
```

## Advanced Techniques

### Few-Shot Learning
Provide examples of desired output:

```
Here are examples of well-written functions in this codebase:

Example 1:
```python
def get_user_by_id(user_id: UUID) -> User:
    """Retrieve a user by their unique identifier.
    
    Args:
        user_id: The unique identifier of the user.
        
    Returns:
        User object if found.
        
    Raises:
        UserNotFoundError: If no user exists with the given ID.
    """
    user = self.repository.find_by_id(user_id)
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    return user
```

Now create a similar function for [new requirement].
```

### Chain-of-Thought
Break complex tasks into steps:

```
Let's approach this step by step:

1. First, analyze the existing data models
2. Then, design the new model relationships
3. Next, create the database migrations
4. Finally, implement the repository methods

Start with step 1: Analyze the existing models in `src/models/`
```

### Role Assignment
Assign a specific role:

```
You are a senior Python developer with 10 years of experience 
in building scalable web applications. You specialize in:
- Clean architecture
- Test-driven development
- API design

Your task is to...
```

## Context Window Management

### Prioritize Information
1. Most relevant code examples first
2. Direct requirements
3. Constraints and guidelines
4. Background context

### Use Summarization
For large codebases, summarize:

```
# Project Summary
- 50 Python modules across 5 packages
- Uses FastAPI for REST API
- PostgreSQL database with SQLAlchemy ORM
- ~15,000 lines of production code

# Relevant Files for This Task
[Include only directly relevant code]
```

### Reference External Resources
```
For coding standards, refer to our documented standards at:
config/code_standards.yaml

Key points:
- [Extract most relevant points]
```

## Anti-Patterns to Avoid

1. **Vague Instructions**: "Make it better" → "Reduce function complexity below 10"
2. **Missing Context**: "Add authentication" → "Add JWT authentication to the FastAPI app"
3. **Overloading**: Too much information → Focus on task-relevant details
4. **Implicit Assumptions**: State all assumptions explicitly

## Measuring Success

Track these metrics for prompt effectiveness:
- First-attempt success rate
- Code review feedback frequency
- Time to production-ready code
- Consistency with existing codebase
