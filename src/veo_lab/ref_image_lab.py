from __future__ import annotations

import os
import pathlib
import time

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
    model: str | None = typer.Option(
        None,
        "--model",
        help="Veo model id (e.g. veo-3.0-generate-preview, veo-3.0-fast-generate-preview, veo-2.0-generate-001)",
    ),
    dry: bool = typer.Option(
        False, "--dry", help="Show what would be generated without calling API"
    ),
):
    prompt = scene_prompt_file.read_text(encoding="utf-8").strip()
    imgs = sorted([p for p in ref_dir.glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    assert imgs, "no images found in ref_dir"

    # Model selection
    picked_model = model or os.environ.get("VEO_MODEL")
    if not picked_model:
        raise typer.BadParameter("Specify --model or set VEO_MODEL environment variable")

    if dry:
        print(f"🔍 Dry run - ref image lab with {len(imgs)} reference images:")
        print(f"  • Scene prompt: {prompt[:50]}...")
        print(f"  • Reference directory: {ref_dir}")
        for idx, img_path in enumerate(imgs, start=1):
            print(f"    Image {idx}: {img_path.name}")
        print(f"  • Model: {picked_model}")
        print(f"  • Output directory: {output}")
        print("✅ Dry run complete - no API calls made")
        return

    client = create_client()
    for i, path in enumerate(imgs, start=1):
        # Add rate limit protection: wait 30 seconds between requests (except first)
        if i > 1:
            print("⏳ Waiting 30 seconds to respect rate limits...")
            time.sleep(30)

        print(f"🎬 Generating video {i}/{len(imgs)} with reference: {path.name}")
        ref = image_from_file(path)
        res = generate_video(
            client,
            prompt,
            image=ref,
            out_dir=output,
            name_prefix=f"ref{i:03d}-",
            model=picked_model,
        )
        print(f"✅ {path.name} -> {res.path.name}")


if __name__ == "__main__":
    app()
