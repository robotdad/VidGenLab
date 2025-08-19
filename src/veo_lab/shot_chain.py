from __future__ import annotations

import os
import pathlib
import time

import typer
import yaml

from .common import OUT
from .common import concat_videos_concat_demuxer
from .common import create_client
from .common import create_session_directory
from .common import generate_video
from .common import image_from_file

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    file: pathlib.Path = typer.Option(..., "--file", "-f"),
    output: pathlib.Path = typer.Option(OUT, "--out"),
    concat: str | None = typer.Option(None, "--concat", help="Concatenate videos into single file"),
    model: str | None = typer.Option(
        None,
        "--model",
        help="Veo model id (e.g. veo-3.0-generate-preview, veo-3.0-fast-generate-preview, veo-2.0-generate-001)",
    ),
    dry: bool = typer.Option(
        False, "--dry", help="Show what would be generated without calling API"
    ),
):
    data = yaml.safe_load(file.read_text(encoding="utf-8"))
    prompts: list[str] = data.get("prompts", [])
    assert prompts, "no prompts found"

    # Model selection
    picked_model = model or os.environ.get("VEO_MODEL")
    if not picked_model:
        raise typer.BadParameter("Specify --model or set VEO_MODEL environment variable")

    if dry:
        print(f"🔍 Dry run - shot chain with {len(prompts)} prompts:")
        for idx, prompt in enumerate(prompts, start=1):
            print(f"  Shot {idx}: {prompt[:50]}...")
        print(f"  • Model: {picked_model}")
        if concat:
            print(f"  Would concatenate to: {concat}")
        print("✅ Dry run complete - no API calls made")
        return

    client = create_client()

    # Create a single session directory for the entire chain
    first_prompt = prompts[0] if prompts else "chain"
    session_dir = create_session_directory("shot_chain", first_prompt, output, picked_model)

    last_ref = None
    outs = []
    for i, p in enumerate(prompts, start=1):
        # Add rate limit protection: wait 30 seconds between requests (except first)
        if i > 1:
            print("⏳ Waiting 30 seconds to respect rate limits...")
            time.sleep(30)

        print(f"🎬 Generating video {i}/{len(prompts)}: {p[:50]}...")
        res = generate_video(
            client,
            p,
            image=last_ref,
            script_name="shot_chain",
            sequence_num=i,
            session_dir=session_dir,
            model=picked_model,
        )
        outs.append(res.path)
        # Use the thumbnail that was already created
        if res.thumb:
            last_ref = image_from_file(res.thumb)
    print(f"✅ Completed {len(outs)} clips -> {session_dir}")

    # Concatenate if requested
    if concat:
        concat_path = session_dir / concat
        concat_videos_concat_demuxer(outs, concat_path)
        print(f"🎬 Concatenated {len(outs)} videos -> {concat_path}")


if __name__ == "__main__":
    app()
