"""Tests for veo_lab.common utility functions."""

import json
import os
from unittest.mock import patch

from veo_lab.common import create_prompt_snippet
from veo_lab.common import create_session_directory
from veo_lab.common import create_video_filename
from veo_lab.common import list_models
from veo_lab.common import save_session_metadata
from veo_lab.common import stable_stem


class TestUtilityFunctions:
    """Test utility functions that don't require API calls."""

    def test_create_prompt_snippet(self):
        """Test prompt snippet creation for filenames."""
        # Basic case
        result = create_prompt_snippet("Subject: witch casting spells")
        assert result == "subject_witch_casting_spells"

        # Max words limit
        result = create_prompt_snippet("one two three four five six seven", max_words=3)
        assert result == "one_two_three"

        # Special characters removed
        result = create_prompt_snippet("Subject: witch! casting @spells# with $magic%")
        assert result == "subject_witch_casting_spells"

        # Empty/whitespace only
        result = create_prompt_snippet("")
        assert result == "untitled"

        result = create_prompt_snippet("   ")
        assert result == "untitled"

        # Very long prompt truncated
        long_prompt = "word " * 50
        result = create_prompt_snippet(long_prompt)
        assert len(result) <= 50

    def test_stable_stem(self):
        """Test stable hash generation for filenames."""
        # Same input produces same hash
        text = "test prompt for hashing"
        result1 = stable_stem(text)
        result2 = stable_stem(text)
        assert result1 == result2
        assert len(result1) == 12  # SHA1 hex[:12]

        # Different inputs produce different hashes
        result3 = stable_stem("different text")
        assert result1 != result3

        # With prefix
        result_with_prefix = stable_stem(text, prefix="test-")
        assert result_with_prefix.startswith("test-")
        assert len(result_with_prefix) == 17  # prefix + hash

    def test_create_video_filename(self):
        """Test video filename creation."""
        # Basic case
        result = create_video_filename("witch casting spells", "veo-3.0-generate-preview")
        assert result == "witch_casting_spells_3.0.mp4"

        # With sequence number
        result = create_video_filename("test prompt", "veo-2.0-generate-001", sequence_num=3)
        assert result == "03_test_prompt_2.0-generate-001.mp4"

        # Model name normalization
        result = create_video_filename("test", "veo-3.0-fast-generate-preview")
        assert result == "test_3.0-fast.mp4"

    def test_list_models(self):
        """Test model listing functionality."""
        result = list_models()

        # Should return dict with known models and default
        assert "known" in result
        assert "default" in result
        assert isinstance(result["known"], list)
        assert len(result["known"]) > 0

        # Known models should include expected values
        known_models = result["known"]
        assert "veo-3.0-generate-preview" in known_models
        assert "veo-2.0-generate-001" in known_models

        # Default should be reasonable
        assert result["default"] in known_models or result["default"] == "veo-2.0-generate-001"

    def test_list_models_with_env_var(self):
        """Test model listing with custom env var."""
        with patch.dict(os.environ, {"VEO_MODEL": "veo-3.0-fast-generate-preview"}):
            result = list_models()
            assert result["default"] == "veo-3.0-fast-generate-preview"


class TestSessionManagement:
    """Test session directory and metadata management."""

    def test_create_session_directory(self, temp_dir, sample_prompt):
        """Test session directory creation."""
        session_dir = create_session_directory("test_script", sample_prompt, temp_dir)

        # Directory should be created
        assert session_dir.exists()
        assert session_dir.is_dir()

        # Should be under date directory
        assert session_dir.parent.parent == temp_dir

        # Should contain script name and prompt snippet
        assert "test_script" in session_dir.name
        assert "subject_cyberpunk_witch_casting" in session_dir.name

        # Latest symlink should be created
        latest_link = temp_dir / "latest"
        assert latest_link.exists()
        assert latest_link.is_symlink()

    def test_save_session_metadata(self, temp_dir, sample_prompt):
        """Test metadata file creation."""
        session_dir = temp_dir / "test_session"
        session_dir.mkdir()

        metadata_file = save_session_metadata(
            session_dir,
            script_name="test_script",
            prompt=sample_prompt,
            negative="blurry, low quality",
            model="veo-3.0-generate-preview",
            files=["test.mp4"],
        )

        # Metadata file should be created
        assert metadata_file.exists()
        assert metadata_file.name == "metadata.json"

        # Load and verify metadata
        metadata = json.loads(metadata_file.read_text())
        assert metadata["script"] == "test_script"
        assert metadata["primary_prompt"] == sample_prompt
        assert metadata["current_prompt"] == sample_prompt
        assert metadata["negative"] == "blurry, low quality"
        assert metadata["model"] == "veo-3.0-generate-preview"
        assert metadata["files"] == ["test.mp4"]
        assert "timestamp" in metadata
        assert "prompt_hash" in metadata

        # Prompt file should also be created
        prompt_file = session_dir / "prompt.txt"
        assert prompt_file.exists()
        prompt_content = prompt_file.read_text()
        assert sample_prompt in prompt_content
        assert "blurry, low quality" in prompt_content

    def test_save_session_metadata_accumulative(self, temp_dir):
        """Test that metadata accumulates files across multiple saves."""
        session_dir = temp_dir / "test_session"
        session_dir.mkdir()

        # First save
        save_session_metadata(
            session_dir, script_name="test_script", prompt="first prompt", files=["video1.mp4"]
        )

        # Second save
        save_session_metadata(
            session_dir, script_name="test_script", prompt="second prompt", files=["video2.mp4"]
        )

        # Metadata should contain both files
        metadata_file = session_dir / "metadata.json"
        metadata = json.loads(metadata_file.read_text())
        assert metadata["files"] == ["video1.mp4", "video2.mp4"]
        assert metadata["primary_prompt"] == "first prompt"  # Should preserve first
        assert metadata["current_prompt"] == "second prompt"  # Should update to latest


class TestPathUtilities:
    """Test path and filename utilities."""

    def test_prompt_snippet_edge_cases(self):
        """Test edge cases for prompt snippet generation."""
        # Unicode characters
        result = create_prompt_snippet("ñoño ükümüs")
        assert len(result) > 0  # Should handle gracefully

        # Very short prompt
        result = create_prompt_snippet("hi")
        assert result == "hi"

        # Only special characters
        result = create_prompt_snippet("!@#$%^&*()")
        assert result == "untitled"

        # Mixed case normalization
        result = create_prompt_snippet("CyberPunk WITCH Casting")
        assert result == "cyberpunk_witch_casting"

    def test_filename_safety(self):
        """Test that generated filenames are filesystem safe."""
        dangerous_prompt = 'test/\\:*?"<>|prompt'
        result = create_prompt_snippet(dangerous_prompt)

        # Should not contain dangerous characters
        dangerous_chars = '/\\:*?"<>|'
        for char in dangerous_chars:
            assert char not in result

        # Should still be meaningful
        assert "test" in result
        assert "prompt" in result
