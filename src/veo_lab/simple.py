from __future__ import annotations

import json
import os
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
    dry: bool = typer.Option(
        False, "--dry", help="Show what would be generated without calling API"
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

    if dry:
        picked_model = model or os.environ.get("VEO_MODEL") or "veo-2.0-generate-001"
        print("🔍 Dry run - single video generation:")
        print(f"  • Prompt: {text[:50]}...")
        print(f"  • Model: {picked_model}")
        print(f"  • Negative: {negative}" if negative else "  • No negative prompt")
        print(f"  • Reference image: {image}" if image else "  • No reference image")
        print(f"  • Output directory: {out}")
        print("✅ Dry run complete - no API calls made")
        return

    client = create_client()
    img = image_from_file(image) if image else None
    res = generate_video(
        client, text, negative=negative, image=img, out_dir=out, script_name="simple", model=model
    )
    print(res.path)


if __name__ == "__main__":
    app()
