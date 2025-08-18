# Testing Philosophy & Guidelines

This document outlines our testing philosophy and provides guidelines for maintaining and expanding the test suite for the VidGenLab project.

## Core Philosophy

### 🎯 **Primary Principle: No API Quota Consumption**

**The cardinal rule**: Tests must NEVER consume generative AI API quota or incur costs.

This means:
- ✅ **Test utility functions, logic, and data transformations**
- ✅ **Mock all external API calls extensively**
- ✅ **Validate behavior through mocks and pure functions**
- ❌ **Never call actual image/video generation APIs**
- ❌ **Never test CLI commands that trigger real API calls**

### 🏗️ **Testing Strategy Alignment**

Our testing follows the **60% unit, 30% integration, 10% end-to-end** pyramid from the implementation philosophy:

- **Unit Tests (60%)**: Pure utility functions, data transformations, path operations
- **Integration Tests (30%)**: Mock-based workflow tests, CLI argument parsing
- **End-to-End Tests (10%)**: Complete workflows with all external dependencies mocked

## What We Test vs. What We Don't

### ✅ **HIGH VALUE - Always Test These:**

1. **Pure Utility Functions**
   ```python
   # Examples from our codebase:
   - create_prompt_snippet()
   - create_session_directory() 
   - create_output_path()
   - stable_stem()
   - load_config()
   ```

2. **Data Transformations & Logic**
   ```python
   # Examples:
   - Matrix combination generation (itertools.product)
   - Template rendering (Jinja2)
   - Path sanitization and filename creation
   - Metadata generation
   ```

3. **File Operations (with temp directories)**
   ```python
   # Examples:
   - YAML/JSON parsing
   - Configuration loading
   - File path management
   - Output structure creation
   ```

4. **CLI Argument Parsing**
   ```python
   # Test CLI interfaces without triggering API calls:
   - Help text generation
   - Argument validation
   - Error handling for missing files
   ```

5. **Dry-Run CLI Testing (Preferred)**
   ```python
   # Test CLI interfaces using dry-run flags:
   - imagen_lab generate --dry (tests parsing + path creation)
   - CLI argument validation without API costs
   - Environment variable precedence testing
   ```

6. **Mock-Based Integration Tests (When Dry-Run Unavailable)**
   ```python
   # Complete workflows with mocked APIs:
   - Video generation workflows (mocked)
   - Image analysis workflows (mocked)
   - Multi-step processes (mocked)
   ```

### ❌ **LOW VALUE - Don't Test These:**

1. **Direct API Integration**
   ```python
   # Skip testing actual calls to:
   - Google Gemini API (image/video generation)
   - Any generative AI endpoints
   - External services with usage costs
   ```

2. **CLI Commands Without Dry-Run Support**
   ```python
   # Skip end-to-end testing of commands that lack --dry flags:
   - veo_lab simple (generates videos, no dry-run yet)
   - Most veo_lab scripts (pending dry-run implementation)
   
   # ✅ USE dry-run for testing these:
   - imagen_lab generate --dry (safe CLI testing)
   - prompt_matrix run --dry (when available)
   ```

3. **Library Implementation Details**
   ```python
   # Don't test how external libraries work:
   - How typer parses commands (trust the library)
   - How pathlib creates paths (trust the stdlib)
   - How yaml parses files (trust the library)
   ```

## Test Organization

### 📁 **File Structure**
```
tests/
├── README.md                    # This file
├── conftest.py                 # Shared fixtures and configuration
├── test_cli_parsing.py         # CLI argument parsing and validation
├── test_imagen_lab_common.py   # Imagen lab utility functions
├── test_integration_mocks.py   # Mock-based integration tests
├── test_prompt_matrix.py       # Prompt matrix utility logic
└── test_veo_lab_common.py      # Veo lab utility functions
```

### 🧪 **Test Categories**

#### **Unit Tests**
- **Focus**: Single functions, pure logic
- **Mocking**: Minimal - only for external dependencies
- **Examples**: Path creation, string manipulation, data validation

#### **Integration Tests**  
- **Focus**: Multiple components working together
- **Mocking**: Extensive - all external APIs and services
- **Examples**: Complete video generation workflow (mocked)

#### **CLI Tests**
- **Focus**: Command-line interfaces and argument parsing
- **Mocking**: All API clients and file operations
- **Examples**: Help text, validation, error handling

## Testing Patterns & Best Practices

