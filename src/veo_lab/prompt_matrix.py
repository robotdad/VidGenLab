from __future__ import annotations

import itertools
import json
import pathlib
import time

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
    total_combinations = len(combos) * len(negatives)
    current_combination = 0

    for combo in combos:
        vars_ = dict(zip(bank, combo, strict=False))
        prompt = Template(tpl_text).render(**vars_).strip()
        for neg in negatives:
            current_combination += 1

            if dry:
                print(f"Combination {current_combination}/{total_combinations}: {prompt}")
                continue

            # Add rate limit protection: wait 30 seconds between requests (except first)
            if current_combination > 1:
                print("⏳ Waiting 30 seconds to respect rate limits...")
                time.sleep(30)

            print(f"🎬 Generating {current_combination}/{total_combinations}: {prompt[:50]}...")
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
