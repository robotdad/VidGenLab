# src/**/*.py

[collect-files]

**Search:** ['src/**/*.py']
**Exclude:** ['__pycache__', '*.pyc', '.pytest_cache', '*.egg-info']
**Include:** []
**Date:** 8/18/2025, 10:40:52 AM
**Files:** 13

=== File: src/imagen_lab/__init__.py ===
__all__ = []
__version__ = "0.1.0"


=== File: src/imagen_lab/cli.py ===
from __future__ import annotations

import pathlib
from typing import Annotated

import typer

from imagen_lab.common import create_client
from imagen_lab.common import create_output_path
from imagen_lab.common import save_generated_image
from imagen_lab.common import save_metadata
from imagen_lab.common import save_prompt_file

app = typer.Typer(
    name="imagen_lab",
    help="Image generation lab using Google's Imagen API",
    no_args_is_help=True,
)


@app.command()
def generate(
    prompt: Annotated[str, typer.Argument(help="Text prompt for image generation")],
    model: Annotated[
        str, typer.Option("--model", "-m", help="Model to use for generation")
    ] = "imagen-3.0-generate-001",
    output: Annotated[
        pathlib.Path | None,
        typer.Option("--output", "-o", help="Custom output directory"),
    ] = None,
    custom_name: Annotated[
        str | None,
        typer.Option("--name", help="Custom name for output folder"),
    ] = None,
) -> None:
    """Generate an image from a text prompt using Imagen."""
    print(f"Generating image: {prompt}")
    print(f"Model: {model}")

    # Create client and output paths
    client = create_client()
    output_path = create_output_path("imagen", prompt, output, custom_name)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Output: {output_path}")

    try:
        # Generate image
        response = client.models.generate_images(model=model, prompt=prompt)

        # Save files
        image_filename = f"{output_path.name}.jpg"
        image_path = save_generated_image(response, output_path, image_filename)
        save_prompt_file(output_path, prompt)
        save_metadata(output_path, prompt, "imagen", model)

        print(f"✅ Generated: {image_path}")

    except Exception as e:
        print(f"❌ Generation failed: {e}")
        raise typer.Exit(1)


@app.command()
def analyze(
    image_path: Annotated[pathlib.Path, typer.Argument(help="Path to image file")],
    model: Annotated[
        str, typer.Option("--model", "-m", help="Vision model to use for analysis")
    ] = "gemini-2.0-flash-exp",
    output: Annotated[
        pathlib.Path | None,
        typer.Option("--output", "-o", help="Custom output directory"),
    ] = None,
) -> None:
    """Analyze an image and generate a descriptive prompt."""
    if not image_path.exists():
        print(f"❌ Image file not found: {image_path}")
        raise typer.Exit(1)

    print(f"Analyzing image: {image_path}")
    print(f"Model: {model}")

    # Create client and output paths
    client = create_client()
    analysis_prompt = "Describe this image in detail, focusing on visual elements, style, composition, and mood. Create a prompt that could be used to generate a similar image."

    output_path = create_output_path("analyze", f"analysis_of_{image_path.stem}", output)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Output: {output_path}")

    try:
        # Read and analyze image
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Create image part using genai types
        from google.genai import types

        image_part = types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_data))

        response = client.models.generate_content(
            model=model, contents=[analysis_prompt, image_part]
        )

        generated_prompt = (
            response.text if hasattr(response, "text") and response.text else str(response)
        )

        # Save analysis results
        save_prompt_file(output_path, generated_prompt)
        save_metadata(
            output_path,
            analysis_prompt,
            "analyze",
            model,
            source_image=str(image_path),
            generated_prompt=generated_prompt,
        )

        print(f"✅ Analysis complete: {output_path}")
        print(f"Generated prompt: {generated_prompt}")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()


=== File: src/imagen_lab/common.py ===
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


=== File: src/veo_lab/__init__.py ===
__all__ = []
__version__ = "0.1.1"


