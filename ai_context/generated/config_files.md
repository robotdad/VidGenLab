# *.toml | *.yml | *.yaml | Makefile | ruff.toml

[collect-files]

**Search:** ['*.toml', '*.yml', '*.yaml', 'Makefile', 'ruff.toml']
**Exclude:** ['uv.lock']
**Include:** []
**Date:** 8/18/2025, 10:40:52 AM
**Files:** 3

=== File: Makefile ===
# Workspace Makefile

# Include the recursive system
repo_root = $(shell git rev-parse --show-toplevel)
include $(repo_root)/tools/makefiles/recursive.mk

# Include Python makefile for this project's source code  
include $(repo_root)/tools/makefiles/python.mk

# Helper function to list discovered projects
define list_projects
	@echo "Projects discovered: $(words $(MAKE_DIRS))"
	@for dir in $(MAKE_DIRS); do echo "  - $$dir"; done
	@echo ""
endef

# Default goal
.DEFAULT_GOAL := help

# Main targets
.PHONY: help workspace-install dev test

help: ## Show this help message
	@echo ""
	@echo "Quick Start:"
	@echo "  make install         Install all dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make check          Format, lint, and type-check all code"
	@echo ""
	@echo "AI Context:"
	@echo "  make ai-context-files Build AI context documentation"
	@echo ""
	@echo "Other:"
	@echo "  make clean          Clean build artifacts"
	@echo ""

# Override install to add workspace setup messaging
install: workspace-install

workspace-install: ## Install all dependencies with workspace messaging
	@echo "Installing workspace dependencies..."
	uv sync --group dev
	@echo ""
	@echo "Dependencies installed!"
	@echo ""
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "✓ Virtual environment already active"; \
	elif [ -f .venv/bin/activate ]; then \
		echo "→ Run this command: source .venv/bin/activate"; \
	else \
		echo "✗ No virtual environment found. Run 'make install' first."; \
	fi

# Code quality and test targets are provided by python.mk

# AI Context
ai-context-files: ## Build AI context files
	@echo "Building AI context files..."
	uv run python tools/build_ai_context_files.py
	uv run python tools/build_git_collector_files.py
	@echo "AI context files generated"

# Workspace info
workspace-info: ## Show workspace information
	@echo ""
	@echo "Workspace"
	@echo "==============="
	@echo ""
	$(call list_projects)
	@echo ""


=== File: pyproject.toml ===
[project]
name = "vidgenlab"
version = "0.1.0"
description = "Exploring generative AI video APIs with modular experiments"
authors = [{ name = "robotdad" }]
requires-python = ">=3.11"
readme = "README.md"
license = { text = "MIT" }
dependencies = [
    "google-genai>=0.3.0",
    "jinja2>=3.1.4",
    "pyyaml>=6.0.2",
    "typer>=0.12.3",
    "tqdm>=4.66.4",
    "pydantic>=2.8.2",
    "rich>=13.7.1",
    "pillow>=10.3.0",
    "streamlit>=1.36.0",
    "python-dotenv>=1.0.1",
]

[tool.setuptools]
packages = ["veo_lab", "imagen_lab"]
package-dir = {"" = "src"}

[project.scripts]
imagen_lab = "imagen_lab.cli:app"

[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[dependency-groups]
dev = [
    "build>=1.2.2.post1",
    "debugpy>=1.8.14",
    "playwright>=1.54.0",
    "pyright>=1.1.403",
    "pytest>=8.3.5",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=6.1.1",
    "pytest-mock>=3.14.0",
    "ruff>=0.11.10",
    "twine>=6.1.0",
]


=== File: ruff.toml ===
# Ruff configuration for the entire project
# This ensures consistent formatting across all Python code

# Use 100 character line length for consistency with veo lab
line-length = 100

# Target Python 3.11+
target-version = "py311"

# Exclude generated and build directories
extend-exclude = [
    ".venv",
    "venv",
    "__pycache__",
    "*.pyc",
    ".web",
    "node_modules",
    "recipe-executor/recipe_executor",  # Generated code
    "cortex-core/cortex_core",  # Generated code
]

[format]
# Use double quotes for strings
quote-style = "double"

# Use 4 spaces for indentation
indent-style = "space"

# Respect magic trailing commas
skip-magic-trailing-comma = false

# Use Unix line endings
line-ending = "auto"

[lint]
# Enable specific rule sets
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings (includes W292 for newline at EOF)
    "F",    # Pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "DTZ",  # flake8-datetimez
    "T10",  # flake8-debugger
    "RET",  # flake8-return
    "SIM",  # flake8-simplify
    "TID",  # flake8-tidy-imports
]

# Ignore specific rules
ignore = [
    "E501",   # Line too long (handled by formatter)
    "E712",   # Comparison to True/False (needed for SQLAlchemy)
    "B008",   # Do not perform function calls in argument defaults
    "B904",   # Within except clause, use raise from (not always needed)
    "UP007",  # Use X | Y for type unions (keep Optional for clarity)
    "SIM108", # Use ternary operator (sometimes if/else is clearer)
    "DTZ005", # datetime.now() without tz (okay for timestamps)
    "N999",   # Invalid module name (web-bff is valid)
    "TID252", # Relative imports from parent (used in package structure)
    "RET504", # Unnecessary assignment before return (sometimes clearer)
]

# Allow unused variables when prefixed with underscore
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[lint.per-file-ignores]
# Ignore import violations in __init__ files
"__init__.py" = ["E402", "F401", "F403"]

# Ignore missing docstrings in tests
"test_*.py" = ["D100", "D101", "D102", "D103", "D104"]
"tests/*" = ["D100", "D101", "D102", "D103", "D104"]

# Allow dynamic imports in recipe files
"recipes/*" = ["F401", "F403"]

[lint.isort]
# Combine as imports
combine-as-imports = true

# Force single line imports
force-single-line = true

# Order imports by type
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[lint.pydocstyle]
# Use Google docstring convention
convention = "google"

