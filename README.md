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

black:
```bash
uv run black accentnotifications example tests
```

ruff:
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
uv build
```

### Publish package

install dependencies:
```bash
uv tool install twine
```

publish package:
```bash
uvx twine upload dist/*
```