### 🎭 **Effective Mocking Patterns**

#### **Mock API Clients**
```python
@patch("veo_lab.common.create_client")
def test_video_generation_workflow(mock_create_client, temp_dir):
    # Create mock client and responses
    mock_client = Mock()
    mock_create_client.return_value = mock_client
    
    # Mock the API response
    mock_operation = Mock()
    mock_operation.name = "test_operation_id"
    mock_client.models.generate_videos.return_value = mock_operation
    
    # Test the workflow logic
    result = generate_video(mock_client, "test prompt", session_dir=temp_dir)
    
    # Verify behavior, not implementation
    assert result.prompt == "test prompt"
    assert result.path.exists()
```

#### **Mock File Operations**
```python
@patch("builtins.open")
def test_image_analysis(mock_open):
    # Mock file reading to return actual bytes
    mock_file = Mock()
    mock_file.read.return_value = b"fake_image_data"
    mock_open.return_value.__enter__.return_value = mock_file
    
    # Test the analysis logic
    result = analyze_image("fake_path.jpg")
    
    # Verify the expected behavior
    assert result.contains_expected_content
```

### 🏗️ **Test Structure Guidelines**

#### **Use Clear Test Classes**
```python
class TestOutputPathCreation:
    """Test output path creation logic."""
    
    def test_default_path_creation(self, temp_dir):
        """Test default output path creation."""
        # Arrange
        script_name = "test_script"
        prompt = "cyberpunk witch casting spells"
        
        # Act  
        result = create_output_path(script_name, prompt)
        
        # Assert
        assert "test_script" in result.name
        assert "cyberpunk_witch_casting" in result.name
```

#### **Test Edge Cases**
```python
def test_special_characters_in_prompt(self):
    """Test prompt with filesystem-unsafe characters."""
    dangerous_prompt = 'test/\\:*?"<>|prompt!'
    result = create_prompt_snippet(dangerous_prompt)
    
    # Should sanitize dangerous characters
    dangerous_chars = '/\\:*?"<>|'
    for char in dangerous_chars:
        assert char not in result
```

#### **Use Fixtures for Shared Setup**
```python
# In conftest.py
@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture  
def sample_config():
    """Sample configuration for testing."""
    return {
        "matrix": {"subject": ["witch", "monk"]},
        "negative": ["blurry", "low quality"]
    }
```

## Coverage Guidelines

### 🎯 **Target Coverage by Module Type**

- **Core Utilities**: 80-95% (imagen_lab/common.py: 98%, veo_lab/common.py: 74%)
- **CLI Interfaces**: 80-90% (imagen_lab/cli.py: 88%)  
- **Integration Workflows**: 70-85% (character_pack.py: 73%)
- **Pure Logic Functions**: 90%+ (prompt_matrix utilities: 100% of testable code)

### ⚪ **Acceptable Low Coverage Areas**

- **Standalone CLI scripts**: 0-10% (ab_viewer.py, simple.py, etc.)
- **API integration points**: Lines that directly call external APIs
- **Error handling for external failures**: Network timeouts, API rate limits

### 📊 **Coverage Philosophy**

Rather than chasing specific coverage percentages, focus on **meaningful coverage** of testable logic:

```bash
# Check current coverage
uv run pytest --cov=src --cov-report=term-missing

# Focus areas for coverage improvement:
# 1. Core utility functions (should be 90%+)
# 2. CLI argument parsing and validation (should be 80%+)  
# 3. Data transformation logic (should be 90%+)
```

**Expected Coverage Patterns:**
- ✅ **Core Utilities**: 90-98% (imagen_lab/common.py, key veo_lab functions)
- ✅ **CLI Interfaces**: 80-90% (use dry-run for testing, avoid API calls)
- ✅ **Pure Logic**: 90%+ (prompt_matrix, path utilities, data validation)
- ⚪ **API-Dependent Scripts**: 0-10% (simple.py, storyboard.py, etc. - by design)

**Coverage Anti-Patterns to Avoid:**
- Don't test external library implementations (pathlib, yaml, typer internals)
- Don't chase coverage of error handling for external API failures
- Don't test CLI scripts that make actual API calls

## Writing New Tests

### 🚀 **Before Adding Tests**

1. **Ask**: "Does this test require API calls?"
   - If YES: Don't test directly, create mocks instead
   - If NO: Proceed with standard testing

