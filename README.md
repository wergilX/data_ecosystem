# Data Ecosystemm: Generator & Ingestor
​This project simulates a professional data engineering lifecycle, focusing on the transition from complex, legacy-style nested JSON to clean, validated, and flattened data ready for AI and Vector Database pipelines.

### 1. The Data Generator (Producer)
​A sophisticated synthetic data engine built on strict Object-Oriented principles.
* Architecture: Uses abc (Abstract Base Classes) to enforce a strict contract for vehicle generation​
* Complexity: Generates deeply nested structures (metadata, technical specs) to simulate real-world data challenges.
* ​Persistence: Utilizes pathlib for robust file I/O and directory management.

### 2. The Data Ingestor (Consumer)
A memory-efficient pipeline designed to transform and validate raw exports.
* Flattening: Converts nested technical specs into flat key-value pairs for optional Vector DB filtering.

### 3. Dependency setup
Run console command to download and setup all dependencies from pyproject.toml:
`uv sync`

### 4. Run scripts
To run scripts with all project dependencies, use the uv run command:
* Data Generator `uv run -m src.data_generator.main`
* Data Ingestor `uv run -m src.data_ingestor.main`

### 5. Code quality
Check your code for errors, style, and type consistency:
- Linter (Errors & Style):
`uv run ruff check .`
- Type Checker (Static Analysis):
`uv run ty .`
- Formatter (Auto-fix style):
`uv run ruff format .`
