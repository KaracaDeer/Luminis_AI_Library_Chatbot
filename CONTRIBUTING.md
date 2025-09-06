# 🤝 Contributing Guide

Thank you for your interest in contributing to the Luminis.AI Library Assistant project!

## 🚀 Quick Start

### 1. Fork the Repository
```bash
git fork https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot
```

### 2. Clone the Project
```bash
git clone https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot
cd Luminis_AI_Library_Chatbot
```

### 3. Install Dependencies
```bash
npm run install-deps
```

### 4. Start Development Environment
```bash
npm run dev
```

## 🛠️ Development Process

### Adding New Features
1. **Create Issue**: Discuss the new feature
2. **Create Branch**: `feature/new-feature-name`
3. **Write Code**: Include tests
4. **Test**: `npm run test`
5. **Submit Pull Request**

### Fixing Bugs
1. **Create Issue**: Report the bug
2. **Create Branch**: `fix/bug-description`
3. **Make Fix**: Include tests
4. **Test**: `npm run test`
5. **Submit Pull Request**

## 📋 Code Standards

### Backend (Python)
- Follow **PEP 8** standards
- Use **type hints**
- Write **docstrings**
- Write **unit tests**

### Frontend (TypeScript/React)
- Follow **ESLint** rules
- Use **TypeScript** strict mode
- Write **component** tests
- Use **responsive** design

## 🧪 Testing

### Run All Tests
```bash
npm run test
```

### Backend Tests
```bash
npm run test:backend
```

### Frontend Tests
```bash
npm run test:frontend
```

## 📝 Commit Messages

### Format
```
type(scope): short description

Detailed description (optional)

Closes #issue-number
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples
```bash
feat(chat): Added Turkish book recommendations

fix(api): Fixed Open Library API timeout issue

docs(readme): Updated installation instructions
```

## 🔍 Pull Request Process

### Checklist
- [ ] Code follows standards
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No conflicts

### Review Process
1. **Automated Tests**: GitHub Actions
2. **Code Review**: By maintainer
3. **Testing**: Manual testing
4. **Merge**: After approval

## 🏗️ Project Structure

```
Luminis_AI_Library_Chatbot/
├── .github/workflows/      # CI/CD
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── backend/           # FastAPI backend
│   ├── frontend/          # React frontend
│   ├── database/          # Database management
│   └── services/          # Shared services
├── tests/                 # Test files
├── scripts/               # Helper scripts
└── docker/                # Docker files
```

## 🎯 Priority Areas

### New Features
- [ ] Expand multi-language support
- [ ] Improve book recommendation algorithm
- [ ] Enhance voice support
- [ ] Improve mobile responsiveness

### Bugs and Improvements
- [ ] Performance optimization
- [ ] Improve error handling
- [ ] Increase test coverage
- [ ] Improve accessibility

## 📖 Resources

- [React Documentation](https://react.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Python PEP 8](https://pep8.org/)

Thank you for your contributions! 🙏