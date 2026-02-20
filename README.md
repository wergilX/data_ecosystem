# python_practice

### 1. Dependency setup
Run console command to download and setup all dependencies from pyproject.toml:
`uv sync`

### 2. Run script
To run scripts with all project dependencies, use the uv run command:
`uv run src/main.py`

### 3. Code quality
Check your code for errors, style, and type consistency:
- Linter (Errors & Style):
`uv run ruff check .`
- Type Checker (Static Analysis):
`uv run ty .`
- Formatter (Auto-fix style):
`uv run ruff format .`
