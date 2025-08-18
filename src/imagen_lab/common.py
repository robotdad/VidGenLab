from __future__ import annotations

import json
import os
import pathlib
import re
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from google import genai

load_dotenv()

# Known Imagen model ids
KNOWN_IMAGEN_MODELS = [
    "imagen-3.0-generate-001",
    "imagen-3.0-fast-generate-001",
]


def list_models():
    """Return known model ids and the current default from env."""
    return {
        "known": KNOWN_IMAGEN_MODELS,
        "default": os.environ.get("IMAGEN_MODEL", "imagen-3.0-generate-001"),
    }


def create_client() -> genai.Client:
    return genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def create_output_path(
    script_name: str,
    prompt: str,
    output_dir: pathlib.Path | None = None,
    custom_name: str | None = None,
) -> pathlib.Path:
    """Create output path following same naming pattern as veo_lab."""
    if output_dir:
        return pathlib.Path(output_dir)

    root = pathlib.Path(__file__).resolve().parents[2]
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H%M%S")

    # Create prompt slug (same logic as veo_lab)
    prompt_slug = re.sub(r"[^\w\s-]", "", prompt.lower())
    prompt_slug = re.sub(r"[-\s]+", "_", prompt_slug).strip("_")
    if len(prompt_slug) > 50:
        prompt_slug = prompt_slug[:50].rstrip("_")

    if custom_name:
        folder_name = f"{timestamp}_{script_name}_{custom_name}"
    else:
        folder_name = f"{timestamp}_{script_name}_{prompt_slug}"

    return root / "out" / today / folder_name


def save_metadata(
    output_path: pathlib.Path,
    prompt: str,
    script_name: str,
    model: str,
    **kwargs: Any,
) -> None:
    """Save metadata JSON file."""
    metadata = {
        "prompt": prompt,
        "script": script_name,
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "output_path": str(output_path),
        **kwargs,
    }

    metadata_file = output_path / "metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def save_prompt_file(output_path: pathlib.Path, prompt: str) -> None:
    """Save prompt to text file."""
    prompt_file = output_path / "prompt.txt"
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt)


def save_generated_image(
    response: Any,
    output_path: pathlib.Path,
    filename: str = "generated_image.jpg",
) -> pathlib.Path:
    """Save generated image from Imagen response."""
    if not hasattr(response, "generated_images") or not response.generated_images:
        raise ValueError("No generated images in response")

    image = response.generated_images[0].image
    image_path = output_path / filename

    # Save image data
    with open(image_path, "wb") as f:
        f.write(image.data)

    return image_path