=== File: src/veo_lab/ab_viewer.py ===
from __future__ import annotations

import json
import pathlib

import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "out"
RATINGS = OUT / "ratings.json"


def load_results() -> list[pathlib.Path]:
    return sorted(p for p in OUT.glob("*.mp4"))


def load_ratings() -> dict[str, int]:
    if RATINGS.exists():
        return json.loads(RATINGS.read_text(encoding="utf-8"))
    return {}


def save_ratings(data: dict[str, int]):
    OUT.mkdir(parents=True, exist_ok=True)
    RATINGS.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    st.set_page_config(page_title="Veo3 A/B Viewer", layout="wide")
    st.title("Veo3 A/B Viewer")
    videos = load_results()
    ratings = load_ratings()
    cols = st.columns(3)
    for i, vid in enumerate(videos):
        with cols[i % 3]:
            st.video(str(vid))
            key = vid.name
            score = ratings.get(key, 0)
            c1, c2, c3 = st.columns(3)
            if c1.button("👍", key=f"up-{key}"):
                ratings[key] = score + 1
            if c2.button("👎", key=f"down-{key}"):
                ratings[key] = score - 1
            if c3.button("reset", key=f"reset-{key}"):
                ratings[key] = 0
            st.caption(f"{key} — score: {ratings.get(key, 0)}")
    if st.button("Save ratings"):
        save_ratings(ratings)
        st.success(f"Saved to {RATINGS}")


if __name__ == "__main__":
    main()


=== File: src/veo_lab/character_pack.py ===
from __future__ import annotations

import pathlib

import typer

from .common import OUT
from .common import create_client
from .common import generate_video
from .common import image_from_file

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    scene_prompt: str = typer.Option(..., "--scene"),
    ref_dir: pathlib.Path | None = typer.Option(None, "--ref-dir"),
    imagen_prompts_file: pathlib.Path | None = typer.Option(None, "--imagen-prompts"),
    k: int = typer.Option(3),
    output: pathlib.Path = typer.Option(OUT, "--out"),
):
    client = create_client()
    refs: list = []
    if ref_dir:
        paths = sorted(
            [
                p
                for p in pathlib.Path(ref_dir).glob("*")
                if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
            ]
        )[:k]
        for p in paths:
            refs.append(image_from_file(p))
    if imagen_prompts_file and not refs:
        lines = [
            ln.strip()
            for ln in imagen_prompts_file.read_text(encoding="utf-8").splitlines()
            if ln.strip()
        ]
        for ln in lines[:k]:
            try:
                r = client.models.generate_images(model="imagen-3.0-generate-002", prompt=ln)
                if r.generated_images:
                    refs.append(r.generated_images[0].image)
            except Exception as e:
                print(f"Imagen generate failed: {e}")
    assert refs, "no reference images available (provide --ref-dir or --imagen-prompts)"
    outs = []
    for i, ref in enumerate(refs, start=1):
        res = generate_video(
            client, scene_prompt, image=ref, out_dir=output, name_prefix=f"pack{i:02d}-"
        )
        outs.append(res.path)
    print(f"done {len(outs)} clips -> {output}")


if __name__ == "__main__":
    app()


=== File: src/veo_lab/common.py ===
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


=== File: src/veo_lab/prompt_matrix.py ===
from __future__ import annotations

import itertools
import json
import pathlib

import typer
import yaml
from jinja2 import Template

from .common import OUT
from .common import create_client
from .common import generate_video

app = typer.Typer(add_completion=False, no_args_is_help=True)


