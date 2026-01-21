# Minimal Web App Example

A simple task manager demonstrating OV-Code best practices.

## Features

- Add, complete, and delete tasks
- Persistent storage (localStorage)
- Accessible UI
- Security best practices (XSS prevention)

## Best Practices Demonstrated

### JavaScript
- Use `const`/`let` instead of `var`
- Use `textContent` instead of `innerHTML` (XSS prevention)
- Proper error handling with try/catch
- Accessible UI with ARIA labels
- Clean, documented code

### HTML
- Semantic HTML structure
- Accessible form elements
- Responsive design

### CSS
- Mobile-first approach
- CSS custom properties
- Smooth transitions

## Running

Simply open `index.html` in a browser. No build step required.

## Generated With

This example was generated using OV-Code CLI with automatic best practices:

```bash
ov-code generate -p openai -l javascript -t "Create a task manager web app"
```
