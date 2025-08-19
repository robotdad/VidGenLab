"""Tests for imagen_lab.common utility functions."""

import json
from unittest.mock import Mock

import pytest

from imagen_lab.common import create_output_path
from imagen_lab.common import save_generated_image
from imagen_lab.common import save_metadata
from imagen_lab.common import save_prompt_file


class TestOutputPathCreation:
    """Test output path creation logic."""

    def test_create_output_path_default(self, temp_dir):
        """Test default output path creation."""
        # Test actual function behavior (creates path under project out/)
        result = create_output_path("imagen", "cyberpunk witch casting spells")

        # Should contain script name and prompt snippet
        assert "imagen" in result.name
        assert "cyberpunk_witch_casting" in result.name

        # Should be timestamped
        assert result.parent.name.count("-") == 2  # YYYY-MM-DD format
        assert "out" in result.parts

    def test_create_output_path_custom_output_dir(self, temp_dir):
        """Test with custom output directory."""
        custom_dir = temp_dir / "custom_output"
        result = create_output_path("imagen", "test prompt", output_dir=custom_dir)
        assert result == custom_dir

    def test_create_output_path_custom_name(self, temp_dir):
        """Test with custom name."""
        result = create_output_path("imagen", "test prompt", custom_name="my_custom_name")
        assert "my_custom_name" in result.name
        assert "imagen" in result.name

    def test_create_output_path_long_prompt(self, temp_dir):
        """Test path creation with very long prompt."""
        long_prompt = "word " * 50  # Very long prompt
        result = create_output_path("imagen", long_prompt)

        # Should be truncated to reasonable length
        assert len(result.name) < 200  # Reasonable folder name length


class TestFileOperations:
    """Test file saving operations."""

    def test_save_prompt_file(self, temp_dir):
        """Test prompt file saving."""
        test_prompt = "A cyberpunk scene with neon lights"
        save_prompt_file(temp_dir, test_prompt)

        prompt_file = temp_dir / "prompt.txt"
        assert prompt_file.exists()
        assert prompt_file.read_text() == test_prompt

    def test_save_metadata(self, temp_dir):
        """Test metadata file saving."""
        save_metadata(
            temp_dir,
            prompt="test prompt",
            script_name="imagen",
            model="imagen-3.0-generate-001",
            custom_field="custom_value",
        )

        metadata_file = temp_dir / "metadata.json"
        assert metadata_file.exists()

        metadata = json.loads(metadata_file.read_text())
        assert metadata["prompt"] == "test prompt"
        assert metadata["script"] == "imagen"
        assert metadata["model"] == "imagen-3.0-generate-001"
        assert metadata["custom_field"] == "custom_value"
        assert "timestamp" in metadata
        assert "output_path" in metadata

    def test_save_generated_image_success(self, temp_dir):
        """Test successful image saving."""
        # Mock response with generated image
        mock_image = Mock()
        mock_image.image_bytes = b"fake_image_data"

        mock_generated_image = Mock()
        mock_generated_image.image = mock_image

        mock_response = Mock()
        mock_response.generated_images = [mock_generated_image]

        # Save the image
        result_path = save_generated_image(mock_response, temp_dir, "test_image.jpg")

        # Verify file was created
        expected_path = temp_dir / "test_image.jpg"
        assert result_path == expected_path
        assert expected_path.exists()
        assert expected_path.read_bytes() == b"fake_image_data"

    def test_save_generated_image_no_images(self, temp_dir):
        """Test error when no images in response."""
        # Mock response with no generated images
        mock_response = Mock()
        mock_response.generated_images = None

        with pytest.raises(ValueError, match="No generated images in response"):
            save_generated_image(mock_response, temp_dir)

    def test_save_generated_image_empty_images(self, temp_dir):
        """Test error when generated images list is empty."""
        mock_response = Mock()
        mock_response.generated_images = []

        with pytest.raises(ValueError, match="No generated images in response"):
            save_generated_image(mock_response, temp_dir)


class TestUtilityEdgeCases:
    """Test edge cases and error conditions."""

    def test_create_output_path_special_characters(self, temp_dir):
        """Test path creation with special characters in prompt."""
        prompt_with_special = 'test/\\:*?"<>|prompt!'
        result = create_output_path("imagen", prompt_with_special)

        # Should sanitize special characters
        dangerous_chars = '/\\:*?"<>|'
        for char in dangerous_chars:
            assert char not in result.name

    def test_save_metadata_with_path_object(self, temp_dir):
        """Test metadata saving with Path object."""
        save_metadata(temp_dir, prompt="test", script_name="imagen", model="test-model")

        metadata_file = temp_dir / "metadata.json"
        metadata = json.loads(metadata_file.read_text())

        # output_path should be converted to string
        assert isinstance(metadata["output_path"], str)
        assert str(temp_dir) in metadata["output_path"]


class TestModelManagement:
    """Test model listing and environment variable handling."""

    def test_list_models(self):
        """Test model listing functionality."""
        from imagen_lab.common import list_models

        result = list_models()

        # Should return dict with known models and default
        assert "known" in result
        assert "default" in result
        assert isinstance(result["known"], list)
        assert len(result["known"]) > 0

        # Known models should include expected values
        known_models = result["known"]
        assert "imagen-3.0-generate-002" in known_models
        assert "imagen-3.0-fast-generate-001" in known_models

        # Default should be reasonable
        assert result["default"] in known_models or result["default"] == "imagen-3.0-generate-002"

    def test_list_models_with_env_var(self):
        """Test model listing with custom env var."""
        from unittest.mock import patch

        from imagen_lab.common import list_models

        with patch.dict("os.environ", {"IMAGEN_MODEL": "imagen-3.0-fast-generate-001"}):
            result = list_models()
            assert result["default"] == "imagen-3.0-fast-generate-001"