def load_config(path: pathlib.Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@app.command()
def run(
    config: pathlib.Path = typer.Option(..., "--config", "-c"),
    template: pathlib.Path = typer.Option(..., "--template", "-t"),
    output: pathlib.Path = typer.Option(OUT, "--out"),
    dry: bool = typer.Option(False, "--dry"),
):
    cfg = load_config(config)
    tpl_text = template.read_text(encoding="utf-8")
    dims = cfg.get("matrix", {})
    negatives: list[str] = cfg.get("negative", [""])
    bank = sorted(dims.keys())
    combos = list(itertools.product(*(dims[k] for k in bank)))
    client = create_client()
    rows = []
    for combo in combos:
        vars_ = dict(zip(bank, combo, strict=False))
        prompt = Template(tpl_text).render(**vars_).strip()
        for neg in negatives:
            if dry:
                print(prompt)
                continue
            res = generate_video(client, prompt, negative=neg, out_dir=output, name_prefix="mx-")
            rows.append(
                {
                    "prompt": prompt,
                    "negative": neg,
                    "path": str(res.path),
                    "thumb": str(res.thumb or ""),
                }
            )
    if rows and not dry:
        (output / "matrix_results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"saved {len(rows)} results -> {output}")


if __name__ == "__main__":
    app()


=== File: src/veo_lab/prompt_rewriter.py ===
from __future__ import annotations

import json
import pathlib

import typer
from google.genai import types

from .common import create_client

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    base_spec_file: pathlib.Path = typer.Option(..., "--base-spec", "-b"),
    n: int = typer.Option(6, "--n"),
    out_json: pathlib.Path = typer.Option(pathlib.Path("out/rewrites.json"), "--out"),
):
    client = create_client()
    base = base_spec_file.read_text(encoding="utf-8").strip()
    sys_prompt = "You write Veo-3 prompts with explicit Subject, Action, Style, Camera, Ambience, and Audio cues. Return a JSON list of strings."
    res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{sys_prompt}\n\nCreate {n} diverse Veo prompts from this spec:\n{base}",
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    try:
        text = res.text if hasattr(res, "text") and res.text else str(res)
        variants: list[str] = json.loads(text)
    except Exception:
        txt = res.text if hasattr(res, "text") and res.text else str(res)
        variants = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(variants, indent=2), encoding="utf-8")
    print(f"wrote {len(variants)} variants -> {out_json}")


if __name__ == "__main__":
    app()


=== File: src/veo_lab/ref_image_lab.py ===
from __future__ import annotations

import pathlib

import typer

