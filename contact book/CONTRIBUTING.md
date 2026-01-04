# Contributing to SmartConnect

Thank you for your interest in contributing to SmartConnect Contact Management System! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git for version control
- Basic knowledge of Python, SQLite, and GUI development

### Development Setup
1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/smartconnect.git
   cd smartconnect
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application** to ensure everything works:
   ```bash
   python run.py
   ```

## 🔧 Development Guidelines

### Code Style
- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all classes and functions
- Keep functions **small and focused** (single responsibility)
- Use **meaningful variable names**

### Project Structure
```
contact book/
├── run.py                      # Application launcher
├── smartconnect_with_login.py  # Main application
├── auth_system.py              # Authentication system
├── database.py                 # Database operations
├── contact_manager.py          # Contact business logic
├── models.py                   # Data models
├── validation.py               # Input validation
├── search_engine.py            # Search functionality
└── admin_*.py                  # Admin components
```

### Database Changes
- **Never modify existing tables** directly in production
- Create **migration scripts** for schema changes
- Test database changes with **sample data**
- Ensure **backward compatibility** when possible

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_auth_system.py

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

### Writing Tests
- Write **unit tests** for new functions
- Include **integration tests** for workflows
- Test **error conditions** and edge cases
- Use **descriptive test names**

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflows
- **Property Tests**: Random input validation (using Hypothesis)
- **GUI Tests**: User interface testing

## 📝 Submitting Changes

### Pull Request Process
1. **Create a feature branch** from main:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test thoroughly**:
   - Run existing tests: `python -m pytest`
   - Test manually with the GUI
   - Verify no regressions

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: New contact export feature"
   git commit -m "Fix: Login validation error handling"
   git commit -m "Update: Improve search performance"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Screenshots for UI changes
   - Test results and coverage
   - Breaking changes (if any)

### Commit Message Format
```
Type: Brief description (50 chars max)

Detailed explanation of what and why (if needed).
Include any breaking changes or migration notes.

Fixes #123
```

**Types**: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Test`, `Doc`

## 🐛 Bug Reports

### Before Reporting
- **Search existing issues** to avoid duplicates
- **Test with latest version** from main branch
- **Try with default admin account** (admin@smartconnect.com / admin123)

### Bug Report Template
```markdown
**Bug Description**
Clear description of what went wrong.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Enter '...'
4. See error

**Expected Behavior**
What should have happened.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g. Windows 10, macOS 12, Ubuntu 20.04]
- Python Version: [e.g. 3.9.7]
- CustomTkinter Version: [e.g. 5.2.0]

**Additional Context**
Any other relevant information.
```

## ✨ Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've considered.

**Additional Context**
Mockups, examples, or references.
```

## 🔒 Security

### Reporting Security Issues
- **DO NOT** create public issues for security vulnerabilities
- Email security concerns privately
- Include detailed reproduction steps
- Allow time for fixes before public disclosure

### Security Guidelines
- Never commit **passwords** or **API keys**
- Use **bcrypt** for password hashing (already implemented)
- Validate **all user inputs**
- Follow **principle of least privilege**
- Log **security-relevant events**

## 📚 Documentation

### Code Documentation
- **Docstrings** for all public functions and classes
- **Inline comments** for complex logic
- **Type hints** for better IDE support
- **README updates** for new features

### Documentation Style
```python
def create_contact(self, contact_data: dict) -> tuple[bool, str]:
    """
    Create a new contact in the database.
    
    Args:
        contact_data (dict): Contact information including name, phone, email
        
    Returns:
        tuple[bool, str]: (success, message) - Success status and result message
        
    Raises:
        ValidationError: If contact data is invalid
        DatabaseError: If database operation fails
    """
```

## 🎯 Areas for Contribution

### High Priority
- **Performance optimization** for large contact lists
- **Import/Export features** (vCard, CSV, JSON)
- **Advanced search** with filters and sorting
- **Backup and restore** improvements
- **Mobile-responsive design** preparation

### Medium Priority
- **Internationalization** (i18n) support
- **Plugin system** for extensions
- **Contact categories** and tags
- **Data synchronization** features
- **Accessibility improvements**

### Low Priority
- **Themes and customization**
- **Contact photos** and avatars
- **Integration** with external services
- **Advanced reporting** features
- **Contact sharing** capabilities

## 🤝 Community Guidelines

### Code of Conduct
- Be **respectful** and **inclusive**
- **Help others** learn and grow
- **Constructive feedback** only
- **No harassment** or discrimination
- **Professional communication**

### Getting Help
- **Read the documentation** first (README.md, SYSTEM_ARCHITECTURE.md)
- **Search existing issues** and discussions
- **Ask specific questions** with context
- **Provide minimal reproducible examples**
- **Be patient** - maintainers are volunteers

## 📋 Checklist for Contributors

### Before Submitting PR
- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated (if needed)
- [ ] No sensitive data in commits
- [ ] Commit messages are clear
- [ ] PR description is complete

### For Maintainers
- [ ] Code review completed
- [ ] Tests pass in CI
- [ ] Documentation is accurate
- [ ] Breaking changes documented
- [ ] Version bump (if needed)
- [ ] Changelog updated

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page
- **Special thanks** in documentation

## 📞 Contact

For questions about contributing:
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For general questions and ideas
- **Code Review**: Through pull request comments

---

**Thank you for contributing to SmartConnect! 🚀**

*Together we can build the best contact management system for everyone.*