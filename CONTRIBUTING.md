# Contributing to Synthetic Plastic Transformer

Thank you for your interest in contributing to the Synthetic Plastic Transformer project! We welcome contributions from the community to help advance sustainable materials discovery.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature or bugfix

```bash
git clone https://github.com/yourusername/synthetic-plastic-transformer.git
cd synthetic-plastic-transformer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Development Workflow

1. **Create a branch**: `git checkout -b feature/your-feature-name`
2. **Make changes**: Follow the coding standards below
3. **Add tests**: Ensure new code is covered by tests
4. **Run tests**: `pytest tests/`
5. **Commit changes**: Use descriptive commit messages
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**: Describe your changes clearly

## Coding Standards

### Code Style
- Follow PEP 8 for Python code style
- Use Black for code formatting: `black src/ tests/`
- Maximum line length: 100 characters
- Use type hints for function parameters and return values

### File Organization
- Keep files under 200 lines as specified in project requirements
- Create multiple files instead of making existing ones longer
- Use descriptive module and function names

### Documentation
- Include docstrings for all public functions and classes
- Use Google-style docstrings
- Update README.md if adding new features
- Add examples for new functionality

### Testing
- Write unit tests for all new functions
- Aim for >90% test coverage
- Use pytest for testing framework
- Test edge cases and error conditions

## Areas for Contribution

### High Priority
- **New Fiber Properties**: Add more natural fibers to the database
- **Processing Methods**: Implement new GOTS-compliant processing techniques
- **Property Prediction**: Improve ML model accuracy
- **Performance Optimization**: Speed up training and inference

### Medium Priority
- **Visualization Tools**: Create plots for property comparisons
- **API Improvements**: Enhance the REST API interface
- **Documentation**: Improve tutorials and examples
- **Integration Tests**: Add end-to-end testing

### Research Areas
- **Quantum Descriptors**: Implement new quantum mechanical features
- **Graph Neural Networks**: Experiment with new GNN architectures
- **Transfer Learning**: Improve protein folding knowledge transfer
- **Multi-Objective Optimization**: Better Pareto frontier exploration

## Scientific Contributions

### Data Contributions
- Verified experimental data for natural fiber properties
- New processing method validation data
- GOTS certification verification

### Model Improvements
- Novel neural network architectures
- Better quantum descriptor calculations
- Improved transfer learning strategies

### Sustainability Focus
- Life cycle assessment integration
- Carbon footprint calculations
- Water usage optimization

## Submission Guidelines

### Pull Request Requirements
- Clear description of changes
- Reference to related issues
- Tests passing
- Documentation updated
- Code reviewed by maintainers

### Commit Message Format
```
type(scope): brief description

Longer description if needed

Fixes #issue_number
```

Types: feat, fix, docs, test, refactor, style, perf

### Code Review Process
1. Automated tests must pass
2. At least one maintainer review required
3. All feedback addressed before merge
4. Squash commits when merging

## Community Guidelines

### Be Respectful
- Use inclusive language
- Be constructive in feedback
- Help newcomers learn
- Follow the code of conduct

### Focus on Science
- Validate claims with literature
- Provide experimental evidence
- Consider environmental impact
- Prioritize GOTS compliance

## Getting Help

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact maintainers for sensitive issues
- **Documentation**: Check the docs/ folder for detailed guides

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes
- Research publications (for significant contributions)
- Conference presentations

Thank you for helping make sustainable materials discovery more accessible! 