from .common import OUT
from .common import create_client
from .common import generate_video
from .common import image_from_file

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    ref_dir: pathlib.Path = typer.Option(..., "--ref-dir"),
    scene_prompt_file: pathlib.Path = typer.Option(..., "--scene"),
    output: pathlib.Path = typer.Option(OUT, "--out"),
):
    prompt = scene_prompt_file.read_text(encoding="utf-8").strip()
    client = create_client()
    imgs = sorted([p for p in ref_dir.glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    assert imgs, "no images found in ref_dir"
    for i, path in enumerate(imgs, start=1):
        ref = image_from_file(path)
        res = generate_video(client, prompt, image=ref, out_dir=output, name_prefix=f"ref{i:03d}-")
        print(f"{path.name} -> {res.path.name}")


if __name__ == "__main__":
    app()


=== File: src/veo_lab/shot_chain.py ===
from __future__ import annotations

import pathlib

import typer
import yaml

from .common import OUT
from .common import create_client
from .common import create_session_directory
from .common import generate_video
from .common import image_from_file

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    file: pathlib.Path = typer.Option(..., "--file", "-f"),
    output: pathlib.Path = typer.Option(OUT, "--out"),
):
    data = yaml.safe_load(file.read_text(encoding="utf-8"))
    prompts: list[str] = data.get("prompts", [])
    assert prompts, "no prompts found"
    client = create_client()

    # Create a single session directory for the entire chain
    first_prompt = prompts[0] if prompts else "chain"
    session_dir = create_session_directory("shot_chain", first_prompt, output)

    last_ref = None
    outs = []
    for i, p in enumerate(prompts, start=1):
        res = generate_video(
            client,
            p,
            image=last_ref,
            script_name="shot_chain",
            sequence_num=i,
            session_dir=session_dir,
        )
        outs.append(res.path)
        # Use the thumbnail that was already created
        if res.thumb:
            last_ref = image_from_file(res.thumb)
    print(f"done {len(outs)} clips -> {session_dir}")


if __name__ == "__main__":
    app()


=== File: src/veo_lab/simple.py ===
from __future__ import annotations

import json
import pathlib

import typer

from .common import OUT
from .common import create_client
from .common import generate_video
from .common import image_from_file
from .common import list_models

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    prompt: str = typer.Option(None, "--prompt", "-p", help="Inline prompt string"),
    prompt_file: pathlib.Path = typer.Option(
        None, "--prompt-file", "-f", help="Path to a text file with the prompt"
    ),
    negative: str = typer.Option("", "--negative", "-n", help="Negative prompt"),
    image: pathlib.Path = typer.Option(
        None, "--image", "-i", help="Optional ref image (jpg/png) for image→video"
    ),
    out: pathlib.Path = typer.Option(OUT, "--out", help="Output directory"),
    model: str = typer.Option(
        None,
        "--model",
        help="Veo model id (e.g. veo-3.0-generate-preview, veo-3.0-fast-generate-preview, veo-2.0-generate-001)",
    ),
    list_models_flag: bool = typer.Option(
        False, "--list-models", help="List known model ids and current default"
    ),
):
    """
    one-shot video generation: send a prompt (and optional negative/ref image) to veo 3.
    """
    if list_models_flag:
        print(json.dumps(list_models(), indent=2))
        return
    if not prompt and not prompt_file:
        raise typer.BadParameter("provide --prompt or --prompt-file")
    text = prompt or prompt_file.read_text(encoding="utf-8").strip()
    client = create_client()
    img = image_from_file(image) if image else None
    res = generate_video(
        client, text, negative=negative, image=img, out_dir=out, script_name="simple", model=model
    )
    print(res.path)


if __name__ == "__main__":
    app()


=== File: src/veo_lab/storyboard.py ===
from __future__ import annotations

import json
import pathlib

import typer

from .common import OUT
from .common import concat_videos_concat_demuxer
from .common import create_client
from .common import create_session_directory
from .common import generate_video
from .common import image_from_file

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    storyboard: pathlib.Path = typer.Option(..., "--storyboard", "-s"),
    output_dir: pathlib.Path = typer.Option(OUT, "--out"),
    concat_to: pathlib.Path | None = typer.Option(None, "--concat"),
):
    data: dict = json.loads(storyboard.read_text(encoding="utf-8"))
    shots: list[dict] = data.get("shots", [])
    assert shots, "no shots found"
    client = create_client()

    # Create a single session directory for the entire storyboard
    first_shot = shots[0]["prompt"] if shots else "storyboard"
    session_dir = create_session_directory("storyboard", first_shot, output_dir)

    prev_last_ref = None
    clip_paths: list[pathlib.Path] = []
    for idx, shot in enumerate(shots, start=1):
        prompt: str = shot["prompt"]
        negative: str = shot.get("negative", "")
        carry_last: bool = bool(shot.get("carry_last_frame", False))
        image_path = shot.get("image")
        ref = prev_last_ref if (carry_last and prev_last_ref is not None) else None
        if image_path:
            ref = image_from_file(pathlib.Path(image_path))
        res = generate_video(
            client,
            prompt,
            negative=negative,
            image=ref,
            script_name="storyboard",
            sequence_num=idx,
            session_dir=session_dir,
        )
        clip_paths.append(res.path)
        # Use the thumbnail that was already created
        if res.thumb:
            prev_last_ref = image_from_file(res.thumb)
    print(f"rendered {len(clip_paths)} shots")
    if concat_to:
        if not concat_to.is_absolute():
            concat_to = session_dir / concat_to.name
        concat_videos_concat_demuxer(clip_paths, concat_to)
        print(f"stitched -> {concat_to}")


if __name__ == "__main__":
    app()


