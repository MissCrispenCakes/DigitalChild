# Contributing to DigitalChild

Thank you for your interest in contributing to GRIMdata / LittleRainbowRights!

This project analyzes human rights documents focusing on child and LGBTQ+ digital protection. We welcome contributions from researchers, developers, and human rights advocates.

## 🎓 About This Project

**Maintainer:** PhD Student (part-time, side project)
**Focus:** Human rights data analysis, child/LGBTQ+ digital rights
**Status:** Active development, research phase

**Please note:** This is maintained by one person alongside PhD work, so response times may vary. Your patience is appreciated!

## 🤝 How to Contribute

### Ways to Contribute

1. **Report Issues** - Found a bug? Let us know!
2. **Suggest Features** - Ideas for improvements welcome
3. **Add Scrapers** - New data sources needed
4. **Improve Documentation** - Help make docs clearer
5. **Add Tests** - More test coverage always helps
6. **Share Research** - Using this in your work? Let us know!

### Not Sure Where to Start?

Check issues labeled:
- `good first issue` - Great for new contributors
- `help wanted` - Maintainer needs assistance
- `documentation` - Help improve docs

## 🐛 Reporting Bugs

**Before reporting:**
1. Check [existing issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
2. Review [First Run Errors](docs/guides/FIRST_RUN_ERRORS.md)
3. Try with latest `basecamp` branch

**When reporting, include:**
- Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (full traceback)
- Relevant log files (from `logs/`)

## 💡 Suggesting Features

We're particularly interested in:
- New data sources (human rights organizations, treaty bodies)
- Additional analysis methods
- Visualization improvements
- Accessibility enhancements

**Feature request template:**
```markdown
**Problem:** What problem does this solve?
**Proposed Solution:** How would it work?
**Alternatives:** Other approaches considered?
**Impact:** Who benefits? How many users?
```

## 🔧 Development Process

### Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/DigitalChild.git
cd DigitalChild

# 2. Create virtual environment
python3 -m venv .LittleRainbow
source .LittleRainbow/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install pre-commit hooks
pip install pre-commit
pre-commit install

# 5. Run tests
pytest tests/ -v
```

### Making Changes

1. **Create a branch** from `basecamp`:
   ```bash
   git checkout -b feature/your-feature-name basecamp
   ```

2. **Make your changes:**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation

3. **Test thoroughly:**
   ```bash
   # Run tests
   pytest tests/ -v

   # Run pre-commit checks
   pre-commit run --all-files

   # Test manually if needed
   python pipeline_runner.py --source au_policy
   ```

4. **Commit with clear messages:**
   ```bash
   git add .
   git commit -m "Add feature: brief description

   - Detailed point 1
   - Detailed point 2

   Fixes #123"
   ```

5. **Push and create Pull Request:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Guidelines

**Title:** Clear, concise description (50 chars or less)

**Description should include:**
- What problem this solves
- How you tested it
- Screenshots (if UI changes)
- Documentation updates
- Related issues (use `Fixes #123`)

**Before submitting:**
- ✅ All tests pass (`pytest tests/ -v`)
- ✅ Pre-commit checks pass (`pre-commit run --all-files`)
- ✅ Documentation updated (if needed)
- ✅ No merge conflicts with `basecamp`

**Review process:**
- Maintainer reviews within 1-2 weeks (remember: part-time!)
- Address feedback if requested
- Once approved, maintainer merges

## 📝 Code Style

### Python Code

- **Style:** Follow PEP 8 (enforced by `black` and `flake8`)
- **Line length:** 88 characters (black default)
- **Imports:** Sorted with `isort --profile black`
- **Type hints:** Encouraged but not required
- **Docstrings:** Use for public functions

**Example:**
```python
def scrape(base_url: str = None, countries: list = None) -> list:
    """
    Download documents from source.

    Args:
        base_url: Base URL for scraping (optional)
        countries: List of countries to filter (optional)

    Returns:
        List of downloaded file paths
    """
    # Implementation
    pass
```

### Documentation

- **Markdown:** Use standard markdown, checked by `mdformat`
- **Links:** Relative links for internal docs
- **Examples:** Include code examples where helpful
- **Clarity:** Write for international audience

### Commit Messages

**Format:**
```
Brief summary (50 chars or less)

- Detailed explanation of what changed
- Why it changed
- Any relevant context

Fixes #issue_number (if applicable)
```

**Good examples:**
```
Add UNICEF scraper for child rights reports

- Implements scrape() function following scraper standards
- Handles pagination and PDF downloads
- Adds tests for new scraper
- Documents usage in RUNBOOK.md

Fixes #42
```

## 🧪 Testing

### Writing Tests

- Place tests in `tests/`
- Use `pytest` framework
- Name test files `test_*.py`
- Name test functions `test_*`

**Example:**
```python
def test_scraper_returns_list():
    """Test that scraper returns a list of file paths."""
    from scrapers.au_policy import scrape
    result = scrape()
    assert isinstance(result, list)
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_validators.py -v

# With coverage
pytest tests/ --cov=processors --cov=scrapers
```

## 📚 Adding Documentation

**When to update docs:**
- New features added
- API changes
- Configuration changes
- New scrapers/processors

**Where to add docs:**
- `README.md` - Brief overview
- `docs/` - Detailed documentation
- `CLAUDE.md` - AI assistant context
- Inline code comments - Complex logic

## 🔒 Security

Found a security vulnerability? **Do NOT open a public issue.**

Instead:
1. Email: [Create SECURITY.md with contact email]
2. Include: Description, impact, steps to reproduce
3. We'll respond within 48 hours

See [SECURITY.md](SECURITY.md) for details.

## 📄 Licensing

By contributing, you agree:
- Code contributions → MIT License
- Data/docs contributions → CC BY 4.0
- You have rights to contribute this work
- You understand contributions may be used in academic research

See [LICENSE](LICENSE) and [LICENSE-DATA](LICENSE-DATA) for details.

## 🌍 Code of Conduct

### Our Pledge

We are committed to providing a welcoming, inclusive environment for all contributors regardless of:
- Age, body size, disability
- Ethnicity, sex characteristics, gender identity/expression
- Level of experience, education
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behavior:**
- Using welcoming, inclusive language
- Respecting different viewpoints
- Accepting constructive criticism gracefully
- Focusing on what's best for the community
- Showing empathy toward others

**Unacceptable behavior:**
- Harassment, trolling, insults
- Publishing private information
- Sexual language or advances
- Any conduct inappropriate in a professional setting

### Enforcement

Report violations to [maintainer email]. All reports reviewed and responded to appropriately.

## 🙋 Questions?

- **Documentation:** Check [docs/](docs/)
- **FAQs:** See [docs/FAQ.md](docs/FAQ.md)
- **Issues:** Search [existing issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Discussion:** Open a [discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions)

## 🎉 Recognition

Contributors are acknowledged in:
- GitHub contributors list
- CITATION.cff file (for academic citations)
- Project documentation

Thank you for contributing to human rights research! 🌈

---

**Last updated:** January 2026
