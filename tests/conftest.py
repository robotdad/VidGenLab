"""Test configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_prompt():
    """Sample prompt for testing."""
    return "Subject: cyberpunk witch casting holographic spells in neon-lit chamber"


@pytest.fixture
def sample_metadata():
    """Sample metadata for testing."""
    return {
        "prompt": "test prompt",
        "script": "test_script",
        "model": "test-model",
        "timestamp": "2025-01-18T10:30:00",
    }
