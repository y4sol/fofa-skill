# Contributing to FOFA Skill

## Development Workflow

### 1. Local Development

```bash
# Clone the repository
git clone https://github.com/y4sol/fofa-skill.git
cd fofa-skill

# Run tests before making changes
bash scripts/test_cli.sh
```

### 2. Making Changes

1. Make your changes to the code
2. Run the test script to verify no errors:
   ```bash
   bash scripts/test_cli.sh
   ```

### 3. Testing Checklist

Before pushing to GitHub, verify:

- [ ] `python fofa_query.py --help` works
- [ ] `python fofa_query.py info` works (requires valid credentials)
- [ ] `python fofa_query.py search "test"` works (requires valid credentials)
- [ ] Python imports work without errors
- [ ] All comments are in English
- [ ] README is in English

### 4. Upload Process

```bash
# Test locally first
python scripts/fofa_query.py info

# If all tests pass, upload to GitHub
git add .
git commit -m "Your changes"
git push origin main
```

## Code Style

- Use English for all comments and documentation
- Follow PEP 8 for Python code
- Add docstrings to new functions

## Common Issues

### API Errors

| Error | Solution |
|-------|----------|
| `403 Access Denied` | Check API key permissions |
| `403 Insufficient Points` | stats requires VIP |
| `404 Not Found` | Check API endpoint |

### Test Failures

If `test_cli.sh` fails:
1. Check Python version (3.7+ required)
2. Verify file permissions
3. Check for syntax errors: `python -m py_compile scripts/fofa_query.py`
