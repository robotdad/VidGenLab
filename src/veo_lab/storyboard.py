from __future__ import annotations

import json
import pathlib
import time

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
        # Add rate limit protection: wait 30 seconds between requests (except first)
        if idx > 1:
            print("⏳ Waiting 30 seconds to respect rate limits...")
            time.sleep(30)

        prompt: str = shot["prompt"]
        negative: str = shot.get("negative", "")
        carry_last: bool = bool(shot.get("carry_last_frame", False))
        image_path = shot.get("image")
        ref = prev_last_ref if (carry_last and prev_last_ref is not None) else None
        if image_path:
            ref = image_from_file(pathlib.Path(image_path))

        print(f"🎬 Generating shot {idx}/{len(shots)}: {prompt[:50]}...")
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
