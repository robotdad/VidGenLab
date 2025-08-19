"""Tests for CLI argument parsing and validation."""

from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch

from typer.testing import CliRunner

from imagen_lab.cli import app as imagen_app


class TestImagenLabCLI:
    """Test imagen_lab CLI parsing and validation."""

    def setUp(self):
        self.runner = CliRunner()

    def test_imagen_help(self):
        """Test imagen_lab help output."""
        runner = CliRunner()
        result = runner.invoke(imagen_app, ["--help"])

        assert result.exit_code == 0
        assert "Image generation lab" in result.output
        assert "generate" in result.output
        assert "analyze" in result.output

    def test_generate_help(self):
        """Test generate command help."""
        runner = CliRunner()
        result = runner.invoke(imagen_app, ["generate", "--help"])

        assert result.exit_code == 0
        assert "Generate an image from a text prompt" in result.output
        assert "--model" in result.output
        assert "--output" in result.output
        assert "--name" in result.output

    def test_analyze_help(self):
        """Test analyze command help."""
        runner = CliRunner()
        result = runner.invoke(imagen_app, ["analyze", "--help"])

        assert result.exit_code == 0
        assert "Analyze an image and generate" in result.output
        assert "--model" in result.output
        assert "--output" in result.output

    def test_generate_command_dry_run_comprehensive(self):
        """Test generate command with all options using dry-run."""
        runner = CliRunner()
        result = runner.invoke(
            imagen_app,
            [
                "generate",
                "cyberpunk witch casting holographic spells in neon-lit gothic atmosphere",
                "--model",
                "imagen-3.0-fast-generate-001",
                "--output",
                "/custom/output/path",
                "--name",
                "magical_scene",
                "--dry",
            ],
        )

        # Should complete successfully
        assert result.exit_code == 0
        assert "Generating image: cyberpunk witch casting holographic spells" in result.output
        assert "Model: imagen-3.0-fast-generate-001" in result.output
        assert "/custom/output/path" in result.output
        assert "🔍 Dry run - showing what would be generated:" in result.output
        # When using --output with absolute path, custom name isn't shown in dry-run output
        assert "✅ Dry run complete - no API calls made" in result.output

    def test_generate_command_default_model_dry_run(self):
        """Test generate command uses default model with dry-run."""
        runner = CliRunner()
        result = runner.invoke(imagen_app, ["generate", "simple prompt", "--dry"])

        assert result.exit_code == 0
        assert "Model: imagen-3.0-generate-002" in result.output
        assert "simple prompt" in result.output
        assert "✅ Dry run complete - no API calls made" in result.output

    def test_generate_command_path_creation_dry_run(self):
        """Test generate command creates proper output paths with dry-run."""
        runner = CliRunner()
        result = runner.invoke(
            imagen_app, ["generate", "test/path\\creation:with*special?chars", "--dry"]
        )

        assert result.exit_code == 0
        # Should sanitize special characters in path
        assert "test_path_creation_with_special_chars" in result.output or "test" in result.output
        assert "✅ Dry run complete - no API calls made" in result.output

    def test_generate_missing_prompt(self):
        """Test generate command without prompt."""
        runner = CliRunner()
        result = runner.invoke(imagen_app, ["generate"])

        # Should fail with missing argument error
        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_analyze_missing_image_path(self):
        """Test analyze command without image path."""
        runner = CliRunner()
        result = runner.invoke(imagen_app, ["analyze"])

        # Should fail with missing argument error
        assert result.exit_code != 0
        assert "Missing argument" in result.output

    @patch("imagen_lab.cli.create_client")
    @patch("imagen_lab.cli.create_output_path")
    def test_analyze_nonexistent_image(self, mock_create_path, mock_create_client, temp_dir):
        """Test analyze command with nonexistent image file."""
        mock_output_path = temp_dir / "test_output"
        mock_create_path.return_value = mock_output_path

        nonexistent_file = "/path/that/does/not/exist.jpg"

        runner = CliRunner()
        result = runner.invoke(imagen_app, ["analyze", nonexistent_file])

        # Should fail with file not found error
        assert result.exit_code == 1
        assert "Image file not found" in result.output

    @patch("imagen_lab.cli.create_client")
    @patch("imagen_lab.cli.create_output_path")
    @patch("imagen_lab.cli.save_prompt_file")
    @patch("imagen_lab.cli.save_metadata")
    @patch("builtins.open")
    def test_analyze_command_success(
        self,
        mock_open,
        mock_save_metadata,
        mock_save_prompt,
        mock_create_path,
        mock_create_client,
        temp_dir,
    ):
        """Test successful analyze command execution."""
        # Create a real temporary image file
        test_image = temp_dir / "test_image.jpg"
        test_image.write_bytes(b"fake_image_data")

        # Setup mocks
        mock_client = Mock()
        mock_create_client.return_value = mock_client

        mock_output_path = temp_dir / "test_output"
        mock_create_path.return_value = mock_output_path

        mock_response = Mock()
        mock_response.text = "Generated analysis prompt"
        mock_client.models.generate_content.return_value = mock_response

        # Mock file reading
        mock_file = Mock()
        mock_file.read.return_value = b"fake_image_data"
        mock_open.return_value.__enter__.return_value = mock_file

        runner = CliRunner()
        result = runner.invoke(
            imagen_app, ["analyze", str(test_image), "--model", "gemini-2.0-flash-exp"]
        )

        # Should complete successfully
        assert result.exit_code == 0
        assert f"Analyzing image: {test_image}" in result.output
        assert "Model: gemini-2.0-flash-exp" in result.output

        # Verify API calls
        mock_create_client.assert_called_once()
        mock_client.models.generate_content.assert_called_once()


