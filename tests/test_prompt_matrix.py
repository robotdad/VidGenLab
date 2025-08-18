"""Tests for veo_lab.prompt_matrix utility functions."""

import itertools
import tempfile
from pathlib import Path

import pytest
import yaml
from jinja2 import Template

from veo_lab.prompt_matrix import load_config


class TestLoadConfig:
    """Test configuration file loading."""

    def test_load_config_valid_yaml(self, temp_dir):
        """Test loading a valid YAML configuration."""
        config_data = {
            "matrix": {
                "subject": ["witch", "monk", "warrior"],
                "style": ["cyberpunk", "medieval", "futuristic"],
                "action": ["casting spells", "meditating", "fighting"],
            },
            "negative": ["blurry", "low quality", "distorted"],
        }

        config_file = temp_dir / "test_config.yml"
        config_file.write_text(yaml.dump(config_data), encoding="utf-8")

        result = load_config(config_file)

        assert result == config_data
        assert "matrix" in result
        assert "negative" in result
        assert len(result["matrix"]["subject"]) == 3
        assert len(result["negative"]) == 3

    def test_load_config_minimal_yaml(self, temp_dir):
        """Test loading minimal YAML configuration."""
        config_data = {"matrix": {"subject": ["test"]}}

        config_file = temp_dir / "minimal_config.yml"
        config_file.write_text(yaml.dump(config_data), encoding="utf-8")

        result = load_config(config_file)

        assert result == config_data
        assert "matrix" in result
        assert result["matrix"]["subject"] == ["test"]

    def test_load_config_empty_file(self, temp_dir):
        """Test loading empty configuration file."""
        config_file = temp_dir / "empty_config.yml"
        config_file.write_text("", encoding="utf-8")

        result = load_config(config_file)

        assert result is None

    def test_load_config_invalid_yaml(self, temp_dir):
        """Test loading invalid YAML raises error."""
        config_file = temp_dir / "invalid_config.yml"
        config_file.write_text("invalid: yaml: content: [unclosed", encoding="utf-8")

        with pytest.raises(yaml.YAMLError):
            load_config(config_file)

    def test_load_config_nonexistent_file(self, temp_dir):
        """Test loading nonexistent file raises error."""
        config_file = temp_dir / "nonexistent.yml"

        with pytest.raises(FileNotFoundError):
            load_config(config_file)

    def test_load_config_encoding_handling(self, temp_dir):
        """Test configuration loading with different encodings."""
        # Test with unicode characters
        config_data = {"matrix": {"subject": ["ñoño", "ükümüs", "café"]}}

        config_file = temp_dir / "unicode_config.yml"
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, allow_unicode=True)

        result = load_config(config_file)

        assert result == config_data
        assert "ñoño" in result["matrix"]["subject"]
        assert "ükümüs" in result["matrix"]["subject"]
        assert "café" in result["matrix"]["subject"]


class TestMatrixLogic:
    """Test matrix expansion logic without CLI dependencies."""

    def test_matrix_combinations(self):
        """Test matrix combination generation logic."""
        # Simulate the core logic from the run function
        matrix_config = {
            "subject": ["witch", "monk"],
            "style": ["cyberpunk", "medieval"],
        }

        # Replicate the combination logic from prompt_matrix.py
        bank = sorted(matrix_config.keys())
        combos = list(itertools.product(*(matrix_config[k] for k in bank)))

        expected_combos = [
            ("cyberpunk", "witch"),
            ("cyberpunk", "monk"),
            ("medieval", "witch"),
            ("medieval", "monk"),
        ]

        assert len(combos) == 4
        assert set(combos) == set(expected_combos)

    def test_matrix_single_dimension(self):
        """Test matrix with single dimension."""
        matrix_config = {"subject": ["witch", "monk", "warrior"]}

        bank = sorted(matrix_config.keys())
        combos = list(itertools.product(*(matrix_config[k] for k in bank)))

        expected_combos = [("witch",), ("monk",), ("warrior",)]

        assert len(combos) == 3
        assert set(combos) == set(expected_combos)

    def test_matrix_empty_dimension(self):
        """Test matrix with empty dimension."""
        matrix_config = {"subject": [], "style": ["cyberpunk"]}

        bank = sorted(matrix_config.keys())
        combos = list(itertools.product(*(matrix_config[k] for k in bank)))

        # Should generate no combinations due to empty subject list
        assert len(combos) == 0

    def test_matrix_three_dimensions(self):
        """Test matrix with three dimensions."""
        matrix_config = {
            "character": ["wizard", "knight"],
            "setting": ["castle", "forest"],
            "time": ["dawn", "midnight"],
        }

        bank = sorted(matrix_config.keys())
        combos = list(itertools.product(*(matrix_config[k] for k in bank)))

        # Should generate 2 * 2 * 2 = 8 combinations
        assert len(combos) == 8

        # Check that we have all expected combinations
        assert ("wizard", "castle", "dawn") in combos
        assert ("knight", "forest", "midnight") in combos


