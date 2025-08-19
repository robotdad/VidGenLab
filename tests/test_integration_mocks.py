"""Integration tests using mocks instead of real API calls."""

import json
from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch

from veo_lab.common import VideoResult
from veo_lab.common import generate_video


class TestVideoGenerationMocks:
    """Test video generation workflow with mocked API calls."""

    @patch("veo_lab.common.save_generated_video")
    @patch("veo_lab.common.wait_for_video_operation")
    @patch("veo_lab.common.extract_last_frame")
    def test_generate_video_success(
        self, mock_extract_frame, mock_wait_op, mock_save_video, temp_dir
    ):
        """Test successful video generation with mocks."""
        # Setup mocks
        mock_client = Mock()
        mock_operation = Mock()
        mock_operation.name = "test_operation_id"
        mock_client.models.generate_videos.return_value = mock_operation

        mock_wait_op.return_value = mock_operation

        # Mock save_generated_video to return the expected path in session_dir
        def mock_save_video_func(client, op, dest_path):
            dest_path.touch()  # Create the file
            return dest_path

        mock_save_video.side_effect = mock_save_video_func

        # Mock extract_last_frame to return the expected thumbnail path
        def mock_extract_frame_func(video_path, thumb_path):
            thumb_path.touch()  # Create the thumbnail
            return thumb_path

        mock_extract_frame.side_effect = mock_extract_frame_func

        # Execute
        result = generate_video(
            mock_client, "test cyberpunk prompt", script_name="test_script", session_dir=temp_dir
        )

        # Verify result
        assert isinstance(result, VideoResult)
        assert result.prompt == "test cyberpunk prompt"
        assert result.op_name == "test_operation_id"
        assert result.session_dir == temp_dir
        # Path should be in the session directory
        assert result.path.parent == temp_dir
        assert result.path.exists()
        # Thumbnail should also exist
        assert result.thumb is not None
        assert result.thumb.exists()

        # Verify API calls
        mock_client.models.generate_videos.assert_called_once()
        mock_wait_op.assert_called_once_with(mock_client, mock_operation)
        mock_save_video.assert_called_once()
        mock_extract_frame.assert_called_once()

        # Verify metadata was created
        metadata_file = temp_dir / "metadata.json"
        assert metadata_file.exists()

        metadata = json.loads(metadata_file.read_text())
        assert metadata["script"] == "test_script"
        assert metadata["primary_prompt"] == "test cyberpunk prompt"

    @patch("veo_lab.common.save_generated_video")
    @patch("veo_lab.common.wait_for_video_operation")
    def test_generate_video_with_reference_image(self, mock_wait_op, mock_save_video, temp_dir):
        """Test video generation with reference image."""
        # Setup mocks
        mock_client = Mock()
        mock_operation = Mock()
        mock_client.models.generate_videos.return_value = mock_operation
        mock_wait_op.return_value = mock_operation

        # Mock save_generated_video to return the expected path in session_dir
        def mock_save_video_func(client, op, dest_path):
            dest_path.touch()  # Create the file
            return dest_path

        mock_save_video.side_effect = mock_save_video_func

        # Mock reference image
        mock_ref_image = Mock()

        # Execute with reference image
        result = generate_video(
            mock_client,
            "test prompt with reference",
            image=mock_ref_image,
            script_name="test_script",
            session_dir=temp_dir,
        )

        # Verify reference image was passed to API
        call_args = mock_client.models.generate_videos.call_args
        assert call_args[1]["image"] == mock_ref_image
        assert result.path.parent == temp_dir
        assert result.path.exists()

    def test_generate_video_model_selection(self, temp_dir):
        """Test model selection priority."""
        mock_client = Mock()

        with (
            patch.dict("os.environ", {"VEO_MODEL": "veo-env-model"}),
            patch("veo_lab.common.save_generated_video"),
            patch("veo_lab.common.wait_for_video_operation") as mock_wait,
        ):
            mock_operation = Mock()
            mock_client.models.generate_videos.return_value = mock_operation
            mock_wait.return_value = mock_operation

            # Test explicit model takes priority
            generate_video(
                mock_client,
                "test prompt",
                model="explicit-model",
                script_name="test_script",
                session_dir=temp_dir,
            )

            call_args = mock_client.models.generate_videos.call_args
            assert call_args[1]["model"] == "explicit-model"

    @patch("veo_lab.common.extract_last_frame")
    def test_generate_video_thumbnail_failure(self, mock_extract_frame, temp_dir):
        """Test graceful handling of thumbnail extraction failure."""
        # Setup mocks
        mock_client = Mock()
        mock_operation = Mock()

        with (
            patch("veo_lab.common.save_generated_video") as mock_save_video,
            patch("veo_lab.common.wait_for_video_operation") as mock_wait_op,
        ):
            mock_client.models.generate_videos.return_value = mock_operation
            mock_wait_op.return_value = mock_operation

            # Mock save_generated_video to return the expected path in session_dir
            def mock_save_video_func(client, op, dest_path):
                dest_path.touch()  # Create the file
                return dest_path

            mock_save_video.side_effect = mock_save_video_func

            # Make thumbnail extraction fail
            mock_extract_frame.side_effect = Exception("FFmpeg not found")

            # Should complete successfully despite thumbnail failure
            result = generate_video(
                mock_client, "test prompt", script_name="test_script", session_dir=temp_dir
            )

            assert result.path.parent == temp_dir
            assert result.path.exists()
            assert result.thumb is None  # Should be None when extraction fails