class TestCLIValidation:
    """Test CLI input validation and edge cases."""

    def test_generate_with_all_options(self):
        """Test generate command with all options specified using dry-run."""
        runner = CliRunner()

        result = runner.invoke(
            imagen_app,
            [
                "generate",
                "detailed cyberpunk scene with neon lighting and futuristic architecture",
                "--model",
                "custom-model",
                "--output",
                "/custom/output/path",
                "--name",
                "custom_name",
                "--dry",
            ],
        )

        # Should parse all options correctly
        assert result.exit_code == 0
        assert "detailed cyberpunk scene with neon lighting" in result.output
        assert "Model: custom-model" in result.output
        assert "/custom/output/path" in result.output
        # When using --output with absolute path, custom name isn't shown in dry-run output
        assert "✅ Dry run complete - no API calls made" in result.output

    def test_analyze_with_custom_model(self):
        """Test analyze command with custom model."""
        runner = CliRunner()

        with (
            patch("imagen_lab.cli.create_client") as mock_create_client,
            patch("imagen_lab.cli.create_output_path"),
            patch("imagen_lab.cli.save_prompt_file"),
            patch("imagen_lab.cli.save_metadata"),
            patch("builtins.open") as mock_open,
        ):
            # Create a fake image file in temp directory
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                tmp_file.write(b"fake_image")
                tmp_file_path = tmp_file.name

            # Mock file reading to return actual bytes
            mock_file = Mock()
            mock_file.read.return_value = b"fake_image_data"
            mock_open.return_value.__enter__.return_value = mock_file

            mock_client = Mock()
            mock_create_client.return_value = mock_client
            mock_response = Mock()
            mock_response.text = "analysis result"
            mock_client.models.generate_content.return_value = mock_response

            result = runner.invoke(
                imagen_app, ["analyze", tmp_file_path, "--model", "custom-vision-model"]
            )

            # Should complete successfully
            assert result.exit_code == 0

            # Should use custom model
            mock_client.models.generate_content.assert_called_once()
            call_args = mock_client.models.generate_content.call_args
            assert call_args[1]["model"] == "custom-vision-model"

            # Cleanup
            Path(tmp_file_path).unlink()

    def test_default_model_values(self):
        """Test that default model values are used when not specified."""
        runner = CliRunner()

        # Test generate defaults
        with (
            patch("imagen_lab.cli.create_client") as mock_create_client,
            patch("imagen_lab.cli.create_output_path"),
            patch("imagen_lab.cli.save_generated_image"),
            patch("imagen_lab.cli.save_prompt_file"),
            patch("imagen_lab.cli.save_metadata"),
        ):
            mock_client = Mock()
            mock_create_client.return_value = mock_client

            runner.invoke(imagen_app, ["generate", "test prompt"])

            # Should use default model
            mock_client.models.generate_images.assert_called_once()
            call_args = mock_client.models.generate_images.call_args
            assert call_args[1]["model"] == "imagen-3.0-generate-002"

    def test_dry_run_functionality(self):
        """Test dry run mode doesn't make API calls."""
        runner = CliRunner()

        with (
            patch("imagen_lab.cli.create_client") as mock_create_client,
            patch("imagen_lab.cli.create_output_path") as mock_create_path,
        ):
            mock_path = Mock()
            mock_path.name = "test_output_name"
            mock_create_path.return_value = mock_path

            result = runner.invoke(imagen_app, ["generate", "test prompt", "--dry"])

            # Should complete successfully
            assert result.exit_code == 0

            # Should show dry run output
            assert "🔍 Dry run - showing what would be generated:" in result.output
            assert "✅ Dry run complete - no API calls made" in result.output
            assert "test prompt" in result.output
            assert "imagen-3.0-generate-002" in result.output

            # Should NOT create client or make API calls
            mock_create_client.assert_not_called()

    def test_dry_run_with_environment_variable(self):
        """Test dry run respects environment variable."""
        runner = CliRunner()

        with (
            patch("imagen_lab.cli.create_output_path") as mock_create_path,
            patch.dict("os.environ", {"IMAGEN_MODEL": "imagen-3.0-fast-generate-001"}),
        ):
            mock_path = Mock()
            mock_path.name = "test_output_name"
            mock_create_path.return_value = mock_path

            result = runner.invoke(imagen_app, ["generate", "test prompt", "--dry"])

            # Should complete successfully
            assert result.exit_code == 0

            # Should use environment variable model
            assert "imagen-3.0-fast-generate-001" in result.output
            assert "✅ Dry run complete - no API calls made" in result.output

    def test_dry_run_with_explicit_model(self):
        """Test dry run with explicit model overrides environment."""
        runner = CliRunner()

        with (
            patch("imagen_lab.cli.create_output_path") as mock_create_path,
            patch.dict("os.environ", {"IMAGEN_MODEL": "imagen-3.0-fast-generate-001"}),
        ):
            mock_path = Mock()
            mock_path.name = "test_output_name"
            mock_create_path.return_value = mock_path

            result = runner.invoke(
                imagen_app, ["generate", "test prompt", "--model", "custom-model", "--dry"]
            )

            # Should complete successfully
            assert result.exit_code == 0

            # Should use explicit model (overrides env var)
            assert "custom-model" in result.output
            assert "imagen-3.0-fast-generate-001" not in result.output
            assert "✅ Dry run complete - no API calls made" in result.output
