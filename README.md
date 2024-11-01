[![Test](https://github.com/accentdesign/accentnotifications/actions/workflows/test.yml/badge.svg)](https://github.com/accentdesign/accentnotifications/actions/workflows/test.yml)

## Commands

### Install dependencies

```bash
uv sync --all-extras
```

### Run tests

```bash
uv run pytest tests
```

### Run linters

ruff:
```bash
uv run ruff format accentnotifications example tests
```
```bash
uv run ruff check --fix accentnotifications example tests
```

### Build package

install dependencies:
```bash
uv tool install hatch
```

build package:
```bash
rm -rf dist && uv build
```

### Publish package

```bash
uv publish --token <token>
```