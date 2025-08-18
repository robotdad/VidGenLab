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