class TestWorkflowIntegration:
    """Test complete workflow integration with mocks."""

    def test_character_pack_workflow_mock(self, temp_dir):
        """Test character pack workflow with mocked components."""
        from veo_lab.character_pack import run as character_pack_run

        # Create mock reference directory with fake images
        ref_dir = temp_dir / "refs"
        ref_dir.mkdir()
        (ref_dir / "char1.jpg").write_bytes(b"fake_image_1")
        (ref_dir / "char2.jpg").write_bytes(b"fake_image_2")

        with (
            patch("veo_lab.character_pack.create_client") as mock_create_client,
            patch("veo_lab.character_pack.generate_video") as mock_generate_video,
            patch("veo_lab.character_pack.image_from_file") as mock_image_from_file,
        ):
            mock_client = Mock()
            mock_create_client.return_value = mock_client

            # Mock image loading
            mock_image_from_file.side_effect = [Mock(), Mock()]  # Two mock images

            # Mock video generation
            mock_result1 = Mock()
            mock_result1.path = temp_dir / "video1.mp4"
            mock_result2 = Mock()
            mock_result2.path = temp_dir / "video2.mp4"
            mock_generate_video.side_effect = [mock_result1, mock_result2]

            # Execute character pack
            character_pack_run(
                scene_prompt="test scene",
                ref_dir=ref_dir,
                k=2,
                output=temp_dir,
                model="veo-2.0-generate-001",
                dry=False,
            )

            # Verify workflow
            assert mock_image_from_file.call_count == 2
            assert mock_generate_video.call_count == 2

            # Verify generate_video was called with correct parameters
            for call in mock_generate_video.call_args_list:
                assert call[0][1] == "test scene"  # scene prompt
                assert "image" in call[1]  # reference image passed

    def test_shot_chain_workflow_mock(self, temp_dir):
        """Test shot chain workflow with mocked components."""
        from veo_lab.shot_chain import run as shot_chain_run

        # Create mock YAML file
        chain_config = temp_dir / "chain.yml"
        chain_config.write_text("""
prompts:
  - "First shot prompt"
  - "Second shot prompt"
  - "Third shot prompt"
""")

        with (
            patch("veo_lab.shot_chain.create_client") as mock_create_client,
            patch("veo_lab.shot_chain.generate_video") as mock_generate_video,
            patch("veo_lab.shot_chain.image_from_file") as mock_image_from_file,
        ):
            mock_client = Mock()
            mock_create_client.return_value = mock_client

            # Mock video results with thumbnails
            mock_results = []
            for i in range(3):
                mock_result = Mock()
                mock_result.path = temp_dir / f"shot_{i + 1}.mp4"
                mock_result.thumb = temp_dir / f"shot_{i + 1}.last.jpg"
                # Create the thumbnail file
                mock_result.thumb.touch()
                mock_results.append(mock_result)

            mock_generate_video.side_effect = mock_results

            # Mock image loading from thumbnails
            mock_image_from_file.return_value = Mock()

            # Execute shot chain
            shot_chain_run(
                file=chain_config,
                output=temp_dir,
                concat=None,
                model="veo-2.0-generate-001",
                dry=False,
            )

            # Verify workflow
            assert mock_generate_video.call_count == 3

            # Verify chaining: first shot has no ref, subsequent shots use previous thumb
            first_call = mock_generate_video.call_args_list[0]
            assert first_call[1].get("image") is None

            # Second and third shots should have reference images
            second_call = mock_generate_video.call_args_list[1]
            third_call = mock_generate_video.call_args_list[2]
            assert second_call[1].get("image") is not None
            assert third_call[1].get("image") is not None


class TestErrorHandling:
    """Test error handling without API calls."""

    def test_video_result_dataclass(self):
        """Test VideoResult dataclass functionality."""
        result = VideoResult(
            path=Path("/test/video.mp4"),
            op_name="test_op",
            prompt="test prompt",
            negative="test negative",
        )

        assert result.path == Path("/test/video.mp4")
        assert result.op_name == "test_op"
        assert result.prompt == "test prompt"
        assert result.negative == "test negative"
        assert result.thumb is None  # Default value
        assert result.session_dir is None  # Default value

    def test_config_loading_mock(self, temp_dir):
        """Test configuration file loading."""
        from veo_lab.prompt_matrix import load_config

        # Create test config
        config_file = temp_dir / "test_config.yml"
        config_file.write_text("""
matrix:
  subject: ["witch", "monk"]
  style: ["cyberpunk", "medieval"]
negative: ["blurry", "low quality"]
""")

        config = load_config(config_file)

        assert "matrix" in config
        assert "negative" in config
        assert config["matrix"]["subject"] == ["witch", "monk"]
        assert config["matrix"]["style"] == ["cyberpunk", "medieval"]
        assert config["negative"] == ["blurry", "low quality"]