2. **Ask**: "Does this test validate core logic?"  
   - If YES: High priority, add comprehensive tests
   - If NO: Consider if the test adds meaningful value

3. **Ask**: "Can this be tested with pure functions?"
   - If YES: Preferred approach, test the logic directly
   - If NO: Use mocks to isolate the testable parts

### ✍️ **Test Writing Checklist**

- [ ] **No API calls**: Verify no real external service calls
- [ ] **Prefer dry-run**: Use `--dry` flags for CLI testing when available
- [ ] **Clear test names**: Describe what behavior is being tested
- [ ] **Arrange-Act-Assert**: Structure tests clearly
- [ ] **Edge cases**: Include boundary conditions and error cases
- [ ] **Minimal mocking**: Mock only when dry-run isn't available
- [ ] **Temp directories**: Use fixtures for file operations
- [ ] **Fast execution**: Tests should run in milliseconds, not seconds

### 🧪 **Common Test Patterns**

#### **Testing File Operations**
```python
def test_config_loading(self, temp_dir):
    """Test configuration file loading."""
    config_data = {"matrix": {"subject": ["test"]}}
    config_file = temp_dir / "test_config.yml" 
    config_file.write_text(yaml.dump(config_data))
    
    result = load_config(config_file)
    
    assert result == config_data
```

#### **Testing Error Conditions**
```python
def test_invalid_config_raises_error(self, temp_dir):
    """Test that invalid YAML raises appropriate error."""
    config_file = temp_dir / "invalid.yml"
    config_file.write_text("invalid: yaml: [unclosed")
    
    with pytest.raises(yaml.YAMLError):
        load_config(config_file)
```

#### **Testing CLI Interfaces with Dry-Run (Preferred)**
```python
def test_generate_command_dry_run(self):
    """Test generate command parsing and validation with dry-run."""
    runner = CliRunner()
    result = runner.invoke(imagen_app, [
        "generate", "cyberpunk scene", 
        "--model", "custom-model",
        "--dry"  # Key: no API calls, tests real parsing logic
    ])
    
    assert result.exit_code == 0
    assert "Model: custom-model" in result.output
    assert "✅ Dry run complete - no API calls made" in result.output

def test_cli_help_output(self):
    """Test CLI help text generation."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "Generate an image" in result.output
```

## Running Tests

### 🏃 **Essential Commands**
```bash
# Run all tests
make test

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_prompt_matrix.py -v

# Run specific test
uv run pytest tests/test_prompt_matrix.py::TestLoadConfig::test_load_config_valid_yaml -v
```

### 🔍 **Debugging Failed Tests**
```bash
# Run with verbose output and no capture
uv run pytest tests/test_failing.py -v -s

# Run with debugger on failure
uv run pytest tests/test_failing.py --pdb

# Run only failed tests from last run
uv run pytest --lf
```

## Principles for Future Development

### 🎯 **When Adding New Features**

1. **Write tests FIRST** for pure utility functions
2. **Mock extensively** for integration points  
3. **Prioritize testable design**: Separate pure logic from API calls
4. **Follow the existing patterns**: Look at similar tests for guidance

### 🔄 **When Refactoring**

1. **Preserve test behavior**: Tests should pass before and after
2. **Update mocks if interfaces change**: Keep mocks aligned with reality
3. **Add tests for new edge cases**: Refactoring often reveals new scenarios
4. **Verify coverage doesn't decrease**: Maintain or improve coverage

### 🚀 **Continuous Improvement**

- **Review tests quarterly**: Remove outdated tests, add missing coverage
- **Update mocks when APIs change**: Keep mocks realistic and current  
- **Share testing patterns**: Document new patterns for team consistency
- **Measure test value**: Focus effort on high-impact, frequently-used code

---

## Summary

Our testing philosophy prioritizes **maximum confidence with zero API costs**. We achieve this through:

- ✅ **Comprehensive testing** of pure utility functions and logic
- ✅ **Dry-run CLI testing** to validate argument parsing and workflows without API calls
- ✅ **Selective mocking** only when dry-run capabilities aren't available
- ✅ **Strategic coverage** focused on high-value, testable code
- ✅ **Clear boundaries** between what we test and what we trust

This approach ensures our codebase remains reliable and maintainable while respecting the cost constraints of generative AI services. The decision hierarchy: **1) Dry-run testing, 2) Pure function testing, 3) Mock the API as last resort**.