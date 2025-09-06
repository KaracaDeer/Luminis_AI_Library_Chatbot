# Contributing to Luminis.AI Library Assistant

Thank you for your interest in contributing to Luminis.AI! This document provides comprehensive guidelines and information for contributors.

## 🚀 Quick Start Guide

### 1. Fork the Repository
- Go to [Luminis.AI Library Assistant](https://github.com/yourusername/luminis-ai-library)
- Click the "Fork" button in the top-right corner
- This creates your own copy of the project

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/luminis-ai-library.git
cd luminis-ai-library
```

### 3. Set Up Upstream Remote
```bash
git remote add upstream https://github.com/yourusername/luminis-ai-library.git
git fetch upstream
```

### 4. Create a Feature Branch
```bash
# For new features
git checkout -b feature/amazing-feature

# For bug fixes
git checkout -b fix/bug-description

# For documentation
git checkout -b docs/improvement
```

### 5. Make Your Changes
- Write your code
- Add tests if applicable
- Update documentation
- Follow our coding standards

### 6. Commit Your Changes
```bash
git add .
git commit -m "Add amazing feature: brief description

- Detailed explanation of changes
- Fixes #123 (if applicable)
- Breaking changes: none"
```

### 7. Push to Your Branch
```bash
git push origin feature/amazing-feature
```

### 8. Create a Pull Request
- Go to your fork on GitHub
- Click "New Pull Request"
- Select your branch
- Fill out the PR template
- Submit!

## 📋 What We're Looking For

### 🎯 High Priority Contributions
- **Bug fixes** - Help us squash those pesky bugs
- **Performance improvements** - Make the app faster and more efficient
- **Security enhancements** - Keep our users safe and secure
- **Documentation improvements** - Make it easier for others to understand

### 🔧 Medium Priority Contributions
- **New features** - Add cool functionality that users will love
- **UI/UX improvements** - Make the interface more beautiful and intuitive
- **Test coverage** - Help us maintain high code quality
- **Code refactoring** - Clean up and improve the codebase

### ✨ Low Priority Contributions
- **Cosmetic changes** - Polish the interface and make it shine
- **Minor optimizations** - Small improvements that add up
- **Additional examples** - Help users understand how to use features

## 🛠️ Development Setup

### Prerequisites
- **Node.js** 18+ 
- **Python** 3.11+
- **Git** 2.20+
- **Code editor** (VS Code recommended)

### Local Development
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/luminis-ai-library.git
cd luminis-ai-library

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Start development servers
npm run dev

# Run tests
npm test
python -m pytest
```

### Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
# Add your OpenAI API key for AI features
```

## 📝 Code Style Guidelines

### Python (Backend)
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all functions
- Write comprehensive docstrings
- Maximum line length: 88 characters (use Black formatter)
- Use meaningful variable and function names

### TypeScript/React (Frontend)
- Use TypeScript strict mode
- Follow React best practices and hooks
- Use functional components with hooks
- Prefer named exports over default exports
- Use meaningful variable and function names
- Follow our component naming conventions

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Add feature" not "Adds feature")
- Limit the first line to 72 characters
- Reference issues and pull requests when applicable
- Use conventional commit format: `type(scope): description`

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_api.py

# Run tests in watch mode
python -m pytest --watch
```

### Frontend Tests
```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test -- --testPathPattern=ChatPage
```

### Integration Tests
```bash
# Run integration tests
npm run test:integration

# Run all tests
npm run test:all
```

## 📚 Documentation

### What to Document
- Update README.md if you add new features
- Add JSDoc comments for new functions
- Update API documentation if endpoints change
- Include examples in your documentation
- Update component documentation

### Documentation Standards
- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep documentation up-to-date

## 🔒 Security Guidelines

### What NOT to Commit
- API keys or secrets
- Database credentials
- Personal information
- Environment-specific configuration

### Security Best Practices
- Use environment variables for configuration
- Follow the principle of least privilege
- Validate all user inputs
- Report security vulnerabilities privately
- Use secure coding practices

## 🚀 Pull Request Process

### Before Submitting
1. **Ensure** your code follows style guidelines
2. **Add** tests for new functionality
3. **Update** documentation as needed
4. **Test** your changes thoroughly
5. **Check** that all tests pass

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring
- [ ] Test addition
- [ ] Other (please describe)

## Testing
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
- [ ] Security considerations addressed
```

### Review Process
1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Address feedback** and make changes
4. **Approval** from maintainers
5. **Merge** into main branch

## 🎯 Areas for Contribution

### Frontend
- React components and hooks
- UI/UX improvements
- Performance optimizations
- Accessibility enhancements
- Mobile responsiveness

### Backend
- API endpoints and services
- Database operations
- AI/ML integrations
- Performance improvements
- Security enhancements

### Infrastructure
- CI/CD pipelines
- Testing frameworks
- Documentation
- Development tools

## 📞 Getting Help

### Resources
- **Issues**: [GitHub Issues](https://github.com/yourusername/luminis-ai-library/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/luminis-ai-library/discussions)
- **Documentation**: [Project Wiki](https://github.com/yourusername/luminis-ai-library/wiki)
- **LinkedIn**: [Luminis.AI LinkedIn](https://linkedin.com/company/luminis-ai)
- **Email**: support@luminis.ai

### Community
- Join our Discord server
- Participate in discussions
- Ask questions in issues
- Share your ideas

## 🙏 Recognition

### How Contributors Are Recognized
- **README.md** - Listed in contributors section
- **Release notes** - Mentioned in version releases
- **Contributor hall of fame** - Special recognition
- **GitHub profile** - Contributions graph

### Contribution Levels
- **Bronze**: 1-5 contributions
- **Silver**: 6-15 contributions  
- **Gold**: 16+ contributions
- **Platinum**: Major contributions

## 🚫 What NOT to Do

- Don't submit incomplete work
- Don't ignore code review feedback
- Don't commit without testing
- Don't break existing functionality
- Don't ignore security concerns

## ✅ What TO Do

- Do test your changes thoroughly
- Do follow our coding standards
- Do update documentation
- Do be respectful and helpful
- Do ask questions when unsure

---

<div align="center">
  <strong>Thank you for contributing to Luminis.AI! 🚀</strong><br>
  <em>Together, we're building the future of AI-powered libraries</em>
</div>
