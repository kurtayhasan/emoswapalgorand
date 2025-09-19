# Contributing to EmoSwap

Thank you for your interest in contributing to EmoSwap! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/emoswapalgo.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Commit your changes: `git commit -m 'Add some amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### Setup

1. **Backend Setup**:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Frontend Setup**:
```bash
cd web
npm install
```

3. **Environment Setup**:
```bash
cp env.example .env
# Edit .env with your configuration
```

## Code Style

### Python (Smart Contracts)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write comprehensive docstrings
- Keep functions focused and small

### TypeScript/React (Frontend)

- Use ESLint configuration provided
- Follow React best practices
- Use TypeScript strict mode
- Write meaningful component names

## Testing

### Smart Contract Tests

```bash
python -m unittest tests/test_compile_contracts.py
```

### Frontend Tests

```bash
cd web
npm test
```

## Pull Request Guidelines

1. **Clear Description**: Provide a clear description of what your PR does
2. **Tests**: Include tests for new functionality
3. **Documentation**: Update documentation if needed
4. **Breaking Changes**: Clearly mark any breaking changes
5. **Screenshots**: Include screenshots for UI changes

## Issue Guidelines

### Bug Reports

When reporting bugs, please include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Feature Requests

When requesting features, please include:

- Clear description of the feature
- Use case and motivation
- Proposed implementation (if you have ideas)
- Any additional context

## Smart Contract Development

### Adding New Contracts

1. Create contract file in `contracts/` directory
2. Follow existing patterns and structure
3. Add comprehensive tests
4. Update deployment scripts if needed
5. Update documentation

### Contract Guidelines

- Use clear, descriptive names
- Include proper error handling
- Add comprehensive comments
- Follow Algorand best practices
- Test thoroughly on Testnet

## Frontend Development

### Adding New Components

1. Create component file in `web/src/components/`
2. Follow existing patterns
3. Add TypeScript types
4. Include tests
5. Update documentation

### Component Guidelines

- Use functional components with hooks
- Follow React best practices
- Make components reusable
- Add proper error handling
- Include loading states

## Documentation

### Updating Documentation

- Keep README.md up to date
- Update DEPLOYMENT.md for deployment changes
- Add inline code comments
- Update API documentation if applicable

## Security

### Security Guidelines

- Never commit private keys or mnemonics
- Use environment variables for sensitive data
- Follow Algorand security best practices
- Report security issues privately

## Community

### Getting Help

- Check existing issues and discussions
- Join the Algorand Discord
- Ask questions in GitHub Discussions
- Review the documentation

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the project's values

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Deploy to Testnet
6. Announce the release

## License

By contributing to EmoSwap, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have any questions about contributing, please:

- Open an issue
- Start a discussion
- Contact the maintainers

Thank you for contributing to EmoSwap! 🎭
