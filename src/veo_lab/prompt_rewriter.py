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