class TestTemplateRendering:
    """Test Jinja2 template rendering logic."""

    def test_simple_template_rendering(self):
        """Test simple template rendering."""
        template_text = "A {{style}} {{subject}} in action"
        template = Template(template_text)

        result = template.render(style="cyberpunk", subject="witch")

        assert result == "A cyberpunk witch in action"

    def test_complex_template_rendering(self):
        """Test complex template with conditional logic."""
        template_text = """A {{character}} {% if time == 'midnight' %}sneaking{% else %}walking{% endif %} through the {{setting}} at {{time}}"""
        template = Template(template_text)

        # Test midnight condition
        midnight_result = template.render(character="wizard", setting="castle", time="midnight")
        assert "sneaking" in midnight_result
        assert midnight_result == "A wizard sneaking through the castle at midnight"

        # Test dawn condition
        dawn_result = template.render(character="knight", setting="forest", time="dawn")
        assert "walking" in dawn_result
        assert dawn_result == "A knight walking through the forest at dawn"

    def test_template_with_missing_variable(self):
        """Test template with undefined variable."""
        template_text = "A {{subject}} with {{undefined_variable}}"
        template = Template(template_text)

        # By default, Jinja2 renders undefined variables as empty strings
        result = template.render(subject="witch")
        assert result == "A witch with "

        # Test with strict undefined behavior
        from jinja2 import StrictUndefined
        from jinja2 import UndefinedError

        strict_template = Template(template_text, undefined=StrictUndefined)
        with pytest.raises(UndefinedError):
            strict_template.render(subject="witch")

    def test_template_whitespace_handling(self):
        """Test template whitespace handling."""
        template_text = "   \n  A {{test}} with special chars: !@#$%^&*()  \n   "
        template = Template(template_text)

        result = template.render(test="value")

        # Template should preserve whitespace
        expected = "   \n  A value with special chars: !@#$%^&*()  \n   "
        assert result == expected

        # But when stripped (as done in the actual code), should be clean
        assert result.strip() == "A value with special chars: !@#$%^&*()"


class TestNegativePrompts:
    """Test negative prompt handling logic."""

    def test_negative_prompt_defaults(self):
        """Test default negative prompt behavior."""
        config = {"matrix": {"subject": ["witch"]}}

        # Simulate the default negative handling from run function
        negatives = config.get("negative", [""])

        assert negatives == [""]
        assert len(negatives) == 1

    def test_multiple_negative_prompts(self):
        """Test multiple negative prompts."""
        config = {
            "matrix": {"subject": ["witch"]},
            "negative": ["blurry", "low quality", "distorted"],
        }

        negatives = config.get("negative", [""])

        assert negatives == ["blurry", "low quality", "distorted"]
        assert len(negatives) == 3

    def test_empty_negative_prompts(self):
        """Test empty negative prompts array."""
        config = {"matrix": {"subject": ["witch"]}, "negative": []}

        negatives = config.get("negative", [""])

        assert negatives == []
        assert len(negatives) == 0


class TestConfigValidation:
    """Test configuration validation and edge cases."""

    def test_config_missing_matrix(self):
        """Test configuration without matrix key."""
        config = {"negative": ["blurry"]}

        # Simulate the matrix handling from run function
        matrix_dims = config.get("matrix", {})

        assert matrix_dims == {}
        assert len(matrix_dims) == 0

    def test_config_with_nested_structure(self):
        """Test configuration with complex nested structure."""
        config_data = {
            "matrix": {
                "character": {
                    "type": "array",
                    "values": ["witch", "monk"],  # This would fail in real usage
                }
            },
            "settings": {"output_format": "json", "max_combinations": 100},
        }

        config_file = Path(tempfile.mktemp(suffix=".yml"))
        try:
            config_file.write_text(yaml.dump(config_data), encoding="utf-8")
            result = load_config(config_file)

            assert result == config_data
            assert "settings" in result
            assert result["settings"]["output_format"] == "json"
        finally:
            if config_file.exists():
                config_file.unlink()

    def test_config_with_special_characters(self):
        """Test configuration with special characters in values."""
        config_data = {
            "matrix": {
                "prompt_style": ['test/\\:*?"<>|prompt!', "normal-prompt", "under_score"],
                "subjects": ["café", "naïve", "résumé"],
            }
        }

        config_file = Path(tempfile.mktemp(suffix=".yml"))
        try:
            config_file.write_text(yaml.dump(config_data), encoding="utf-8")
            result = load_config(config_file)

            assert result == config_data
            assert 'test/\\:*?"<>|prompt!' in result["matrix"]["prompt_style"]
            assert "café" in result["matrix"]["subjects"]
        finally:
            if config_file.exists():
                config_file.unlink()
