from __future__ import annotations

import pathlib
import time

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
        )
        outs.append(res.path)
        # Use the thumbnail that was already created
        if res.thumb:
            last_ref = image_from_file(res.thumb)
    print(f"✅ Completed {len(outs)} clips -> {session_dir}")


if __name__ == "__main__":
    app()
