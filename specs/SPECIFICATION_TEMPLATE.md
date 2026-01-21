# Specification Template

## Overview

This template provides a structured format for writing specifications that AI systems can understand and generate high-quality code from. Research shows that structured requirements improve maintainability by 14-30%.

## Template Structure

### 1. Project Header

```yaml
# PROJECT SPECIFICATION
project_name: ""
version: "1.0.0"
author: ""
date: ""
status: "draft"  # draft, review, approved
```

### 2. Executive Summary

Provide a brief overview (2-3 sentences) of what the project does and its primary purpose.

### 3. Functional Requirements

List what the system must DO:

```markdown
## Functional Requirements

### FR-001: [Feature Name]
- **Priority**: High/Medium/Low
- **Description**: Clear description of the feature
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2
- **Dependencies**: List any dependencies

### FR-002: [Feature Name]
...
```

### 4. Non-Functional Requirements

List HOW the system should behave:

```markdown
## Non-Functional Requirements

### NFR-001: Performance
- Response time: < 200ms for API calls
- Throughput: 1000 requests/second
- Memory usage: < 512MB

### NFR-002: Security
- Authentication: JWT-based
- Data encryption: AES-256
- Input validation: Required

### NFR-003: Accessibility
- WCAG compliance level: AA
- Keyboard navigation: Required
- Screen reader support: Required
```

### 5. Technical Specifications

```markdown
## Technical Specifications

### Technology Stack
- Language: Python 3.10+
- Framework: FastAPI
- Database: PostgreSQL 15
- Cache: Redis

### Architecture
- Pattern: Microservices / Monolith
- API Style: REST / GraphQL
- Deployment: Docker / Kubernetes

### Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | ^0.100.0 | Web framework |
| sqlalchemy | ^2.0.0 | ORM |
```

### 6. Data Models

```markdown
## Data Models

### User
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier |
| email | String | Unique, Required | User email |
| name | String | Required | Display name |
| created_at | DateTime | Required | Creation timestamp |
```

### 7. API Endpoints

```markdown
## API Endpoints

### POST /api/users
- **Description**: Create a new user
- **Request Body**:
  ```json
  {
    "email": "string",
    "name": "string"
  }
  ```
- **Response**: 201 Created
  ```json
  {
    "id": "uuid",
    "email": "string",
    "name": "string",
    "created_at": "datetime"
  }
  ```
- **Errors**:
  - 400: Invalid input
  - 409: Email already exists
```

### 8. User Interface

```markdown
## User Interface

### Screen: Dashboard
- **Route**: /dashboard
- **Components**:
  - Header with navigation
  - Sidebar with menu
  - Main content area
- **States**:
  - Loading
  - Empty
  - Populated
  - Error
```

### 9. Testing Requirements

```markdown
## Testing Requirements

### Unit Tests
- Minimum coverage: 80%
- All public methods tested
- Edge cases covered

### Integration Tests
- API endpoint tests
- Database integration
- External service mocks

### E2E Tests
- Critical user flows
- Cross-browser testing
```

### 10. Constraints and Assumptions

```markdown
## Constraints
- Budget: $X
- Timeline: X weeks
- Team size: X developers

## Assumptions
- Users have modern browsers
- Network latency < 100ms
- Database available 99.9%
```

## Best Practices for AI Code Generation

1. **Be Specific**: Vague requirements lead to vague code
2. **Include Examples**: Show expected inputs/outputs
3. **Define Edge Cases**: How should errors be handled?
4. **Specify Style**: Reference coding standards
5. **Break Down Tasks**: Smaller tasks = better results

## Example Usage

See `specification_examples/` directory for complete examples.
