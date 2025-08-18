from __future__ import annotations

import contextlib
import hashlib
import json
import os
import pathlib
import re
import subprocess
import time
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv  # add
from google import genai
from google.genai import types

load_dotenv()  # add (loads .env from project root)


ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True, parents=True)

# Known Veo model ids (Gemini API / Vertex naming may vary by preview line)
KNOWN_VEO_MODELS = [
    "veo-3.0-generate-preview",
    "veo-3.0-fast-generate-preview",
    "veo-2.0-generate-001",
]


def list_models():
    """Return known model ids and the current default from env."""
    return {
        "known": KNOWN_VEO_MODELS,
        "default": os.environ.get("VEO_MODEL", "veo-2.0-generate-001"),
    }


def create_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key) if api_key else genai.Client()


@dataclass
class VideoResult:
    path: pathlib.Path
    op_name: str
    prompt: str
    negative: str
    thumb: pathlib.Path | None = None
    session_dir: pathlib.Path | None = None
    metadata_file: pathlib.Path | None = None


def wait_for_video_operation(client: genai.Client, op, poll_seconds: int = 8):
    while True:
        if getattr(op, "done", None) is True:
            break
        time.sleep(poll_seconds)
        try:
            op = client.operations.get(op)
        except Exception:
            with contextlib.suppress(Exception):
                op = client.operations.get(getattr(op, "name", op))
    return op


def save_generated_video(client: genai.Client, op, dest: pathlib.Path) -> pathlib.Path:
    resp = getattr(op, "response", None)
    if not resp or not getattr(resp, "generated_videos", None):
        raise RuntimeError("operation finished but no generated_videos found")
    v = resp.generated_videos[0]
    client.files.download(file=v.video)
    dest.parent.mkdir(parents=True, exist_ok=True)
    v.video.save(str(dest))
    return dest


def stable_stem(text: str, prefix: str = "") -> str:
    h = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}{h}" if prefix else h


def extract_last_frame(mp4_path: pathlib.Path, out_jpg: pathlib.Path) -> pathlib.Path:
    ensure_ffmpeg()
    subprocess.run(
        [
            "ffmpeg",
            "-sseof",
            "-1",
            "-i",
            str(mp4_path),
            "-frames:v",
            "1",
            str(out_jpg),
            "-y",
            "-loglevel",
            "error",
        ],
        check=True,
    )
    return out_jpg


def concat_videos_concat_demuxer(
    files: Iterable[pathlib.Path], out_path: pathlib.Path
) -> pathlib.Path:
    ensure_ffmpeg()
    list_file = out_path.with_suffix(".txt")
    list_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in files), encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c",
            "copy",
            str(out_path),
            "-y",
            "-loglevel",
            "error",
        ],
        check=True,
    )
    return out_path


def image_from_file(path: pathlib.Path):
    data = path.read_bytes()
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return types.Image(image_bytes=data, mime_type=mime)


