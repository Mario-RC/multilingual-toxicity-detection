# Contributing

Keep the package lightweight and predictable:

- Do not import optional ML frameworks at module import time.
- Keep local-rule changes covered by focused tests.
- Store large model artifacts outside the repository.
- Run formatting, linting, and tests before opening a pull request.

Recommended checks:

```bash
python -m pip install -e ".[dev]"
ruff check .
python -m unittest discover -s tests
```