def ensure_ffmpeg():
    try:
        subprocess.run(
            ["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except Exception as e:
        raise RuntimeError("ffmpeg is required on PATH") from e


def create_prompt_snippet(prompt: str, max_words: int = 4) -> str:
    """Extract a filename-safe snippet from a prompt for naming files."""
    # Remove special characters and normalize whitespace
    cleaned = re.sub(r"[^\w\s-]", "", prompt.lower()).strip()
    # Take first few words
    words = cleaned.split()[:max_words]
    # Join with underscores and truncate if needed
    snippet = "_".join(words)[:50]  # Max 50 chars
    return snippet or "untitled"


def create_session_directory(
    script_name: str, prompt: str, base_dir: pathlib.Path = OUT
) -> pathlib.Path:
    """Create a timestamped session directory for organized output."""
    now = datetime.now()
    date_dir = base_dir / now.strftime("%Y-%m-%d")
    prompt_snippet = create_prompt_snippet(prompt)
    time_str = now.strftime("%H%M%S")

    session_name = f"{time_str}_{script_name}_{prompt_snippet}"
    session_dir = date_dir / session_name
    session_dir.mkdir(parents=True, exist_ok=True)

    # Create a symlink to latest
    latest_link = base_dir / "latest"
    if latest_link.is_symlink() or latest_link.exists():
        latest_link.unlink()
    latest_link.symlink_to(session_dir.relative_to(base_dir))

    return session_dir


def save_session_metadata(
    session_dir: pathlib.Path,
    script_name: str,
    prompt: str,
    negative: str = "",
    model: str = "",
    files: list | None = None,
) -> pathlib.Path:
    """Save metadata about the generation session."""
    metadata_file = session_dir / "metadata.json"

    # Load existing metadata if it exists (for multi-video sessions)
    if metadata_file.exists():
        existing_metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        # Add new files to the list
        existing_files = existing_metadata.get("files", [])
        all_files = existing_files + (files or [])
    else:
        all_files = files or []
        existing_metadata = {}

    metadata = {
        "timestamp": existing_metadata.get("timestamp", datetime.now().isoformat()),
        "script": script_name,
        "model": model,
        "primary_prompt": existing_metadata.get("primary_prompt", prompt),
        "current_prompt": prompt,
        "negative": negative,
        "prompt_hash": hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:8],
        "files": all_files,
    }

    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # Also save/update the prompt file
    prompt_file = session_dir / "prompt.txt"
    if not prompt_file.exists():
        full_prompt = f"Primary Prompt: {prompt}"
        if negative:
            full_prompt += f"\n\nNegative: {negative}"
        prompt_file.write_text(full_prompt, encoding="utf-8")

    return metadata_file


def create_video_filename(prompt: str, model: str, sequence_num: int | None = None) -> str:
    """Create a descriptive filename for generated videos."""
    prompt_snippet = create_prompt_snippet(prompt)
    model_short = model.replace("veo-", "").replace("-generate-preview", "").replace("-preview", "")

    if sequence_num is not None:
        return f"{sequence_num:02d}_{prompt_snippet}_{model_short}.mp4"
    return f"{prompt_snippet}_{model_short}.mp4"


def generate_video(
    client: genai.Client,
    prompt: str,
    *,
    image=None,
    negative: str = "",
    aspect_ratio: str = "16:9",
    name_prefix: str = "",
    out_dir: pathlib.Path = OUT,
    model: str | None = None,
    script_name: str = "unknown",
    sequence_num: int | None = None,
    session_dir: pathlib.Path | None = None,
) -> VideoResult:
    """Generate a single Veo clip with organized output structure.

    Model selection precedence:
    1) Explicit `model` arg
    2) VEO_MODEL environment variable
    3) "veo-2.0-generate-001"
    """
    picked_model = model or os.environ.get("VEO_MODEL") or "veo-2.0-generate-001"

    # Create session directory if not provided
    if session_dir is None:
        session_dir = create_session_directory(script_name, prompt, out_dir)

    # Generate the video
    op = client.models.generate_videos(
        model=picked_model,
        prompt=prompt,
        image=image,
        config=types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            negative_prompt=negative,
        ),
    )
    op = wait_for_video_operation(client, op)

    # Create organized filename
    if name_prefix:
        # For backward compatibility, use old naming when prefix is provided
        stem = stable_stem(prompt + negative, prefix=name_prefix)
        filename = f"{stem}.mp4"
    else:
        filename = create_video_filename(prompt, picked_model, sequence_num)

    dest = session_dir / filename
    save_generated_video(client, op, dest)

    # Extract thumbnail/last frame
    thumb = dest.with_suffix(".last.jpg")
    try:
        extract_last_frame(dest, thumb)
    except Exception:
        thumb = None

    # Save session metadata
    metadata_file = save_session_metadata(
        session_dir, script_name, prompt, negative, picked_model, [filename]
    )

    return VideoResult(
        path=dest,
        op_name=getattr(op, "name", ""),
        prompt=prompt,
        negative=negative,
        thumb=thumb,
        session_dir=session_dir,
        metadata_file=metadata_file,
    )
